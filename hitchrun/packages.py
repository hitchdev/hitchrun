from path import Path
from commandlib import Command, CommandError
import sys
import os


class PathGroup(object):
    """Represent a group of file paths."""

    def __init__(self, **paths):
        """Create a group of paths."""
        for path_name, path_value in paths.items():
            setattr(self, path_name, path_value)

    def __setattr__(self, name, path):
        self.__dict__[name] = path


def paths():
    p = PathGroup(
        hvenv=Path(sys.executable).joinpath("..", "..").abspath(),
        gen=Path(sys.executable).joinpath("..", "..", "..").abspath(),
        key=Path(hvenv().joinpath("linkfile").bytes().decode("utf8").strip()),
    )
    p.hitchreqsin = p.key.joinpath("hitchreqs.in")
    p.hitchreqstxt = p.key.joinpath("hitchreqs.in")
    p.frozenreqstxt = p.hvenv.joinpath("frozenreqs.txt")
    p.frozenreqsin = p.hvenv.joinpath("frozenreqs.in")
    return p

def hvenv():
    """Get Hvenv folder."""
    return Path(sys.executable).joinpath("..", "..").abspath()


def keypath():
    """Get the project directory by working backwards from the virtualenv python."""
    assert hvenv().joinpath("linkfile").exists()
    assert Path(hvenv().joinpath("linkfile").bytes().decode("utf8").strip()).exists()
    return Path(hvenv().joinpath("linkfile").bytes().decode("utf8").strip())


def frozenreqstxt():
    """
    Path to frozenreqs file.

    This is a copy of hitchreqs.txt that is taken every time an installation
    is done to use to check for changes.
    """
    return Path(hvenv().joinpath("frozenreqs.txt"))


def frozenreqsin():
    """
    Path to frozenreqs file.

    This is a copy of hitchreqs.txt that is taken every time an installation
    is done to use to check for changes.
    """
    return Path(hvenv().joinpath("frozenreqs.in"))


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
    try:
        Command(hvenv().joinpath("bin", "pip-compile"))(
            "--no-header",
            "--output-file", "hitchreqs.txt",
            "hitchreqs.in"
        ).in_dir(keypath()).run()
        keypath().joinpath("hitchreqs.in").copy(frozenreqsin())
        print("Compiled new hitchreqs.txt")
    except CommandError:
        print("Error compiling hitchreqs.txt")
        sys.exit(1)


def pip_sync():
    try:
        Command(hvenv().joinpath("bin", "pip-sync"))("hitchreqs.txt").in_dir(keypath()).run()
        keypath().joinpath("hitchreqs.txt").copy(frozenreqstxt())
        print("Synced hitchreqs.in and hitchreqs.txt")
    except CommandError:
        print("Error installing from hitchreqs.txt")
        sys.exit(1)


def ensure_hitchreqs_synced():
    """
    Check packages installed are in sync with what is in hitchreqs.txt.

    If not, run pip-sync and re-run everything to ensure that everything is run
    with the correct packages installed.
    """
    trigger_rerun = False
    path = paths()

    if path.hitchreqsin.exists() and not path.hitchreqstxt.exists():
        print("hitchreqs.in must exist if hitchreqs.txt exists")
        sys.exit(1)

    if not path.hitchreqsin.exists() and not path.hitchreqstxt.exists():
        print("No hitchreqs.in or hitchreqs.txt exists, creating default")
        hitchreqsin().write_text("hitchrun\n")
        compile_hitchreqs_in()
        pip_sync()
        trigger_rerun = True


    if not path.frozenreqsin.exists() or not path.frozenreqstxt.exists():
        print("First run")
        compile_hitchreqs_in()
        trigger_rerun = True

    if frozenreqsin().bytes().decode('utf8') != keypath().joinpath("hitchreqs.in").bytes().decode('utf8'):
        print("hitchreqs.in changed, re-compiling hitchreqs.txt")
        compile_hitchreqs_in()
        trigger_rerun = True

    if not frozenreqstxt().exists() or \
        frozenreqstxt().bytes().decode("utf8") != keypath().joinpath("hitchreqs.txt").bytes().decode('utf8'):
        print("hitchreqs.txt changed, re-syncing packages")
        pip_sync()
        trigger_rerun = True

    if trigger_rerun:
        os.execvp(sys.argv[0], sys.argv)
