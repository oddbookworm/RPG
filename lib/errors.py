class TupleAdditionError(Exception):
    """Raised when add_tuples runs into a problem, such as different size
    tuples or tuples with different datatypes in the same index. No guarantee
    about what happens if relying on loose typing.
    """
    pass