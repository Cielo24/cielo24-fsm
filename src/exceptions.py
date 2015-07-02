# encoding: utf-8

class FSMException(Exception):
    pass

class EmptySetOfStates(FSMException):
    pass

class EmptySetOfTransitions(FSMException):
    pass

class NoFinalState(FSMException):
    pass

class NoInitialState(FSMException):
    pass

class MissingTransitions(FSMException):
    pass

class DisconnectedState(FSMException):
    pass

class UnknownSymbol(FSMException):
    pass

class DuplicateState(FSMException):
    pass

class DuplicateTransition(FSMException):
    pass

class OnExitNotSupportedInDeadState(FSMException):
    pass

class OnlyOneDeadStatePerFSMAllowed(FSMException):
    pass

class ValidationRequired(FSMException):
    pass

class TransitionContainsUnknownState(FSMException):
    pass

class CannotModifyStateThatIsCurrent(FSMException):
    pass

class StateCannotHaveSameSymbolTransitions(FSMException):
    pass
