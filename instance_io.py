from typing import List, Tuple

def read_max_sc_qbf_instance(filename: str) -> Tuple[int, List[List[int]], List[List[float]]]:
    """
    Reads a MAX-SC-QBF instance from a file.

    Parameters
    ----------
    filename : str
        Path to the instance file.

    Returns
    -------
    n : int
        Number of variables/subsets.
    subsets : List[List[int]]
        List of subsets; each subset is a list of covered elements (1-based).
    A : List[List[float]]
        Full n x n coefficient matrix.
    """
    with open(filename, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]

    # Read n
    n: int = int(lines[0])

    # Read sizes of each subset
    subset_sizes: List[int] = list(map(int, lines[1].split()))

    # Read subsets
    subsets: List[List[int]] = []
    idx = 2
    for size in subset_sizes:
        elements = list(map(int, lines[idx].split()))
        if len(elements) != size:
            raise ValueError(f"Expected {size} elements in subset, got {len(elements)}.")
        subsets.append(elements)
        idx += 1

    # Read upper triangular matrix
    A: List[List[float]] = [[0.0] * n for _ in range(n)]
    row = 0
    while idx < len(lines) and row < n:
        values = list(map(float, lines[idx].split()))
        for col, val in enumerate(values, start=row):
            A[row][col] = val
        idx += 1
        row += 1

    return n, subsets, A