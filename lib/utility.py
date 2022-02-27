import logging
import sys
from os import path
try:
    from errors import TupleAdditionError
except ModuleNotFoundError:
    from .errors import TupleAdditionError

def get_path(filename) -> str:
    """This is really so that any executables created with pyinstaller can find
    appropriate resources.
    
    Any time a file is read or written, use this function with the relative 
    path from here.
    """
    if hasattr(sys, "_MEIPASS"):
        return path.join(sys._MEIPASS, filename)
    else:
        return filename

def add_tuples(tuple_list: tuple[float, str]) -> tuple[float, str]:
    """Element-wise addition of tuples.

    Supported types are int, float, and str.

    Mixing ints and floats wil return floats. Mixing strings and numerical will
    raise TupleAdditionError.
    """
    sizes = set(len(tup) for tup in tuple_list)
    if len(sizes) > 1:
        if logging.getLogger().hasHandlers():
            logging.warning(f"Tried to feed different sized tuples to add_tuples")
        raise TupleAdditionError
    
    elements = [[] for _ in range(len(tuple_list[0]))]
    for tup in tuple_list:
        for i in range(len(tup)):
            elements[i].append(tup[i])

    for elmt in elements: 
        if not all(isinstance(e, (int, float, str)) for e in elmt):
            if logging.getLogger().hasHandlers():
                logging.warning(f"Tried to feed non-ints to add_tuples")
            raise TupleAdditionError

    try:
        result = [sum(lst) for lst in elements]
    except TypeError:
        result = [''.join(lst) for lst in elements]
    return result

if __name__ == "__main__":
    tup1 = (1.1, 2)
    tup2 = (45, 8)
    tup3 = (38, 54)
    # tup1 = ("1", "2")
    # tup2 = ("3", "4")
    # tup3 = ("5", "6")
    print(add_tuples([tup1, tup2, tup3]))