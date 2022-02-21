import logging
import sys
from os import path
try:
    from errors import TupleAdditionError
except ModuleNotFoundError:
    from .errors import TupleAdditionError


def get_path(filename):
    """This is really so that any executables created with pyinstaller can find
    appropriate resources. Any time a file is read or written, use this
    function with the relative path from here.
    """
    if hasattr(sys, "_MEIPASS"):
        return path.join(sys._MEIPASS, filename)
    else:
        return filename

def add_tuples(tuple_list: tuple[float]):
    """Element-wise addition for tuples of numerical types. Has no logic for 
    type compatibility.
    """
    sizes = set(len(tup) for tup in tuple_list)
    if len(sizes) > 1:
        if logging.getLogger().hasHandlers():
            logging.warning(f"Tried to feed different sized tuples to add_tuples")
        raise TupleAdditionError
    
    elements = [] * len(tuple_list[0])
    for tup in tuple_list:
        for i in range(len(tup)):
            elements[i].append(tup[i])

    if not all(isinstance(e, int) for e in elements):
        if logging.getLogger().hasHandlers():
            logging.warning(f"Tried to feed non-ints to add_tuples")
        raise TupleAdditionError

    return [sum(lst) for lst in elements]