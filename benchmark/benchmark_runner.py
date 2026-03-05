import csv
from backend.app.pipeline import solve
from benchmark.problems import problems


def execute_function(code, function_name, args):
    local_env = {}

    try:
        exec(code, local_env)

        if function_name not in local_env:
            return False, "Function not found"

        result = local_env[function_name](*args)
        return True, result

    except Exception as e:
        return False, str(e)


def run_benchmark():
    results = []

    print("\n=== BONBON ADVANCED BENCHMARK MODE ===\n")

    for item in problems:
        name = item["name"]
        problem_text = item["problem"]
        function_name = item["function"]
        tests = item["tests"]

        print(f"\nRunning: {name}")

        metrics = solve(problem_text)
        code = metrics["code"]

        all_passed = True

        for i, test in enumerate(tests):
            success, output = execute_function(code, function_name, test["args"])

            if not success:
                print(f"Test {i+1} crashed:", output)
                all_passed = False
                break

            expected = test["expected"]

            if isinstance(expected, list):
                if sorted(output) != sorted(expected):
                    print(f"Test {i+1} failed.")
                    print("Expected:", expected)
                    print("Got:", output)
                    all_passed = False
                    break
            else:
                if output != expected:
                    print(f"Test {i+1} failed.")
                    print("Expected:", expected)
                    print("Got:", output)
                    all_passed = False
                    break

        results.append({
            "Problem": name,
            "Passed": all_passed,
            "First Pass Success": metrics["first_pass_success"],
            "Repairs": metrics["repair_attempts"],
            "Critic Rewrite": metrics["critic_rewrite"],
            "Time (s)": metrics["total_time"]
        })

        print("Passed:", all_passed)
        print("First Pass Success:", metrics["first_pass_success"])
        print("Repair Attempts:", metrics["repair_attempts"])
        print("Critic Rewrite:", metrics["critic_rewrite"])
        print("Time:", metrics["total_time"])

    # Save CSV
    with open("benchmark_results.csv", "w", newline="") as csvfile:
        fieldnames = ["Problem", "Passed", "First Pass Success", "Repairs", "Critic Rewrite", "Time (s)"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(results)

    print("\n=== BENCHMARK COMPLETE ===")

    pass_rate = sum(r["Passed"] for r in results) / len(results) * 100
    first_pass_rate = sum(r["First Pass Success"] for r in results) / len(results) * 100
    avg_time = sum(r["Time (s)"] for r in results) / len(results)

    print(f"Overall Final Pass Rate: {pass_rate:.2f}%")
    print(f"First-Pass Success Rate: {first_pass_rate:.2f}%")
    print(f"Average Solve Time: {avg_time:.2f}s")


if __name__ == "__main__":
    run_benchmark()