from hitchtest import monitor
from commandlib import run
from simex import DefaultSimex
from commandlib import Command
import hitchpython
import hitchserve
import hitchtest
import hitchvm
#import kaching
import time
from hitchvm import StandardBox, Vagrant
from path import Path
from pexpect import EOF
import sys
import hitchstory
from hitchrun import genpath
from strictyaml import Int
from hitchstory import validate


class Paths(object):
    def __init__(self, keypath):
        self.genpath = genpath
        self.keypath = keypath
        self.project = keypath.parent
        self.state = keypath.parent.joinpath("state")
        self.engine = keypath
        self.hitch = genpath


class Engine(hitchstory.BaseEngine):
    """Hitch bootstrap engine tester."""
    def __init__(self, keypath, settings):
        self.path = Paths(keypath)
        self.settings = settings


    def set_up(self):
        self.path.project = self.path.engine.parent
        self.path.state = self.path.engine.parent.joinpath("state")

        if self.path.state.exists():
            self.path.state.rmtree(ignore_errors=True)
        self.path.state.mkdir()

        box = StandardBox(Path("~/.hitchpkg").expand(), "ubuntu-trusty-64")
        self.vm = Vagrant("hitchrun", box, self.path.hitch)
        self.vm = self.vm.synced_with(self.path.project, "/hitchrun/")

        if not self.vm.snapshot_exists("ubuntu-1604-installed"):
            if not self.vm.snapshot_exists("ubuntu-1604-ready"):
                self.vm.up()
                self.long_run("sudo apt-get install python-setuptools -y")
                self.long_run("sudo apt-get install build-essential -y")
                self.long_run("sudo apt-get install python-pip -y")
                self.long_run("sudo apt-get install python-virtualenv -y")
                self.long_run("sudo apt-get install python3 -y")
                self.run("virtualenv --python python3 ~/hvenv")
                self.vm.take_snapshot("ubuntu-1604-ready")
                self.vm.halt()
            self.vm.restore_snapshot("ubuntu-1604-ready")
            self.vm.sync()
            self.long_run("~/hvenv/bin/pip install /hitchrun/")
            self.vm.take_snapshot("ubuntu-1604-installed")
            self.vm.halt()

        self.vm.restore_snapshot("ubuntu-1604-installed")

        for filename, contents in self.preconditions.get("files", {}).items():
            directory = self.path.project.joinpath("state", filename).dirname()
            if not directory.exists():
                directory.makedirs()
            self.path.project.joinpath("state", filename).write_text(contents)

        self.vm.sync()
        self.run("echo /hitchrun/state/{0} > /home/vagrant/hvenv/linkfile".format(
            self.preconditions.get("linkfile", "")
        ))
        self.run("/home/vagrant/hvenv/bin/pip uninstall hitchrun -y")
        self.run("/home/vagrant/hvenv/bin/pip install /hitchrun/")
        self.hitchrun("", exit_code=None)
        self.run("/home/vagrant/hvenv/bin/pip uninstall hitchrun -y")
        self.run("/home/vagrant/hvenv/bin/pip install /hitchrun/")


    def long_run(self, cmd):
        self.run(cmd=cmd, timeout=1500)

    def hitchrun(self, args="", expect=None, timeout=60, exit_code=0):
        self.run(
            "~/hvenv/bin/hitchrun " + args,
            expect=expect,
            timeout=timeout,
            exit_code=exit_code
        )

    @validate(exit_code=Int())
    def run(self, cmd=None, expect=None, timeout=60, exit_code=0):
        self.process = self.vm.cmd(cmd).pexpect()

        if sys.stdout.isatty():
            self.process.logfile = sys.stdout.buffer
        else:
            self.process.logfile = sys.stdout


        if expect is not None:
            self.process.expect(expect, timeout=timeout)
        self.process.expect(EOF, timeout=timeout)
        self.process.close()
        if exit_code is not None:
            assert int(self.process.exitstatus) == int(exit_code)

    def lint(self, args=None):
        """Lint the source code."""
        run(self.pip("install", "flake8"))
        run(self.python_package.cmd.flake8(*args).in_dir(self.path.project))

    def sleep(self, duration):
        """Sleep for specified duration."""
        time.sleep(int(duration))

    def placeholder(self):
        """Placeholder to add a new test."""
        pass

    def pause(self, message=""):
        self.ipython(message=message)

    def on_failure(self):
        #self.pause()
        pass

    def sshin(self):
        self.vm.cmd("bash").run()

    def on_success(self):
        """Ka-ching!"""
        if self.settings.get("kaching", False):
            kaching.win()
        if self.settings.get("pause_on_success", False):
            self.pause(message="SUCCESS")

    def tear_down(self):
        """Clean out the state directory."""
        if hasattr(self, 'vm'):
            if self.settings.get("destroy", False):
                self.vm.destroy()
            else:
                self.vm.halt()
