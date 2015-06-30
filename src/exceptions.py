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

class InitialStateNotInSetOfStates(FSMException):
    pass

class MissingTransitions(FSMException):
    pass

class DisconnectedState(FSMException):
    pass

class UnknownSymbol(FSMException):
    pass

class DuplicateState(FSMException):
    pass

class DeadStateDisabled(FSMException):
    pass

class ImpossibleToDisableDeadState(FSMException):
    pass

class OnExitNoSupportedInDeadState(FSMException):
    pass

class SourceStateCannotBeDead(FSMException):
    pass

class OnlyOneDeadStatePerFSMAllowed(FSMException):
    pass

class ValidationRequired(FSMException):
    pass

class TransitionContainsUnknownState(FSMException):
    pass
