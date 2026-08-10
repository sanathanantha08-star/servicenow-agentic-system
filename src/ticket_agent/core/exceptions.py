

class TicketAgentError(Exception):
    """Base class for exceptions in the Ticket Agent."""
    pass

class RetryableError(TicketAgentError):
    """Exception raised for errors that can be retried."""
    pass

class FatalError(TicketAgentError):
    """Exception raised for errors that cannot be recovered from."""
    pass

class ServiceNowAuthError(FatalError):
    """Exception raised for errors related to ServiceNow API interactions."""
    pass

class InvalidInputError(FatalError):
    """Exception raised for invalid input data."""
    pass

class ServiceNowTimeoutError(RetryableError):
    """Exception raised for timeout errors when interacting with ServiceNow API."""
    pass

class MongoDBConnectionError(RetryableError):
    """Exception raised for errors related to MongoDB connection issues."""
    pass

class LLMServiceError(RetryableError):
    """Exception raised for errors related to LLM service interactions."""
    pass

class LLMServiceTimeoutError(RetryableError):
    """Exception raised for timeout errors when interacting with LLM service."""
    pass