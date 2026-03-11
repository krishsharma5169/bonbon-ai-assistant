def structured_prompt(problem: str, context: str = ""):
    context_block = ""
    if context and context.strip():
        context_block = f"""
RELEVANT KNOWLEDGE BASE (use this to inform your solution):
---
{context}
---
"""

    return f"""
You are BonBon, an elite competitive programmer.
{context_block}
STRICTLY follow this structure:

1. Restate the problem clearly.
2. Identify constraints.
3. List all edge cases.

4. Generate THREE different algorithmic approaches.
   For each approach:
   - Explain idea
   - Time complexity
   - Space complexity

5. Select the BEST approach and justify why.

6. Provide ONLY final Python solution inside ONE ```python code block.

7. After the code block, write a SHORT 2-3 line summary covering:
   - The approach used
   - Time complexity
   - Space complexity

Problem:
{problem}
"""


def repair_prompt(code: str, failure_reason: str):
    return f"""
The following solution failed.

CODE:
{code}

FAILURE:
{failure_reason}

Fix it carefully.
Return ONLY corrected Python code inside ONE ```python code block.
"""


def critic_prompt(code: str, problem: str):
    return f"""
You are reviewing this solution for a HARD competitive programming problem.

You MUST check:

1. Is time complexity truly optimal?
2. Could it fail for large input sizes?
3. Is there a faster algorithmic approach?

If the solution is NOT optimal, you MUST rewrite it using the optimal approach.

If it is fully optimal and robust, respond only with APPROVED.

Problem:
{problem}

CODE:
{code}
"""

def generate_tests_prompt(problem: str):
    return f"""
Given the following coding problem:

{problem}

Generate 5 diverse and tricky test cases.
For each test case, provide:

1. Input
2. Expected Output

Format clearly like:

Test 1:
Input: ...
Expected Output: ...

Do NOT provide explanation.
"""