import functools
import time

# Simple retry decorator
def retry(retry_count=5, delay=5, allowed_exceptions=()):
    def decorator(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            for r in range(retry_count):
                try:
                    return f(*args, **kwargs)
                except allowed_exceptions as e:
                    if r == retry_count-1:
                        print("Retry failed with %s" % e)
                        raise
                    pass
                print("Waiting for %s seconds before retrying again" % delay)
                time.sleep(delay)
        return wrapper
    return decorator
