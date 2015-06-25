# encoding: utf-8

class State(object):

    def __init__(self, id, final=False):
        self._id = id
        self._final = final

    @property
    def id(self):
        return self._id

    @property
    def final(self):
        return self._final

    @id.setter
    def id(self, value):
        assert value is not None, 'Id cannot be None'
        self._id = value

    @final.setter
    def final(self, value):
        assert isinstance(value, bool), 'Final must be a boolean'
        self._final = value

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.id == other.id
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self._id)
