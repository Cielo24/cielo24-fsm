# encoding: utf-8

from fsm_exceptions import OnExitNotSupportedInDeadState


class State(object):

    def __init__(self, id, final=False, on_enter=None, on_exit=None, on_loop_enter=None, on_loop_exit=None):
        """
        Initializes a new state.

        :param id: Id associated with this state. No two states in an FSM can have identical Ids.
        :type id: object
        :param final: Indicates whether the state is final or not.
        :type final: bool
        :param on_enter: Callback to perform when entering this state during a transition from some other state.
        :type on_enter: (callable|None)
        :param on_exit: Callback to perform when leaving this state during a transition to some other state.
        :type on_exit: (callable|None)
        :param on_loop_enter: Callback to perform when entering this state during a transition from this state.
        :type on_loop_enter: (callable|None)
        :param on_loop_exit: Callback to perform when leaving this state during a transition to this state.
        :type on_loop_exit: (callable|None)
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
        """
        Gets the id of the state.
        :return: Id
        :rtype: object
        """
        return self._id

    @property
    def final(self):
        """
        :return: True if the state is final, False otherwise.
        :rtype: bool
        """
        return self._final

    @property
    def on_enter(self):
        """
        Gets the on_enter callback of the state.
        :return: on_enter callback
        :rtype: (callable|None)
        """
        return self._on_enter

    @property
    def on_exit(self):
        """
        Gets the on_exit callback of the state.
        :return: on_exit callback
        :rtype: (callable|None)
        """
        return self._on_exit

    @property
    def on_loop_enter(self):
        """
        Gets the on_loop_enter callback of the state.
        :return: on_loop_enter callback
        :rtype: (callable|None)
        """
        return self._on_loop_enter

    @property
    def on_loop_exit(self):
        """
        Gets the on_loop_exit callback of the state.
        :return: on_loop_exit callback
        :rtype: (callable|None)
        """
        return self._on_loop_exit

    @id.setter
    def id(self, value):
        """
        Sets the id of the state.
        :param value: Id
        :type value: object
        """
        assert value is not None, 'Id cannot be None'
        self._id = value

    @final.setter
    def final(self, value):
        """
        Sets the indicator of whether the state is final.
        :param value: Final indicator
        :type value: bool
        """
        assert isinstance(value, bool), 'Final must be a boolean'
        self._final = value

    @on_enter.setter
    def on_enter(self, value):
        """
        Sets the on_enter callback of the state.
        :param value: on_enter callback
        :type value: (callable|None)
        """
        assert value is None or callable(value), 'On-Enter callback must be callable or None'
        self._on_enter = value

    @on_exit.setter
    def on_exit(self, value):
        """
        Sets the on_exit callback of the state.
        :param value: on_exit callback
        :type value: (callable|None)
        """
        assert value is None or callable(value), 'On-Exit callback must be callable or None'
        self._on_exit = value

    @on_loop_enter.setter
    def on_loop_enter(self, value):
        """
        Sets the on_loop_enter callback of the state.
        :param value: on_loop_enter callback
        :type value: (callable|None)
        """
        assert value is None or callable(value), 'On-Loop-Enter callback must be callable or None'
        self._on_loop_enter = value

    @on_loop_exit.setter
    def on_loop_exit(self, value):
        """
        Sets the on_loop_exit callback of the state.
        :param value: on_loop_exit callback
        :type value: (callable|None)
        """
        assert value is None or callable(value), 'On-Loop-Exit callback must be callable or None'
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
        Because no transition can lead to or originate from a dead state, on_transition callback should be
        made part of on_enter and on_loop_enter callbacks.

        :param id: Id associated with this state. Each state in the FSM must have a unique Id.
        :type id: object
        :param final: Indicates whether the state is final or not.
        :type final: bool
        :param on_enter: Callback to perform when entering this state during a transition from some other state.
        :type on_enter: (callable|None)
        :param on_loop_enter: Callback to perform when entering this state during a transition from this same state.
        :type on_loop_enter: (callable|None)
        :param on_loop_exit: Callback to perform when leaving this state during a transition to this same state.
        :type on_loop_exit: (callable|None)
        :return:
        """
        super(DeadState, self).__init__(id=id,
                                        final=final,
                                        on_enter=on_enter,
                                        on_loop_enter=on_loop_enter,
                                        on_loop_exit=on_loop_exit)

    @property
    def on_exit(self):
        raise OnExitNotSupportedInDeadState

    @on_exit.setter
    def on_exit(self, value):
        # We need the below check to allow the parent class (State) set on_exit to None
        if value:
            raise OnExitNotSupportedInDeadState
