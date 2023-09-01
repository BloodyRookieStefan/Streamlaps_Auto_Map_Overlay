############################################################################
# Progam state machine
# Date: 01.09.2023
############################################################################

from enum import Enum

# Definition of state machine states
class States(Enum):
    INIT = 1
    LOCKED = 2
    RELEASED = 3

# Definition of state machine commands
class Commands(Enum):
    LOCK = 1
    RELEASE = 2

class CStateMachine:

    State = States.INIT                 # Current state
    Transitions = dict()                # State machine transitions

    def __init__(self) -> None:
        # Set transitions
        self.Transitions[States.INIT]       = {Commands.RELEASE : States.RELEASED}
        self.Transitions[States.LOCKED]     = {Commands.RELEASE : States.RELEASED}
        self.Transitions[States.RELEASED]   = {Commands.LOCK : States.LOCKED}

    def moveNext(self, command):
        # Check if current state has valid transitions
        if self.State not in self.Transitions:
            raise ValueError(f'Invalid transition: No transition available for "{self.State}"')
        # Get all possible transitions
        possibleTransitions = self.Transitions[self.State]
        # Check if command is in transitions
        if command not in possibleTransitions:
            raise ValueError(f'Invalid transition: "{self.State}" does not have transition "{command}"')
        # Set new state
        self.State = possibleTransitions[command]

    def getCurrentState(self):
        return self.State

SM = CStateMachine()