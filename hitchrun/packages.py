from path import Path
from commandlib import Command, CommandError
import sys
import os


def hvenv():
    """Get Hvenv folder."""
    return Path(sys.executable).joinpath("..", "..").abspath()


def keypath():
    """Get the project directory by working backwards from the virtualenv python."""
    assert hvenv().joinpath("linkfile").exists()
    assert Path(hvenv().joinpath("linkfile").bytes().decode("utf8").strip()).exists()
    return Path(hvenv().joinpath("linkfile").bytes().decode("utf8").strip())


def frozenreqs():
    """
    Path to frozenreqs file.

    This is a copy of hitchreqs.txt that is taken every time an installation
    is done to use to check for changes.
    """
    return Path(hvenv().joinpath("frozenreqs.txt"))


def hitchreqsin():
    """
    Path to hitchreqs.in file.
    """
    return keypath().joinpath("hitchreqs.in")


def hitchreqstxt():
    """
    Path to hitchreqs.txt file.
    """
    return keypath().joinpath("hitchreqs.txt")


def compile_hitchreqs_in():
    """
    Run hitchreqs_in.
    """
    Command(hvenv().joinpath("bin", "pip-compile"))(
        "--no-header",
        "--output-file", "hitchreqs.txt",
        "hitchreqs.in"
    ).in_dir(keypath()).run()
    print("Compiled new hitchreqs.txt")


def ensure_hitchreqs_synced():
    """
    Check packages installed are in sync with what is in hitchreqs.txt.

    If not, run pip-sync and re-run this command.
    """
    if frozenreqs().exists():
        if frozenreqs().bytes().decode("utf8") == keypath().joinpath("hitchreqs.txt").bytes().decode('utf8'):
            return

    if hitchreqsin().exists() and not hitchreqstxt().exists():
        Command(hvenv().joinpath("bin", "pip-compile"))("hitchreqs.in").in_dir(keypath()).run()

    try:
        Command(hvenv().joinpath("bin", "pip-sync"))("hitchreqs.txt").in_dir(keypath()).run()
    except CommandError:
        print("Error installing from hitchreqs.txt")
        sys.exit(1)
    keypath().joinpath("hitchreqs.txt").copy(frozenreqs())
    os.execvp(sys.argv[0], sys.argv)
