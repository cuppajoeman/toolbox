import random

def random_partition(n, s):
    partition = [0] * s
    for x in range(n):
        partition[random.randrange(s)] += 1
    return partition

def random_partition_with_choices_differing_length(n, choices):
    # assuming the choices will always give rise to a paritition
    # a bad input would be n = 10 and choices = [3]
    # a good input would be n = 10 and choices = [2,3]
    partition = []
    while sum(partition) !=  n:
        x = random.choice(choices)
        # Keep trying ones until it's a valid choice
        while x + sum(partition) > n:
            x = random.choice(choices)
        partition.append(x)
    return partition


print(random_partition_with_choices_differing_length(12,[1,2,3,4,5,6] ))
