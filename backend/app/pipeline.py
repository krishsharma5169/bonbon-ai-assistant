import re
import time
from backend.app.llm import ask_model
from backend.app.prompts import structured_prompt, repair_prompt, critic_prompt
from backend.app.executor import execute_python
from backend.app.config import MAX_ATTEMPTS, DEBUG, FAST_MODE, AUTO_ESCALATE, ESCALATE_ON_REPAIR, ESCALATE_ON_CRITIC_REWRITE


def extract_code(text):
    match = re.search(r"```python(.*?)```", text, re.DOTALL)
    if match:
        return match.group(1).strip()

    fallback = re.search(r"(def\s+\w+\(.*?\):[\s\S]*)", text)
    if fallback:
        return fallback.group(1).strip()

    return text.strip()


def generate_with_mode(problem, use_fast):
    voting_time = 0
    selected = "Single"

    if use_fast:
        response = ask_model(structured_prompt(problem))
        code = extract_code(response)
    else:
        voting_start = time.time()

        response_a = ask_model(structured_prompt(problem))
        code_a = extract_code(response_a)

        response_b = ask_model(structured_prompt(problem))
        code_b = extract_code(response_b)

        comparison_prompt = f"""
Compare Solution A and Solution B.
Return only 'A' or 'B'.

Solution A:
{code_a}

Solution B:
{code_b}
"""

        decision = ask_model(comparison_prompt, temperature=0.1)
        match = re.search(r"\b(A|B)\b", decision)
        selected = match.group(1) if match else "A"

        code = code_a if selected == "A" else code_b
        voting_time = time.time() - voting_start

    return code, selected, voting_time


def solve(problem, test_input=None, expected_output=None):
    start_time = time.time()
    critic_rewrite = False
    first_pass_success = False

    # --------------------------
    # INITIAL GENERATION
    # --------------------------
    use_fast = FAST_MODE
    code, selected, voting_time = generate_with_mode(problem, use_fast)

    # --------------------------
    # EXECUTION + REPAIR
    # --------------------------
    attempt = 0
    success, output = execute_python(code, test_input)

    if success:
        first_pass_success = True

    while not success and attempt < MAX_ATTEMPTS:
        repair = repair_prompt(code, output)
        code = extract_code(ask_model(repair))
        attempt += 1
        success, output = execute_python(code, test_input)

    # --------------------------
    # CRITIC
    # --------------------------
    critic_response = ask_model(critic_prompt(code, problem), temperature=0.1)

    if "APPROVED" not in critic_response:
        improved = extract_code(critic_response)
        if "def" in improved:
            code = improved
            critic_rewrite = True

    # --------------------------
    # AUTO ESCALATION LOGIC
    # --------------------------
    should_escalate = (
        AUTO_ESCALATE and
        use_fast and
        (
            (ESCALATE_ON_REPAIR and attempt > 0) or
            (ESCALATE_ON_CRITIC_REWRITE and critic_rewrite)
        )
    )

    if should_escalate:
        if DEBUG:
            print("\n--- AUTO ESCALATION TRIGGERED ---")

        # Re-run in voting mode
        code, selected, voting_time = generate_with_mode(problem, use_fast=False)

        # Re-run repair loop
        attempt = 0
        success, output = execute_python(code, test_input)

        while not success and attempt < MAX_ATTEMPTS:
            repair = repair_prompt(code, output)
            code = extract_code(ask_model(repair))
            attempt += 1
            success, output = execute_python(code, test_input)

        critic_response = ask_model(critic_prompt(code, problem), temperature=0.1)

        if "APPROVED" not in critic_response:
            improved = extract_code(critic_response)
            if "def" in improved:
                code = improved
                critic_rewrite = True

        use_fast = False  # Escalated mode

    total_time = time.time() - start_time

    if DEBUG:
        print("\n--- Performance Metrics ---")
        print("Mode:", "FAST" if use_fast else "VOTING")
        print("Selected:", selected)
        print("First Pass Success:", first_pass_success)
        print("Repair Attempts:", attempt)
        print("Total Solve Time:", round(total_time, 2))
        print("Critic Rewrite:", critic_rewrite)

    return {
        "code": code,
        "mode": "FAST" if use_fast else "VOTING",
        "repair_attempts": attempt,
        "critic_rewrite": critic_rewrite,
        "first_pass_success": first_pass_success,
        "total_time": round(total_time, 2)
    }