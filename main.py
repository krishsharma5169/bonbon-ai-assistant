from backend.app.pipeline import solve

if __name__ == "__main__":
    problem = """
    Given an array of integers nums and an integer k,
    return the k most frequent elements.
    """

    solution = solve(problem)

    print("\nFinal Solution:\n")
    print(solution)