from subprocess import call
from os import path
from commandlib import run, Command
import hitchpython
import hitchserve
from hitchstory import StoryCollection, StorySchema, BaseEngine, exceptions, validate
from hitchrun import expected
from path import Path
import strictyaml
from strictyaml import MapPattern, Str, Seq, Map
from pathquery import pathq
import hitchtest
import hitchdoc

from simex import DefaultSimex
from hitchrun import genpath, hitch_maintenance
from commandlib import python

from engine import Engine


@expected(strictyaml.exceptions.YAMLValidationError)
@expected(exceptions.HitchStoryException)
def test(*words):
    """
    Run test with words.
    """
    print(
        StoryCollection(
            pathq(Path(KEYDIR)).ext("story"), Engine(Path(KEYDIR), {"overwrite artefacts": True})
        ).shortcut(*words).play().report()
    )


def ci():
    """
    Continuos integration - run all tests and linter.
    """
    #lint()
    print(
        StoryCollection(
            pathq(Path(KEYDIR)).ext("story"), Engine(Path(KEYDIR), {})
        ).ordered_by_name().play().report()
    )


def lint():
    """
    Lint all code.
    """
    python("-m", "flake8")(
        Path(KEYDIR).parent.joinpath("hitchrun"),
        "--max-line-length=100",
        "--exclude=__init__.py",
    ).run()
    python("-m", "flake8")(
        Path(KEYDIR).joinpath("key.py"),
        "--max-line-length=100",
        "--exclude=__init__.py",
    ).run()
    print("Lint success!")


def hitch(*args):
    """
    Use 'h hitch --help' to get help on these commands.
    """
    hitch_maintenance(*args)


def deploy(version):
    """
    Deploy to pypi as specified version.
    """
    git = Command("git").in_dir(DIR.project)
    version_file = DIR.project.joinpath("VERSION")
    old_version = version_file.bytes().decode('utf8')
    if version_file.bytes().decode("utf8") != version:
        DIR.project.joinpath("VERSION").write_text(version)
        git("add", "VERSION").run()
        git("commit", "-m", "RELEASE: Version {0} -> {1}".format(
            old_version,
            version
        )).run()
        git("push").run()
        git("tag", "-a", version, "-m", "Version {0}".format(version)).run()
        git("push", "origin", version).run()
    else:
        git("push").run()
    python("setup.py", "sdist").in_dir(DIR.project).run()
    python(
        "-m", "twine", "upload", "dist/strictyaml-{0}.tar.gz".format(version)
    ).in_dir(DIR.project).run()


def docgen():
    """
    Generate documentation.
    """
    docpath = Path(KEYDIR).parent.joinpath("docs")

    if not docpath.exists():
        docpath.mkdir()

    documentation = hitchdoc.Documentation(
        genpath.joinpath('storydb.sqlite'),
        'doctemplates.yml'
    )

    for story in documentation.stories:
        story.write(
            "rst",
            docpath.joinpath("{0}.rst".format(story.slug))
        )
