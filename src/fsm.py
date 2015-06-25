# encoding: utf-8
from state import State
from transition import Transition
from exceptions import *

class FSM(object):

    def __init__(self):
        self._states = set()
        self._transitions = set()
        self._current_state = None
        self._initial_state = None
        self._alphabet = set()
        self._map = dict()
        '''
        Map is a two-level dict with the following structure:
        {
            symbol_1: {
                src_1: dst_1,
                src_2: dst_2,
                src_3: dst_3
            },
            symbol_2: {
                src_1: dst_3,
                src_2: dst_2,
                src_3: dst_1
            }
        }
        '''

    @property
    def current_state(self):
        return self._current_state

    @property
    def initial_state(self):
        return self._initial_state

    def is_in_final_state(self):
        """
        :return: True if the current state is final, False otherwise.
        """
        return self._current_state.final

    def step(self, symbol):
        """
        Follows a transition corresponding to the given symbol and the current state, into the destination state.
        Throws an exception if the symbol is not in the alphabet.
        :param symbol: Symbol to follow
        :return:
        """
        if symbol not in self._alphabet:
            raise UnknownSymbol
        dst_state = self._map[symbol][self._current_state]
        self._current_state = dst_state

    def add_state(self, state):
        """
        Adds the given state to the FSM. New state must have a unique id, otherwise this function has no effect.
        :param state: State to be added to this FSM
        :return:
        """
        assert isinstance(state, State), 'Invalid argument type'
        self._states.add(state)
        # TODO: throw an error if duplicate state?

    def add_transition(self, transition):
        """
        Adds the given transition to the FSM. If the given transition already exists it will be ignored.
        If the given transition contains unknown states, they will automatically be added to the set of states.
        :param transition: Transition to be added to this FSM
        :return:
        """
        assert isinstance(transition, Transition), 'Invalid argument type'
        # Add transition to the set of transitions
        self._transitions.add(transition)
        # Add states from the transition
        self.add_state(transition.src)
        self.add_state(transition.dst)
        # Add symbol to the alphabet
        self._alphabet.add(transition.symbol)
        # Update the transition map
        if transition.symbol not in self._map.keys():
            # Create an entry for symbol if it does not already exist in the outer dict
            self._map[transition.symbol] = dict()
        # Insert src-dst pair
        self._map[transition.symbol][transition.src] = transition.dst

    def remove_state(self, state):
        """
        Removes the given state from the set of states, removes all corresponding transitions
        from the set of transitions and the map.
        :param state: State to remove
        :return:
        """
        # Remove from set of states
        self._states.remove(state)
        # Remove from map
        for symbol in self._map.iterkeys():
            inner_dict = self._map[symbol]
            for src, dst in inner_dict.iteritems():
                if src == state or dst == state:
                    inner_dict.pop(src, None)
                    self._transitions.remove(Transition(symbol, src, dst))
            # Check if the inner dict is empty
            if len(inner_dict) == 0:
                self._alphabet.remove(symbol)
                self._map.pop(symbol, None)

    def remove_transition(self, transition):
        """
        Removes the given transition from the set of transition and the map.
        :param transition: Transition to remove
        :return:
        """
        # Remove from set of transitions
        self._states.remove(transition)
        # Remove from map
        self._map[transition.symbol].pop(transition.src, None)
        # If this was the last remaining transition with the corresponding symbol
        if len(self._map[transition.symbol]) == 0:
            self._alphabet.remove(transition.symbol)
            self._map.pop(transition.symbol, None)

    def validate(self):
        """
        Checks whether this FSM follows all of the constraints.
        Throws exceptions to indicate the problem.
        :return:
        """
        # Set of states must not be empty
        if len(self._states) == 0:
            raise EmptySetOfStates
        # Set of transitions must not be empty
        if len(self._transitions) == 0:
            raise EmptySetOfTransitions
        # There must be at least one final state
        if len([state for state in self._states if state.final]):
            raise NoFinalState
        # There must be an initial state
        if not self.initial_state:
            raise NoInitialState
        # Initial state must belong to the set of states
        if self.initial_state not in self._states:
            raise InitialStateNotInSetOfStates
        # The number of transitions must be equal to the number of states times the size of the alphabet
        if len(self._transitions) != len(self._states) * len(self._alphabet):
            raise MissingTransitions
        # No state should be disconnected from the rest of the states
        # i.e. for each state x there must be a transition from state y to x, s.t. x != y
        dst_dict = {state: False for state in self._states}
        for inner_dict in self._map.itervalues():
            for src, dst in inner_dict.iteritems():
                if src != dst:
                    dst_dict[dst] = True
        if len([x for x in dst_dict.itervalues() if not x]) != 0:
            raise DisconnectedState
