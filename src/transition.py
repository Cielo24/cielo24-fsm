# encoding: utf-8

from state import State
from exceptions import SourceStateCannotBeDead

class Transition(object):

    def __init__(self, symbol, src_state, dst_state, on_transition=None):
        """
        Transition diagram:
        (source_state) --------symbol-------> (destination_state)

        Event diagram (corresponds to the above diagram):
        (on_exit) ---------(on_transition)-----> (on_enter)

        Event diagram for a loop transition (where source_state == destination_state):
        (on_loop_exit) ----(on_transition)-----> (on_loop_enter)

        :param symbol: Symbol associated with this transition
        :param src_state: The source state of this transition
        :param dst_state: The destination state of this transition
        :param on_transition: Callback to perform during this transition
        :return:
        """
        # Define private fields
        self._symbol = None
        self._src_state = None
        self._dst_state = None
        self._on_transition = None
        # Set properties
        self.symbol = symbol
        self.src_state = src_state
        self.dst_state = dst_state
        self.on_transition = on_transition

    @property
    def symbol(self):
        return self._symbol

    @property
    def src_state(self):
        return self._src_state

    @property
    def dst_state(self):
        return self._dst_state

    @property
    def on_transition(self):
        return self._on_transition

    @symbol.setter
    def symbol(self, value):
        assert value is not None, 'Symbol cannot be None'
        self._symbol = value

    @src_state.setter
    def src_state(self, value):
        assert isinstance(value, State), 'Source must be a valid state'
        if value.dead:
            raise SourceStateCannotBeDead
        self._src_state = value

    @dst_state.setter
    def dst_state(self, value):
        assert isinstance(value, State), 'Destination must be a valid state'
        self._dst_state = value

    @on_transition.setter
    def on_transition(self, value):
        assert callable(value), 'On-Transition callback must be callable'
        self._on_transition = value

    # The below operators are overriden to support dictionary operations
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.symbol == other.symbol and \
                   self.src_state == other.src_state and \
                   self.dst_state == other.dst_state
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash('{}_{}_{}'.format(self.symbol, self.src_state.id, self.dst_state.id))
