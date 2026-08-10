


from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential
from src.ticket_agent.core.exceptions import RetryableError

from src.ticket_agent.config import Settings 

def retryable():


    return retry(
        stop=stop_after_attempt(Settings().app.max_retries),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type( RetryableError),
    )