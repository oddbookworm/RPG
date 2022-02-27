class TupleAdditionError(Exception):
    """Raised when add_tuples runs into a problem, such as different size
    tuples or tuples with different datatypes in the same index
    """
    pass