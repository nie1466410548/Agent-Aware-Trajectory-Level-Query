from math import comb

K_LIST = [1, 5, 10, 15, 20, 30, 40, 50]

def pass_at_k(n, c, k):
    """
    Calculate pass@k metric.

    Args:
        n (int): Total number of attempts.
        c (int): Number of correct attempts.
        k (int): Number of top attempts to consider.

    Returns:
        float: pass@k value.
    """
    if c == 0:
        return 0.0
    if n - c < k:
        return 1.0

    passk = 1.0 - comb(n - c, k) / comb(n, k)
    return passk

def pass_at_k_list(n, c):
    """
    Calculate pass@k for a list of k values.

    Args:
        n (int): Total number of attempts.
        c (int): Number of correct attempts.

    Returns:
        dict: Dictionary of pass@k values for each k in K_LIST.
    """
    results = {}
    for k in K_LIST:
        results[f"pass@{k}"] = pass_at_k(n, c, k)
    return results