import functools
import time
import requests
import sys

# Simple retry decorator
def retry(retry_count=5, delay=5, allowed_exceptions=(requests.exceptions.RequestException)):
    def decorator(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            for r in range(retry_count):
                try:
                    return f(*args, **kwargs)
                except allowed_exceptions as e:
                    if r == retry_count-1:
                        print("Retry failed with %s" % str(e), file=sys.stderr)
                        raise
                    print("Request failed with %s" % str(e), file=sys.stderr)
                print("Wating for %s seconds before retrying again" % delay)
                time.sleep(delay)
        return wrapper
    return decorator
