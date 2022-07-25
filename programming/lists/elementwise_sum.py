def elementwise_sum(l1, l2):
    """
    Precondition: len(l1) == len(l2)
    """
    return [a + b for a, b in zip(l1, l2)]
