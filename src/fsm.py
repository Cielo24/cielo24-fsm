# encoding: utf-8
from __future__ import unicode_literals

from state import State
from transition import Transition
from exceptions import *

class FSM(object):

    def __init__(self):
        # Set of all states in this FSM
        self._states = set()

        # Set of all transitions in this FSM
        self._transitions = set()

        # Current state of the FSM
        self._current_state = None

        # Initial state of this FSM
        self._initial_state = None

        # Set of all symbols
        self._alphabet = set()

        # When defined, this variable contains the dead state for this FSM.
        # Note that there will never be a transition that involves a dead state.
        # Hence, on_transition callback should be merged into on_enter/on_loop_enter callback of the dead state.
        self._dead_state = None

        # Indicates whether this FSM needs validation before next step
        self._dirty = False

        # Indicates whether step() has been called at least once
        self._execution_started = False

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
        assert isinstance(value, State), 'Invalid type'
        assert value in self._states, 'State not in the set of known states'
        # Does not require dirty flag if it passed the asserts
        self._initial_state = value
        if self._execution_started:
            self._current_state = self._initial_state

    def is_dead_state_on(self):
        """
        :return: True if this FSM contains a dead state. False, otherwise.
        """
        return self._dead_state is not None

    def is_in_final_state(self):
        """
        :return: True if the current state is final, False otherwise.
        """
        return self._current_state.final

    def is_in_dead_state(self):
        """
        :return: True if the current state is "dead" state. False, otherwise.
        """
        return self.current_state.dead

    def step(self, symbol):
        """
        Follows a transition corresponding to the given symbol and the current state, into the destination state.
        Throws an exception if the symbol is not in the alphabet.
        :param symbol: Symbol to follow
        :return:
        """
        # Throw exception if FSM has not been validated (dirty)
        if self._dirty:
            raise ValidationRequired
        else:
            self._execution_started = True

        # "loop" variable indicates whether to invoke the on_loop_* versions of the callbacks
        if self.is_dead_state_on() and self.is_in_dead_state():
            # Stay in dead state no matter what (loop)
            dst_state = self._dead_state
            on_transition_fn = None
            loop = True
        elif symbol not in self._alphabet:
            # If unknown symbol and dead state is enabled
            if self.is_dead_state_on():
                # Transition into dead state
                dst_state = self._dead_state
                on_transition_fn = None
                loop = False
            else:
                raise UnknownSymbol
        else:
            # Everything OK - retrieve dst_state from the map
            (dst_state, on_transition_fn) = self._map[symbol][self._current_state]
            loop = True if self._current_state == dst_state else False

        # Perform on_exit callbacks
        self._perform_call(self._current_state.on_exit) if loop \
            else self._perform_call(self._current_state.on_loop_exit)
        # Perform on_transition callbacks
        self._perform_call(on_transition_fn)
        # Set current state (transition)
        self._current_state = dst_state
        # Perform on_enter callbacks
        self._perform_call(self._current_state.on_enter) if loop \
            else self._perform_call(self._current_state.on_loop_enter)

    def add_state(self, state):
        """
        Adds the given state to the FSM. New state must have a unique id, otherwise an error is thrown.
        :param state: State to be added to this FSM.
        :return:
        """
        assert isinstance(state, State), 'Invalid argument type'
        # If such state already exists
        if state in self._states:
            raise DuplicateState
        # If given state is dead state
        if state.dead:
            # Throw exception if this FSM already has a dead state
            # (only one dead state is allowed per FSM)
            if not self.is_dead_state_on():
                self._dead_state = state
            else:
                raise OnlyOneDeadStatePerFSMAllowed
        else:
            self._states.add(state)
        # Set the dirty bit
        self._dirty = True

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
        # Throw error if transition contains unknown states
        if transition.src_state not in self._states or transition.dst_state not in self._states:
            raise TransitionContainsUnknownState
        # Add symbol to the alphabet
        self._alphabet.add(transition.symbol)
        # Update the transition map
        if transition.symbol not in self._map.keys():
            # Create an entry for symbol if it does not already exist in the outer dict
            self._map[transition.symbol] = dict()
        # Insert src-dst pair
        self._map[transition.symbol][transition.src_state] = (transition.dst_state, transition.on_transition)

    def remove_state(self, state):
        """
        Removes the given state from the set of states, removes all corresponding transitions
        from the set of transitions and from the map.
        :param state: State to remove
        :return:
        """
        # If given state is dead state
        if state.dead:
            if self._current_state.dead:
                raise CannotRemoveStateThatIsCurrent
            else:
                self._dead_state = None

        # Remove state from set of states
        self._states.remove(state)
        # Remove from map
        for symbol in self._map.iterkeys():
            inner_dict = self._map[symbol]
            for src, (dst, _) in inner_dict.iteritems():
                if src == state or dst == state:
                    # Remove transition from map
                    inner_dict.pop(src, None)
                    # Remove transition from set of transitions
                    self._transitions.remove(Transition(symbol, src, dst))
            # Check if the inner dict is empty
            if len(inner_dict) == 0:
                self._alphabet.remove(symbol)
                self._map.pop(symbol, None)
        # Set the dirty bit
        self._dirty = True

    def remove_transition(self, transition):
        """
        Removes the given transition from the set of transition and the map.
        :param transition: Transition to remove
        :return:
        """
        # Remove transition from set of transitions
        self._states.remove(transition)
        # Remove transition from map
        self._map[transition.symbol].pop(transition.src, None)
        # If this was the last remaining transition with the corresponding symbol
        if len(self._map[transition.symbol]) == 0:
            self._alphabet.remove(transition.symbol)
            self._map.pop(transition.symbol, None)
        # Set the dirty bit
        self._dirty = True

    def validate(self):
        if self.is_dead_state_on():
            self._validate_with_dead_state()
        else:
            self._validate_ideal()

    def _validate_with_dead_state(self):
        """
        Checks whether this FSM follows some of the constraints for an ideal FSM.
        (i.e. constraints required in the "dead" state mode)
        Throws exceptions to indicate the problem.
        'Initial state must belong to the set of states' constraint is enforced in the setter.
        :return:
        """
        # Set of states must not be empty (otherwise there is no FSM)
        if len(self._states) == 0:
            raise EmptySetOfStates
        # Set of transitions must not be empty (otherwise there is no FSM)
        if len(self._transitions) == 0:
            raise EmptySetOfTransitions
        # There must be at least one final state
        if len([state for state in self._states if state.final]):
            raise NoFinalState
        # There must be an initial state
        if not self.initial_state:
            raise NoInitialState
        # No state should be disconnected from the rest of the states
        # i.e. for each state x there must be a transition from state y to x, s.t. x != y
        dst_dict = {state: False for state in self._states}
        for inner_dict in self._map.itervalues():
            for src, dst in inner_dict.iteritems():
                if src != dst:
                    dst_dict[dst] = True
        if len([x for x in dst_dict.itervalues() if not x]) != 0:
            raise DisconnectedState

    def _validate_ideal(self):
        """
        Checks whether this FSM follows all of the constraints for an ideal FSM.
        Throws exceptions to indicate the problem.
        'Initial state must belong to the set of states' constraint is enforced in the setter.
        :return:
        """
        # "dead" state mode covers most of the ideal requirements
        self._validate_with_dead_state()

        # The number of transitions must be equal to the number of states times the size of the alphabet
        if len(self._transitions) != len(self._states) * len(self._alphabet):
            raise MissingTransitions

    def _perform_call(self, fn):
        """
        Helper function.
        :param fn: Callable object that need to be called (if it is actually callable)
        :return:
        """
        if callable(fn):
            fn()

    def to_JSON(self):
        raise NotImplementedError

    def from_JSON(self, json_str):
        raise NotImplementedError
