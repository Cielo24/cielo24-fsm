# encoding: utf-8
from __future__ import unicode_literals

import json
from fsm import FSM

class FSMEncoder(json.JSONEncoder):
    """
    To be able to reconstruct the FSM we need to retain:
    States, transitions, initial state and dead state.
    """

    def default(self, o):
        assert isinstance(o, FSM), 'Invalid argument type'
        pass
