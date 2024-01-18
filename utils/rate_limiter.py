# rate_limiter.py
from ratelimit import limits, sleep_and_retry

CALLS = 5
RATE_LIMIT = 1

@sleep_and_retry
@limits(calls=CALLS, period=RATE_LIMIT)
def check_limit():
    ''' Empty function just to check for calls to API '''
    return
