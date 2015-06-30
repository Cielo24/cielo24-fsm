# encoding: utf-8
from __future__ import unicode_literals

from exceptions import OnExitNoSupportedInDeadState

class State(object):

    def __init__(self, id, final=False, on_enter=None, on_exit=None, on_loop_enter=None, on_loop_exit=None):
        """
        Initializes a new state.

        :param id: Id associated with this state. No two states in an FSM can have identical Ids.
        :param final: Indicates whether the state is final or not.
        :param on_enter: Callback to perform when entering this state during a transition from some other state.
        :param on_exit: Callback to perform when leaving this state during a transition to some other state.
        :param on_loop_enter: Callback to perform when entering this state during a transition from this state.
        :param on_loop_exit: Callback to perform when leaving this state during a transition to this state.
        :return:
        """

        # Define private fields
        self._id = None
        self._final = None
        self._on_enter = None
        self._on_exit = None
        self._on_loop_enter = None
        self._on_loop_exit = None

        # Set properties
        self.id = id
        self.final = final
        self.on_enter = on_enter
        self.on_exit = on_exit
        self.on_loop_enter = on_loop_enter
        self.on_loop_exit = on_loop_exit

    @property
    def id(self):
        return self._id

    @property
    def final(self):
        return self._final

    @property
    def on_enter(self):
        return self._on_enter

    @property
    def on_exit(self):
        return self._on_exit

    @property
    def on_loop_enter(self):
        return self._on_loop_enter

    @property
    def on_loop_exit(self):
        return self._on_loop_exit

    @id.setter
    def id(self, value):
        assert value is not None, 'Id cannot be None'
        self._id = value

    @final.setter
    def final(self, value):
        assert isinstance(value, bool), 'Final must be a boolean'
        self._final = value

    @on_enter.setter
    def on_enter(self, value):
        assert callable(value), 'On-Enter callback must be callable'
        self._on_enter = value

    @on_exit.setter
    def on_exit(self, value):
        assert callable(value), 'On-Exit callback must be callable'
        self._on_exit = value

    @on_loop_enter.setter
    def on_loop_enter(self, value):
        assert callable(value), 'On-Loop-Enter callback must be callable'
        self._on_loop_enter = value

    @on_loop_exit.setter
    def on_loop_exit(self, value):
        assert callable(value), 'On-Loop-Exit callback must be callable'
        self._on_loop_exit = value

    # The below operators are overridden to support dictionary operations
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.id == other.id
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self._id)


class DeadState(State):

    def __init__(self, id, final=False, on_enter=None, on_loop_enter=None, on_loop_exit=None):
        """
        Initializes a new dead state. Dead state is a state from which there is no return.
        It does not support on_exit callbacks for that reason. Only one dead state can exist per FSM.

        :param id: Id associated with this state. Each state in the FSM must have a unique Id.
        :param final: Indicates whether the state is final or not.
        :param on_enter: Callback to perform when entering this state during a transition from some other state.
        :param on_loop_enter: Callback to perform when entering this state during a transition from this same state.
        :param on_loop_exit: Callback to perform when leaving this state during a transition to this same state.
        :return:
        """
        super(DeadState, self).__init__(id=id,
                                        final=final,
                                        on_enter=on_enter,
                                        on_loop_enter=on_loop_enter,
                                        on_loop_exit=on_loop_exit)

    @property
    def on_exit(self):
        raise OnExitNoSupportedInDeadState

    @on_exit.setter
    def on_exit(self, value):
        raise OnExitNoSupportedInDeadState
