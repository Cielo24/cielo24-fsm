# encoding: utf-8
from state import State

class Transition(object):

    def __init__(self, symbol, src, dst):
        self._symbol = symbol
        self._src = src
        self._dst = dst

    @property
    def symbol(self):
        return self._symbol

    @property
    def src(self):
        return self._src

    @property
    def dst(self):
        return self._dst

    @symbol.setter
    def symbol(self, value):
        assert value is not None, 'Symbol cannot be None'
        self._symbol = value

    @src.setter
    def src(self, value):
        assert isinstance(value, State), 'Source must be a valid state'
        self._src = value

    @dst.setter
    def dst(self, value):
        assert isinstance(value, State), 'Destination must be a valid state'
        self._dst = value

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.symbol == other.symbol and self.src == other.src and self.dst == other.dst
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash('{}_{}_{}'.format(self.symbol, self.src.id, self.dst.id))
