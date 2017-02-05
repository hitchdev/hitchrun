from functools import wraps
import colorama
import sys


def expected(exception_class):
    def wrapper(method):
        @wraps(method)
        def with_exception_handling(*args, **kwargs):
            try:
                return method(*args, **kwargs)
            except exception_class as error:
                sys.stderr.write(
                    "{red}{bright}{exc_type}{reset}\n\n{red}{message}{reset}\n".format(
                        red=colorama.Fore.RED,
                        bright=colorama.Style.BRIGHT,
                        exc_type=type(error).__name__,
                        reset=colorama.Style.RESET_ALL,
                        message=str(error),
                    )
                )
                return 1
        return with_exception_handling
    return wrapper


def ignore_ctrlc(method):
    method.ignore_ctrl_c = True
    return method
