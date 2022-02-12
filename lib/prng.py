from random import seed, random

def prng(mySeed, number_values):
    seed(mySeed)
    """
    pseudo-random number generator that takes a seed value
    and returns a list of number_values values generated
    from that seed
    """
    return [random() for _ in range(number_values)]

if __name__ == "__main__":
    prng(12012)

