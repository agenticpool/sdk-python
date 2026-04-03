class AgenticPoolError(Exception):
    """Base exception for AgenticPool SDK"""
    pass


class AuthenticationError(AgenticPoolError):
    """Authentication failed"""
    pass


class APIError(AgenticPoolError):
    """API request failed"""
    def __init__(self, message: str, code: str = None, details: dict = None):
        super().__init__(message)
        self.code = code
        self.details = details
