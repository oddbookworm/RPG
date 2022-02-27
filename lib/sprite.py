import pygame as pg

class Sprite:
    """A custom implementation of a Sprite class instead of the pygame
    built-in class
    """
    def __init__(self):
        pass

    def get_attrs(self):
        from inspect import getmembers, ismethod
        attrs = []
        for i in getmembers(self):
            if not i[0].startswith('_'):
                if not ismethod(i[1]):
                    attrs.append(i)
        return attrs
    
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return set(self.get_attrs()) == set(other.get_attrs())
        else:
            return NotImplemented

class SpriteGroup:
    """A custom implementation of a Group class instead of the pygame
    built-in class
    """
    def __init__(self):
        self.sprites = {}
