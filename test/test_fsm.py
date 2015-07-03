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
                        on_enter=partial(TestFSM._fake_callback, self, 1),
                        on_exit=partial(TestFSM._fake_callback, self, 2),
                        on_loop_enter=partial(TestFSM._fake_callback, self, 3),
                        on_loop_exit=partial(TestFSM._fake_callback, self, 4)
                        )
        self.q1 = State('q1',
                        final=True,
                        on_enter=partial(TestFSM._fake_callback, self, 5),
                        on_exit=partial(TestFSM._fake_callback, self, 6),
                        on_loop_enter=partial(TestFSM._fake_callback, self, 7),
                        on_loop_exit=partial(TestFSM._fake_callback, self, 8)
                        )
        self.q2 = State('q2',
                        final=False,
                        on_enter=partial(TestFSM._fake_callback, self, 9),
                        on_exit=partial(TestFSM._fake_callback, self, 10),
                        on_loop_enter=partial(TestFSM._fake_callback, self, 11),
                        on_loop_exit=partial(TestFSM._fake_callback, self, 12)
                        )
        self.q3 = State('q3',
                        final=True,
                        on_enter=partial(TestFSM._fake_callback, self, 13),
                        on_exit=partial(TestFSM._fake_callback, self, 14),
                        on_loop_enter=partial(TestFSM._fake_callback, self, 15),
                        on_loop_exit=partial(TestFSM._fake_callback, self, 16)
                        )
        self.ds = DeadState('ds',
                            final=False,
                            on_enter=partial(TestFSM._fake_callback, self, 17),
                            on_loop_enter=partial(TestFSM._fake_callback, self, 18),
                            on_loop_exit=partial(TestFSM._fake_callback, self, 19)
                            )

        # Transitions
        self.q0_a = Transition('a', self.q0, self.q2, on_transition=partial(TestFSM._fake_callback, self, 20))
        self.q0_b = Transition('b', self.q0, self.q1, on_transition=partial(TestFSM._fake_callback, self, 21))
        self.q0_c = Transition('c', self.q0, self.q0, on_transition=partial(TestFSM._fake_callback, self, 22))

        self.q1_a = Transition('a', self.q1, self.q1, on_transition=partial(TestFSM._fake_callback, self, 23))
        self.q1_b = Transition('b', self.q1, self.q3, on_transition=partial(TestFSM._fake_callback, self, 24))
        # self.q1_c = None

        # self.q2_a = None
        self.q2_b = Transition('b', self.q2, self.q3, on_transition=partial(TestFSM._fake_callback, self, 25))
        self.q2_c = Transition('c', self.q2, self.q3, on_transition=partial(TestFSM._fake_callback, self, 26))

        self.q3_a = Transition('a', self.q3, self.q2, on_transition=partial(TestFSM._fake_callback, self, 27))
        # self.q3_b = None
        self.q3_c = Transition('c', self.q3, self.q1, on_transition=partial(TestFSM._fake_callback, self, 28))

        # Number
        self.number = 0

    def _populate_fsm(self, states=True, transitions=True):
        # States
        if states:
            self.fsm.add_state(self.q0)
            self.fsm.add_state(self.q1)
            self.fsm.add_state(self.q2)
            self.fsm.add_state(self.q3)
            self.fsm.dead_state = self.ds
            self.fsm.initial_state = self.q0

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

    def _fake_callback(self, value):
        # fake callback function to be used to test callbacks in the FSM
        self.number += value

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
        self.assertEqual(len(self.fsm._transitions), 4)
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
        pass

    """
    SET INITIAL/DEAD STATE TESTS
    """

    """
    VALIDATE TESTS
    """

    """
    STEP TESTS
    """
