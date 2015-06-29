# encoding: utf-8
from state import State
from transition import Transition
from exceptions import *

class FSM(object):

    def __init__(self, dead_state_on=False):
        # Set of all states
        self._states = set()
        # Set of all transitions
        self._transitions = set()
        # Current state
        self._current_state = None
        # Initial state
        self._initial_state = None
        # Set of all symbols
        self._alphabet = set()
        # When True, any unknown symbol will result in a transition
        # to the "dead" state from which there is no return
        self._dead_state_on = dead_state_on
        # Data structure for finding destination states
        # (and corresponding callbacks) based on symbol and source state
        self._map = dict()
        '''
        Map is a two-level dict with the following structure:
        {
            symbol_1: {
                src_state_1: (dst_state_1, callback),
                src_state_2: (dst_state_2, callback),
                src_state_3: (dst_state_3, callback)
            },
            symbol_2: {
                src_state_1: (dst_state_3, callback),
                src_state_2: (dst_state_2, callback),
                src_state_3: (dst_state_1, callback)
            }
        }
        '''

    @property
    def current_state(self):
        return self._current_state

    @property
    def initial_state(self):
        return self._initial_state

    @initial_state.setter
    def initial_state(self, value):
        assert isinstance(value, State), 'Invalid type"'
        assert value in self._states, 'State not in the set of known states'
        self._initial_state = value

    def is_in_final_state(self):
        """
        :return: True if the current state is final, False otherwise.
        """
        return self._current_state.final

    def is_in_dead_state(self):
        """
        :return: True if the current state is "dead" state. False, otherwise.
        Throws an exception if dead_state_on is False.
        """
        if self._dead_state_on:
            return self._current_state  # TODO
        else:
            raise DeadStateDisabled

    def step(self, symbol):
        """
        Follows a transition corresponding to the given symbol and the current state, into the destination state.
        Throws an exception if the symbol is not in the alphabet.
        :param symbol: Symbol to follow
        :return:
        """
        if symbol not in self._alphabet:
            if self._dead_state_on:
                pass  # TODO: transition into dead state
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
        if state in self._states:
            raise DuplicateState
        self._states.add(state)

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
