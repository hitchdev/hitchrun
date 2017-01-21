import datetime
from hitchrun import cwd, Path

keypath = Path(__file__).abspath()


def humantime():
    """Use a library."""
    import humanize
    print(humanize.naturaltime(datetime.datetime.now()))


def hitch(*args):
    """
    Run a hitch maintenance command.
    """
    from hitchrun import hitch_maintenance
    hitch_maintenance(*args)
