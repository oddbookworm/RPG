class TupleAdditionError(Exception):
    """Raised when add_tuples runs into a problem, such as different size
    tuples or tuples with different datatypes in the same index.
    """
    pass

class TilesetKeyError(Exception):
    """Raised when a tileset has incorrect keys when passed into a method
    that requires specific keys. To see the correct keys, look at the
    docstring for that particular method."""
    pass