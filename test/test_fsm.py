# encoding: utf-8
from __future__ import unicode_literals

from unittest import TestCase
from fsm import FSM
from state import State, DeadState
from transition import Transition


class TestFSM(TestCase):

    def setUp(self):
        # FSM (see test_fsm_diagram.png)
        self.fsm = FSM()

        # States
        self.q0 = State('q0',
                        final=False,
                        on_enter=lambda: self._fake_callback(1),
                        on_exit=lambda: self._fake_callback(2),
                        on_loop_enter=lambda: self._fake_callback(3),
                        on_loop_exit=lambda: self._fake_callback(4)
                        )
        self.q1 = State('q1',
                        final=True,
                        on_enter=lambda: self._fake_callback(5),
                        on_exit=lambda: self._fake_callback(6),
                        on_loop_enter=lambda: self._fake_callback(7),
                        on_loop_exit=lambda: self._fake_callback(8)
                        )
        self.q2 = State('q2',
                        final=False,
                        on_enter=lambda: self._fake_callback(9),
                        on_exit=lambda: self._fake_callback(10),
                        on_loop_enter=lambda: self._fake_callback(11),
                        on_loop_exit=lambda: self._fake_callback(12)
                        )
        self.q3 = State('q3',
                        final=True,
                        on_enter=lambda: self._fake_callback(13),
                        on_exit=lambda: self._fake_callback(14),
                        on_loop_enter=lambda: self._fake_callback(15),
                        on_loop_exit=lambda: self._fake_callback(16)
                        )
        self.ds = DeadState('ds',
                            final=False,
                            on_enter=lambda: self._fake_callback(17),
                            on_loop_enter=lambda: self._fake_callback(18),
                            on_loop_exit=lambda: self._fake_callback(19)
                            )

        # Transitions
        self.q0_a = Transition('a', self.q0, self.q2, on_transition=lambda: self._fake_callback(20))
        self.q0_b = Transition('b', self.q0, self.q1, on_transition=lambda: self._fake_callback(21))
        self.q0_c = Transition('c', self.q0, self.q0, on_transition=lambda: self._fake_callback(22))

        self.q1_a = Transition('a', self.q1, self.q1, on_transition=lambda: self._fake_callback(23))
        self.q1_b = Transition('b', self.q1, self.q3, on_transition=lambda: self._fake_callback(24))
        self.q1_c = None

        self.q2_a = None
        self.q2_b = Transition('b', self.q2, self.q3, on_transition=lambda: self._fake_callback(25))
        self.q2_c = Transition('c', self.q2, self.q3, on_transition=lambda: self._fake_callback(26))

        self.q3_a = Transition('a', self.q3, self.q2, on_transition=lambda: self._fake_callback(27))
        self.q3_b = None
        self.q3_c = Transition('c', self.q3, self.q1, on_transition=lambda: self._fake_callback(28))

        # Number
        self.number = 0

    def _populate_fsm(self):
        # States
        self.fsm.add_state(self.q0)
        self.fsm.add_state(self.q1)
        self.fsm.add_state(self.q2)
        self.fsm.add_state(self.q3)
        self.fsm.dead_state = self.ds

        # Transitions
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

    def test_add_state(self):
        pass

    def test_add_transition(self):
        pass

    def test_remove_state(self):
        pass

    def test_remove_transition(self):
        pass
