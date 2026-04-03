class AgneticPoolError(Exception):
    """Base exception for AgneticPool SDK"""
    pass


class AuthenticationError(AgneticPoolError):
    """Authentication failed"""
    pass


class APIError(AgneticPoolError):
    """API request failed"""
    def __init__(self, message: str, code: str = None, details: dict = None):
        super().__init__(message)
        self.code = code
        self.details = details
