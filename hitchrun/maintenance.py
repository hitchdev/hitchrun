from hitchrun import packages


def hitch_maintenance(*args):
    """
    Runs general maintenance commands.
    """
    if args[0] == "compilereqs":
        packages.compile_hitchreqs_in()
