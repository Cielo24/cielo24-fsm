# encoding: utf-8

import json
from fsm import FSM

class FSMEncoder(json.JSONEncoder):
    """
    To be able to reconstruct the FSM we need to retain:
    States, transitions, initial state and dead state.
    """

    def default(self, o):
        assert isinstance(o, FSM), 'Invalid argument type'
        json_out = {'states': o._states,
                    'transitions': o._transitions,
                    'initial_state_id': o.initial_state.id,
                    'dead_state': o.dead_state}
        return json_out

class FSMDecoder(json.JSONDecoder):
    """
    To be able to reconstruct the FSM we need to retain:
    States, transitions, initial state and dead state.
    """

    def default(self, o):
        assert isinstance(o, FSM), 'Invalid argument type'
        json_out = {'states': o._states,
                    'transitions': o._transitions,
                    'initial_state_id': o.initial_state.id,
                    'dead_state': o.dead_state}
        return json_out
