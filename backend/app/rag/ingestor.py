"""
BonBon RAG Ingestor
====================
Run this script once (or whenever you update your knowledge base)
to embed and store your documents into ChromaDB.

Usage:
    py -m backend.app.rag.ingestor

Add your own content by editing the ALGORITHM_NOTES and
LEETCODE_PATTERNS lists below, or point it at .txt / .md files.
"""

import uuid
from backend.app.rag.embedder import get_embedding
from backend.app.rag.vectorstore import add_documents, collection_count

# ─────────────────────────────────────────────────
# KNOWLEDGE BASE — Edit / extend these freely
# ─────────────────────────────────────────────────

ALGORITHM_NOTES = [
    {
        "topic": "Sorting",
        "text": """Quick Sort: Divide and conquer. Pick a pivot, partition array into elements less than and greater than pivot, recursively sort.
Time: O(n log n) average, O(n²) worst. Space: O(log n).
Best for: General purpose in-place sorting. Avoid when worst-case matters (use merge sort instead)."""
    },
    {
        "topic": "Sorting",
        "text": """Merge Sort: Divide array in half, recursively sort each half, merge sorted halves.
Time: O(n log n) always. Space: O(n).
Best for: Stable sort, linked lists, external sorting. Guaranteed O(n log n)."""
    },
    {
        "topic": "Searching",
        "text": """Binary Search: Works on sorted arrays. Compare target with mid element, eliminate half of search space each iteration.
Time: O(log n). Space: O(1) iterative, O(log n) recursive.
Key insight: Always define your search space clearly (left/right boundaries)."""
    },
    {
        "topic": "Graph Traversal",
        "text": """BFS (Breadth-First Search): Uses a queue. Explores level by level. 
Time: O(V + E). Space: O(V).
Best for: Shortest path in unweighted graphs, level-order traversal, finding nearest neighbor."""
    },
    {
        "topic": "Graph Traversal",
        "text": """DFS (Depth-First Search): Uses a stack (or recursion). Explores as deep as possible before backtracking.
Time: O(V + E). Space: O(V).
Best for: Cycle detection, topological sort, connected components, maze solving."""
    },
    {
        "topic": "Dynamic Programming",
        "text": """Dynamic Programming: Break problem into overlapping subproblems. Store results (memoization/tabulation) to avoid recomputation.
Two approaches:
- Top-down (memoization): Recursive + cache
- Bottom-up (tabulation): Iterative DP table
Key steps: Define state, write recurrence relation, handle base cases."""
    },
    {
        "topic": "Dynamic Programming",
        "text": """Common DP patterns:
- 0/1 Knapsack: dp[i][w] = max value using first i items with weight limit w
- Longest Common Subsequence: dp[i][j] = LCS of first i and j chars
- Coin Change: dp[amount] = min coins to make amount
- Longest Increasing Subsequence: dp[i] = LIS ending at index i"""
    },
    {
        "topic": "Trees",
        "text": """Binary Search Tree (BST): Left child < node < right child.
Search/Insert/Delete: O(h) where h = height. O(log n) balanced, O(n) worst.
In-order traversal of BST gives sorted order.
Balanced BSTs: AVL Tree, Red-Black Tree guarantee O(log n)."""
    },
    {
        "topic": "Heaps",
        "text": """Heap (Priority Queue): Complete binary tree. Max-heap: parent >= children. Min-heap: parent <= children.
Insert: O(log n). Extract min/max: O(log n). Build heap: O(n).
Use heapq in Python (min-heap by default). For max-heap, negate values.
Best for: K largest/smallest elements, scheduling, Dijkstra's algorithm."""
    },
    {
        "topic": "Hashing",
        "text": """Hash Map / Hash Table: Key-value storage. Average O(1) insert, lookup, delete.
Collision handling: chaining or open addressing.
Python dict is a hash map. Use for: frequency counting, two-sum pattern, caching, grouping."""
    },
    {
        "topic": "Two Pointers",
        "text": """Two Pointers technique: Use two indices moving toward each other or in the same direction.
Common uses: Pair sum in sorted array, removing duplicates, container with most water, palindrome check.
Time: O(n). Space: O(1). Works best on sorted arrays or when shrinking a window."""
    },
    {
        "topic": "Sliding Window",
        "text": """Sliding Window: Maintain a window of elements that satisfies a condition. Expand/shrink as needed.
Fixed window: move both pointers together.
Variable window: expand right until invalid, shrink left to restore.
Best for: Subarray/substring problems — max sum, longest without repeat, minimum window substring."""
    },
    {
        "topic": "Backtracking",
        "text": """Backtracking: Explore all possibilities by building candidates incrementally and abandoning (backtracking) when a candidate fails.
Template: choose → explore → unchoose.
Best for: Permutations, combinations, subsets, N-Queens, Sudoku solver.
Time: Often exponential O(2^n) or O(n!), but pruning reduces real cost."""
    },
    {
        "topic": "Greedy",
        "text": """Greedy Algorithms: Make locally optimal choice at each step hoping to reach global optimum.
Works when: Problem has greedy choice property and optimal substructure.
Examples: Activity selection, Huffman coding, Dijkstra's, Interval scheduling.
Pitfall: Greedy doesn't always work — verify with a proof or counterexample."""
    },
]

LEETCODE_PATTERNS = [
    {
        "topic": "Two Sum Pattern",
        "text": """Pattern: Two Sum / Pair with Target Sum
Problem type: Find two numbers that sum to a target.
Approach 1 - Hash Map: Store complement (target - num) in map. O(n) time, O(n) space.
Approach 2 - Two Pointers (sorted): Move left/right pointers based on sum vs target. O(n) time, O(1) space.
Variations: Three Sum (fix one, two-pointer the rest), Four Sum."""
    },
    {
        "topic": "Top K Elements",
        "text": """Pattern: Top K Frequent / K Largest / K Smallest Elements
Approach 1 - Min Heap of size K: Push all, pop when size > K. O(n log k).
Approach 2 - Bucket Sort: Index by frequency. O(n) time and space.
Approach 3 - QuickSelect: Average O(n). Use for K-th largest in array.
Python: use heapq.nlargest(k, ...) or heapq.nsmallest(k, ...)"""
    },
    {
        "topic": "Merge Intervals",
        "text": """Pattern: Merge / Insert / Find Overlapping Intervals
Step 1: Sort intervals by start time.
Step 2: Iterate — if current interval overlaps with last merged, extend end. Else append.
Overlap condition: current.start <= last.end
Time: O(n log n). Space: O(n)."""
    },
    {
        "topic": "Fast and Slow Pointers",
        "text": """Pattern: Fast & Slow Pointers (Floyd's Cycle Detection)
Use: Detect cycle in linked list, find middle of linked list, find cycle start.
Cycle detection: fast moves 2 steps, slow moves 1. They meet if cycle exists.
Find middle: when fast reaches end, slow is at middle."""
    },
    {
        "topic": "Modified Binary Search",
        "text": """Pattern: Binary Search on Answer / Search in Rotated Array
Search in rotated sorted array: Determine which half is sorted, binary search that half.
Binary search on answer: When you can check if a value is feasible — minimize/maximize answer.
Examples: Koko eating bananas, minimum capacity to ship packages, split array largest sum."""
    },
    {
        "topic": "Tree DFS Patterns",
        "text": """Pattern: Tree DFS — Path Sum, Diameter, LCA
Path sum: Track running sum, check at leaf nodes.
Diameter: At each node, longest path = left_height + right_height. Track global max.
LCA (Lowest Common Ancestor): If both targets found below a node, that node is LCA.
All use postorder DFS (process children before parent)."""
    },
    {
        "topic": "Matrix BFS",
        "text": """Pattern: BFS on Matrix / Grid Problems
Use: Shortest path, number of islands, rotting oranges, walls and gates.
Template: Add all starting cells to queue, BFS outward, track visited.
Key: Use directions array [(0,1),(0,-1),(1,0),(-1,0)] for 4-directional movement.
Time: O(m * n). Space: O(m * n)."""
    },
    {
        "topic": "Monotonic Stack",
        "text": """Pattern: Monotonic Stack
Use: Next Greater Element, Largest Rectangle in Histogram, Daily Temperatures, Trapping Rain Water.
Increasing stack: pop when current > top (find next greater).
Decreasing stack: pop when current < top (find next smaller).
Time: O(n) — each element pushed and popped once."""
    },
    {
        "topic": "Prefix Sum",
        "text": """Pattern: Prefix Sum / Subarray Sum
prefix[i] = sum of nums[0..i-1]
Subarray sum from i to j = prefix[j+1] - prefix[i]
Use with hash map to find subarray with target sum in O(n).
Variations: 2D prefix sum for matrix queries, XOR prefix for XOR subarray problems."""
    },
    {
        "topic": "Graph Topological Sort",
        "text": """Pattern: Topological Sort (DAG ordering)
Kahn's Algorithm (BFS): Track in-degrees, start from nodes with in-degree 0, reduce neighbors' in-degree.
DFS approach: DFS, add to result after all neighbors visited (reverse post-order).
Use: Course schedule, task ordering, build systems, dependency resolution.
Cycle detection: If result length < number of nodes, a cycle exists."""
    },
]


# ─────────────────────────────────────────────────
# INGESTION LOGIC
# ─────────────────────────────────────────────────

def ingest():
    all_docs = []
    all_embeddings = []

    sources = [
        (ALGORITHM_NOTES, "algorithm"),
        (LEETCODE_PATTERNS, "pattern"),
    ]

    total = sum(len(s[0]) for s in sources)
    print(f"[Ingestor] Starting ingestion of {total} documents...\n")

    for entries, doc_type in sources:
        for entry in entries:
            doc_id = f"{doc_type}_{entry['topic'].replace(' ', '_').lower()}_{uuid.uuid4().hex[:6]}"
            text = entry["text"]
            metadata = {"type": doc_type, "topic": entry["topic"]}

            print(f"  Embedding [{doc_type}] {entry['topic']}...")
            embedding = get_embedding(text)

            all_docs.append({"id": doc_id, "text": text, "metadata": metadata})
            all_embeddings.append(embedding)

    add_documents(all_docs, all_embeddings)
    print(f"\n[Ingestor] Done. {collection_count()} documents now in ChromaDB.")


if __name__ == "__main__":
    ingest()