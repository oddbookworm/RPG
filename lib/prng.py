from random import seed, random

def prng(mySeed, number_values):
    """pseudo-random number generator that takes a seed value
    and returns a list of number_values values generated
    from that seed
    """
    seed(mySeed)
    return [random() for _ in range(number_values)]

if __name__ == "__main__":
    randoms = prng(12012, 1000)

    first = [r for r in randoms if r <= 0.55]
    second = [r for r in randoms if r > 0.55]

    print(len(first) / (len(first) + len(second)))