# This file contains the definition for all custom exceptions in Tuprware Node.

# This is the parent exception for all custom exceptions in Tuprware Node
class TuprwareNodeException(Exception):
    def __init__(self, error_message='Bad request.'):
        super().__init__(error_message)

# Custom exceptions
class InvalidChallengeIDException(TuprwareNodeException):
    def __init__(self):
        super().__init__('Invalid Challenge ID.')

class NoChallengeToStopException(TuprwareNodeException):
    def __init__(self):
        super().__init__('There is no challenge to stop.')

class NoChallengeToRestartException(TuprwareNodeException):
    def __init__(self):
        super().__init__('There is no challenge to restart.')

class ChallengeAlreadyRunningException(TuprwareNodeException):
    def __init__(self):
        super().__init__('This challenge is already running. To restart it, use /restart-challenge.')