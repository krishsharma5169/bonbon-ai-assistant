problems = [
    {
        "name": "Maximum Subarray",
        "problem": """
Given an integer array nums, find the contiguous subarray 
which has the largest sum and return its sum.
""",
        "function": "maxSubArray",
        "tests": [
            {"args": [[-2,1,-3,4,-1,2,1,-5,4]], "expected": 6},
            {"args": [[1]], "expected": 1},
            {"args": [[-1,-2,-3]], "expected": -1},
            {"args": [[5,-2,3,4]], "expected": 10}
        ]
    },
    {
        "name": "Top K Frequent",
        "problem": """
Given an array of integers nums and an integer k,
return the k most frequent elements.
""",
        "function": "topKFrequent",
        "tests": [
            {"args": [[1,1,1,2,2,3], 2], "expected": [1,2]},
            {"args": [[4,4,4,6,6,7], 1], "expected": [4]},
            {"args": [[1], 1], "expected": [1]},
            {"args": [[1,2,3,4], 4], "expected": [1,2,3,4]}
        ]
    },
    {
        "name": "Longest Increasing Subsequence",
        "problem": """
Given an integer array nums, return the length of the longest 
strictly increasing subsequence.
""",
        "function": "lengthOfLIS",
        "tests": [
            {"args": [[10,9,2,5,3,7,101,18]], "expected": 4},
            {"args": [[0,1,0,3,2,3]], "expected": 4},
            {"args": [[7,7,7,7,7]], "expected": 1},
            {"args": [[1,3,6,7,9,4,10,5,6]], "expected": 6}
        ]
    }
]