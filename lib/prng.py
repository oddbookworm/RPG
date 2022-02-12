def prng(mySeed):
    from random import seed, random
    seed(mySeed)
    """
    pseudo-random number generator that takes a seed value
    """
    return [random() for _ in range(10)]

if __name__ == "__main__":
    print(prng(12012))