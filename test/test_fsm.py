# encoding: utf-8

from unittest import TestCase
from functools import partial
from fsm import FSM
from state import State, DeadState
from transition import Transition
from fsm_exceptions import *


class TestFSM(TestCase):

    def setUp(self):
        # FSM (see test_fsm_diagram.png)
        self.fsm = FSM()

        # States
        self.q0 = State('q0',
                        final=False,
                        on_enter=partial(TestFSM._fake_callback, self, 'q0_on_enter'),
                        on_exit=partial(TestFSM._fake_callback, self, 'q0_on_exit'),
                        on_loop_enter=partial(TestFSM._fake_callback, self, 'q0_on_loop_enter'),
                        on_loop_exit=partial(TestFSM._fake_callback, self, 'q0_on_loop_exit')
                        )
        self.q1 = State('q1',
                        final=True,
                        on_enter=partial(TestFSM._fake_callback, self, 'q1_on_enter'),
                        on_exit=partial(TestFSM._fake_callback, self, 'q1_on_exit'),
                        on_loop_enter=partial(TestFSM._fake_callback, self, 'q1_on_loop_enter'),
                        on_loop_exit=partial(TestFSM._fake_callback, self, 'q1_on_loop_exit')
                        )
        self.q2 = State('q2',
                        final=False,
                        on_enter=partial(TestFSM._fake_callback, self, 'q2_on_enter'),
                        on_exit=partial(TestFSM._fake_callback, self, 'q2_on_exit'),
                        on_loop_enter=partial(TestFSM._fake_callback, self, 'q2_on_loop_enter'),
                        on_loop_exit=partial(TestFSM._fake_callback, self, 'q2_on_loop_exit')
                        )
        self.q3 = State('q3',
                        final=True,
                        on_enter=partial(TestFSM._fake_callback, self, 'q3_on_enter'),
                        on_exit=partial(TestFSM._fake_callback, self, 'q3_on_exit'),
                        on_loop_enter=partial(TestFSM._fake_callback, self, 'q3_on_loop_enter'),
                        on_loop_exit=partial(TestFSM._fake_callback, self, 'q3_on_loop_exit')
                        )
        self.ds = DeadState('ds',
                            final=False,
                            on_enter=partial(TestFSM._fake_callback, self, 'dead_on_enter'),
                            on_loop_enter=partial(TestFSM._fake_callback, self, 'dead_on_loop_enter'),
                            on_loop_exit=partial(TestFSM._fake_callback, self, 'dead_on_loop_exit')
                            )

        # Transitions
        self.q0_a = Transition('a', self.q0, self.q2, on_transition=partial(TestFSM._fake_callback, self, 'q0_a'))
        self.q0_b = Transition('b', self.q0, self.q1, on_transition=partial(TestFSM._fake_callback, self, 'q0_b'))
        self.q0_c = Transition('c', self.q0, self.q0, on_transition=partial(TestFSM._fake_callback, self, 'q0_c'))

        self.q1_a = Transition('a', self.q1, self.q1, on_transition=partial(TestFSM._fake_callback, self, 'q1_a'))
        self.q1_b = Transition('b', self.q1, self.q3, on_transition=partial(TestFSM._fake_callback, self, 'q1_b'))
        # self.q1_c = None

        # self.q2_a = None
        self.q2_b = Transition('b', self.q2, self.q3, on_transition=partial(TestFSM._fake_callback, self, 'q2_b'))
        self.q2_c = Transition('c', self.q2, self.q3, on_transition=partial(TestFSM._fake_callback, self, 'q2_c'))

        self.q3_a = Transition('a', self.q3, self.q2, on_transition=partial(TestFSM._fake_callback, self, 'q3_a'))
        # self.q3_b = None
        self.q3_c = Transition('c', self.q3, self.q1, on_transition=partial(TestFSM._fake_callback, self, 'q3_c'))

        # Step stack
        self.step_stack = []

    def _populate_fsm(self, states=True, transitions=True, initial=True, dead=True):
        # States
        if states:
            self.fsm.add_state(self.q0)
            self.fsm.add_state(self.q1)
            self.fsm.add_state(self.q2)
            self.fsm.add_state(self.q3)

        # Initial state
        if initial:
            self.fsm.initial_state = self.q0

        # Dead state
        if dead:
            self.fsm.dead_state = self.ds

        # Transitions
        if transitions:
            self.fsm.add_transition(self.q0_a)
            self.fsm.add_transition(self.q0_b)
            self.fsm.add_transition(self.q0_c)

            self.fsm.add_transition(self.q1_a)
            self.fsm.add_transition(self.q1_b)
            # self.fsm.add_transition(self.q1_c)

            # self.fsm.add_transition(self.q2_a)
            self.fsm.add_transition(self.q2_b)
            self.fsm.add_transition(self.q2_c)

            self.fsm.add_transition(self.q3_a)
            # self.fsm.add_transition(self.q3_b)
            self.fsm.add_transition(self.q3_c)

        # Validate
        if states and transitions and initial and dead:
            self.fsm.validate()

    def _fake_callback(self, value):
        # fake callback function to be used to test callbacks in the FSM
        self.step_stack.append(value)

    """
    ADD STATE TESTS
    """

    # Regular add
    def test_add_state(self):
        self.fsm.add_state(self.q0)
        self.assertIn(self.q0, self.fsm._states)
        self.assertTrue(self.fsm._dirty)

    # Duplicate add
    def test_add_state_duplicate(self):
        self.fsm.add_state(self.q0)
        with self.assertRaises(DuplicateState):
            self.fsm.add_state(self.q0)

    # Invalid type add
    def test_add_state_invalid_type(self):
        with self.assertRaises(AssertionError):
            self.fsm.add_state(self.ds)
        self.assertNotIn(self.ds, self.fsm._states)

        with self.assertRaises(AssertionError):
            self.fsm.add_state(None)
        self.assertNotIn(None, self.fsm._states)

    # Many state add
    def test_add_state_many(self):
        for state in [self.q0, self.q1, self.q2, self.q3]:
            self.fsm.add_state(state)
            self.assertIn(state, self.fsm._states)
            self.assertTrue(self.fsm._dirty)

    """
    ADD TRANSITION TESTS
    """

    # Regular add
    def test_add_transition(self):
        self.fsm.add_state(self.q0)
        self.fsm.add_state(self.q2)
        self.fsm.add_transition(self.q0_a)
        self.assertIn(self.q0_a, self.fsm._transitions)
        self.assertIn(self.q0_a.symbol, self.fsm._alphabet)
        self.assertEqual(self.fsm._map[self.q0_a.symbol][self.q0_a.src_state],
                         (self.q0_a.dst_state, self.q0_a.on_transition))

    # Duplicate add
    def test_add_transition_duplicate(self):
        self._populate_fsm()
        with self.assertRaises(DuplicateTransition):
            self.fsm.add_transition(self.q0_a)

    # Invalid type add
    def test_add_transition_invalid_type(self):
        with self.assertRaises(AssertionError):
            self.fsm.add_transition(self.ds)
        self.assertNotIn(self.ds, self.fsm._transitions)

        with self.assertRaises(AssertionError):
            self.fsm.add_transition(None)
        self.assertNotIn(None, self.fsm._transitions)

    # Unknown dst_state add
    def test_add_transition_unknown_dst(self):
        self._populate_fsm()
        unknown_state = State('unknown')
        transition = Transition('a', self.q2, unknown_state)
        with self.assertRaises(TransitionContainsUnknownState):
            self.fsm.add_transition(transition)

    # Unknown src_state add
    def test_add_transition_unknown_src(self):
        self._populate_fsm()
        unknown_state = State('unknown')
        transition = Transition('a', unknown_state, self.q2)
        with self.assertRaises(TransitionContainsUnknownState):
            self.fsm.add_transition(transition)

    # Transition exists add (NFA behavior must be prevented)
    def test_add_transition_transition_exists(self):
        self._populate_fsm()
        # Note that q0 already has 'b' transition to q1
        # Added another 'b' transition should result in an error
        transition = Transition('b', self.q0, self.q2)
        with self.assertRaises(StateCannotHaveSameSymbolTransitions):
            self.fsm.add_transition(transition)

    # Many transition add
    def test_add_transition_many(self):
        self._populate_fsm(transitions=False)
        for transition in [self.q0_a, self.q0_b, self.q0_c, self.q1_a, self.q1_b, self.q2_b, self.q2_c, self.q3_a, self.q3_c]:
            self.fsm.add_transition(transition)
            self.assertIn(transition, self.fsm._transitions)
            self.assertIn(transition.symbol, self.fsm._alphabet)
            self.assertEqual(self.fsm._map[transition.symbol][transition.src_state],
                             (transition.dst_state, transition.on_transition))

    """
    REMOVE STATE TESTS
    """

    # Regular remove
    def test_remove_state(self):
        self._populate_fsm()
        self.fsm.remove_state(self.q0)
        self.assertNotIn(self.q0, self.fsm._states)
        self.assertNotIn(self.q0_a, self.fsm._transitions)
        self.assertNotIn(self.q0_b, self.fsm._transitions)
        self.assertNotIn(self.q0_c, self.fsm._transitions)
        self.assertNotIn(self.q0_a.src_state, self.fsm._map[self.q0_a.symbol])
        self.assertNotIn(self.q0_b.src_state, self.fsm._map[self.q0_b.symbol])
        self.assertNotIn(self.q0_c.src_state, self.fsm._map[self.q0_c.symbol])
        self.assertTrue(self.fsm._dirty)

    # Invalid type remove
    def test_remove_state_invalid_type(self):
        self._populate_fsm()
        with self.assertRaises(AssertionError):
            self.fsm.remove_state(self.ds)
        with self.assertRaises(AssertionError):
            self.fsm.remove_state(None)

    # Current remove
    def test_remove_state_current(self):
        self._populate_fsm()
        self.fsm.step(self.q0_a.symbol)  # from q0 to q2
        with self.assertRaises(CannotModifyStateThatIsCurrent):
            self.fsm.remove_state(self.q2)
        self.assertIn(self.q2, self.fsm._states)

    # Symbol remove
    def test_remove_state_symbol(self):
        # Verify that the symbol gets removed from the map
        # if no transitions with that symbol are left
        self._populate_fsm()
        self.fsm.remove_state(self.q1)
        self.assertEqual(len(self.fsm._transitions), 5)
        self.fsm.remove_state(self.q3)
        self.assertEqual(len(self.fsm._transitions), 2)
        self.assertNotIn('b', self.fsm._alphabet)
        self.assertNotIn('b', self.fsm._map)
        self.fsm.remove_state(self.q2)
        self.assertEqual(len(self.fsm._transitions), 1)
        self.assertNotIn('a', self.fsm._alphabet)
        self.assertNotIn('a', self.fsm._map)
        self.assertTrue(self.fsm._dirty)

    """
    REMOVE TRANSITION TESTS
    """

    # Regular remove
    def test_remove_transition(self):
        self._populate_fsm()
        self.fsm.remove_transition(self.q0_a)
        self.assertNotIn(self.q0_a, self.fsm._transitions)
        self.assertTrue(self.fsm._dirty)

    # Invalid type remove
    def test_remove_transition_invalid_type(self):
        self._populate_fsm()
        with self.assertRaises(AssertionError):
            self.fsm.remove_transition(self.q0)
        with self.assertRaises(AssertionError):
            self.fsm.remove_transition(None)

    # Symbol remove
    def test_remove_transition_symbol(self):
        # Verify that the symbol gets removed from the map
        # if no transitions with that symbol are left
        self._populate_fsm()
        self.fsm.remove_transition(self.q0_b)
        self.fsm.remove_transition(self.q1_b)
        self.fsm.remove_transition(self.q2_b)
        self.assertNotIn(self.q0_b, self.fsm._transitions)
        self.assertNotIn(self.q1_b, self.fsm._transitions)
        self.assertNotIn(self.q2_b, self.fsm._transitions)
        self.assertNotIn('b', self.fsm._alphabet)
        self.assertNotIn('b', self.fsm._map)
        self.assertTrue(self.fsm._dirty)

    """
    SET INITIAL/DEAD STATE TESTS
    """

    # Invalid type set
    def test_set_initial_invalid_type(self):
        self._populate_fsm(initial=False)
        with self.assertRaises(AssertionError):
            self.fsm.initial_state = self.ds
        with self.assertRaises(AssertionError):
            self.fsm.initial_state = None
        # Set unknown state as initial
        with self.assertRaises(AssertionError):
            self.fsm.initial_state = State('unknown_state')
        # Should not raise any exceptions
        self.fsm.initial_state = self.q0
        self.fsm.validate()

    # Invalid type set
    def test_set_dead_invalid_type(self):
        self._populate_fsm(dead=False)
        with self.assertRaises(AssertionError):
            self.fsm.dead_state = self.q0
        # Should not raise any exceptions
        self.fsm.dead_state = self.ds
        self.fsm.validate()
        self.fsm.dead_state = None

    # Set dead state while in dead state
    def test_set_dead_in_dead(self):
        self._populate_fsm()
        self.fsm.step('b')
        self.fsm.step('c')
        # FSM should be in dead state now
        with self.assertRaises(CannotModifyStateThatIsCurrent):
            self.fsm.dead_state = DeadState('new_dead_state')

    # Get current state before setting initial
    def test_get_current_no_initial(self):
        self._populate_fsm(initial=False)
        self.assertIsNone(self.fsm.current_state)

    """
    VALIDATE TESTS
    """

    def test_validate_empty_set_of_states(self):
        with self.assertRaises(EmptySetOfStates):
            self.fsm.validate()

    def test_validate_empty_set_of_transitions(self):
        self._populate_fsm(transitions=False)
        with self.assertRaises(EmptySetOfTransitions):
            self.fsm.validate()

    def test_validate_no_final_state(self):
        self.fsm.add_state(self.q0)
        self.fsm.add_state(self.q2)
        self.fsm.initial_state = self.q0
        self.fsm.add_transition(self.q0_a)
        with self.assertRaises(NoFinalState):
            self.fsm.validate()

    def test_validate_no_initial_state(self):
        self.fsm.add_state(self.q0)
        self.fsm.add_state(self.q1)
        self.fsm.add_transition(self.q0_b)
        with self.assertRaises(NoInitialState):
            self.fsm.validate()

    def test_validate_unreachable_state(self):
        self.fsm.add_state(self.q0)
        self.fsm.add_state(self.q1)
        self.fsm.initial_state = self.q0
        self.fsm.add_transition(self.q0_c)
        with self.assertRaises(UnreachableStateDetected):
            self.fsm.validate()

    def test_validate_deterministic(self):
        self._populate_fsm(dead=False)
        with self.assertRaises(MissingTransitions):
            self.fsm.validate()
        # Now let's add missing states and revalidate
        self.q1_c = Transition('c', self.q1, self.q0)
        self.q2_a = Transition('a', self.q2, self.q0)
        self.q3_b = Transition('b', self.q3, self.q3)
        self.fsm.add_transition(self.q1_c)
        self.fsm.add_transition(self.q2_a)
        self.fsm.add_transition(self.q3_b)
        self.fsm.validate()

    """
    STEP TESTS
    """

    def test_step_regular_sequence(self):
        self._populate_fsm()
        self.assertEqual(self.q0, self.fsm.current_state)
        my_step_stack = []

        # Transition into q1:
        self.fsm.step('b')
        my_step_stack.extend(['q0_on_exit', 'q0_b', 'q1_on_enter'])
        self.assertEqual(self.q1, self.fsm.current_state)
        self.assertTrue(self.fsm.is_in_final_state())

        # Loop into q1:
        self.fsm.step('a')
        my_step_stack.extend(['q1_on_loop_exit', 'q1_a', 'q1_on_loop_enter'])
        self.assertEqual(self.q1, self.fsm.current_state)
        self.assertTrue(self.fsm.is_in_final_state())

        # Transition into q3
        self.fsm.step('b')
        my_step_stack.extend(['q1_on_exit', 'q1_b', 'q3_on_enter'])
        self.assertEqual(self.q3, self.fsm.current_state)
        self.assertTrue(self.fsm.is_in_final_state())

        # Transition into q2
        self.fsm.step('a')
        my_step_stack.extend(['q3_on_exit', 'q3_a', 'q2_on_enter'])
        self.assertEqual(self.q2, self.fsm.current_state)

        # Transition into q3
        self.fsm.step('c')
        my_step_stack.extend(['q2_on_exit', 'q2_c', 'q3_on_enter'])
        self.assertEqual(self.q3, self.fsm.current_state)
        self.assertTrue(self.fsm.is_in_final_state())

        # Transition into dead
        self.fsm.step('b')
        my_step_stack.extend(['q3_on_exit', 'dead_on_enter'])
        self.assertEqual(self.ds, self.fsm.current_state)

        # Loop in dead
        self.fsm.step('b')
        my_step_stack.extend(['dead_on_loop_exit', 'dead_on_loop_enter'])
        self.assertEqual(self.ds, self.fsm.current_state)

        # Let's check how our callbacks performed
        self.assertListEqual(my_step_stack, self.step_stack)

    def test_step_unknown_symbol(self):
        self._populate_fsm()
        with self.assertRaises(AssertionError):
            self.fsm.step('unknown_symbol')

    def test_step_transition_into_dead(self):
        self._populate_fsm()
        self.fsm.step('b')  # Transition into q1
        self.fsm.step('c')  # Undefined transition
        self.assertTrue(self.fsm.is_in_dead_state())
        for symbol in ['a', 'b', 'c']:
            self.fsm.step(symbol)
            self.assertTrue(self.fsm.is_in_dead_state())

    def test_step_dirty_bit(self):
        self._populate_fsm()
        self.fsm.add_state(State('new_state'))
        with self.assertRaises(ValidationRequired):
            self.fsm.step('a')
