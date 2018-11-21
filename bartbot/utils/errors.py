
import logging
import json
import wrapt


def handle_request_error(response: dict) -> bool:
    """
    Returns True if no error and False if error.
    Handles error and outputs to logs.
    """

    logging.debug(f"Response: {json.dumps(response,indent=2)}")

    if 'error' in response:
        # TODO: More apecific responses
        return False
    else:
        return True


def print_traceback(error):
    import os
    import sys
    import traceback
    exc_type, _, exc_tb = sys.exc_info()
    traceback.print_tb(exc_tb)
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    logging.debug(
        f"Error: {error}. Error info: {exc_type}, {fname}, {exc_tb.tb_lineno}")
    print(
        f"Error: {error}. Error info: {exc_type}, {fname}, {exc_tb.tb_lineno}")


@wrapt.decorator
def catch_here(wrapped, instance, args, kwargs):
    try:
        return wrapped(*args, **kwargs)
    except Exception as e:
        print_traceback(e)
