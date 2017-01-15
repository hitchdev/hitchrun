import humanize
import datetime


def commanda():
    """Command A help.
    """
    print("Command A ran")


def commandb():
    """Command B help.
    """
    print("Command B ran")


def commandvar1(variable1):
    print("Command {0}".format(variable1))


def humantime():
    """Use a library."""
    print(humanize.naturaltime(datetime.datetime.now()))
