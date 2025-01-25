class APIError(Exception):
    """Base exception for API errors"""
    pass

class WalletAlreadyRegisteredError(APIError):
    """Raised when attempting to register an already registered wallet"""
    pass

class InvalidWalletError(APIError):
    """Raised when wallet address is invalid"""
    pass 