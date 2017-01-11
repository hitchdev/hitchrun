"""High level command line interface to hitchrun."""
#from __future__ import print_function
import os
import sys
from hitchrun import key_file
import argcomplete
import argparse
import sys
import imp
from path import Path


def hvenv():
    """Get Hvenv folder."""
    return Path(sys.executable).joinpath("..", "..").abspath()


def linkfile():
    """Get the hitch directory by working backwards from the virtualenv python."""
    assert hvenv().joinpath("linkfile").exists()
    assert Path(hvenv().joinpath("linkfile").bytes().decode("utf8").strip()).exists()
    return Path(hvenv().joinpath("linkfile").bytes().decode("utf8").strip())



def run():
    """Run hitch bootstrap CLI"""
    parser = argparse.ArgumentParser(add_help=False, prefix_chars=[None, ])
    cc = key_file.KeyFile(imp.load_source("key", str(linkfile().joinpath("key.py"))))
    parser.add_argument("commands", nargs='*', default=None).completer = cc.command_completer
    argcomplete.autocomplete(parser)
    commands = parser.parse_args().commands

    returnval = 0

    if len(cc.commands) == 0:
        print("No commands found in {0}!".format(cc.hitchkey_file))
        sys.exit(1)

    if len(commands) == 0 or len(commands) == 1 and commands[0] in ['-h', '--help', 'help']:
        print("Usage: h command [args]\n")
        if cc.doc() is not None:
            print("%s\n" % cc.doc())
        print(cc.commands_help())
        print("Run 'h help [command]' to get more help on a particular command.")
    elif len(commands) > 1 and commands[0] in ['-h', '--help', 'help']:
        command = commands[1]
        if command in cc.command_list():
            print("Usage: h %s %s" % (command, cc.arg_help(command)))
            print()
            print(cc.commands[command]['helptext'])
        else:
            print("Command '{0}' not found in {1}. Type 'k help' to see a full list of commands.".format(command, cc.hitchkey_file))
    else:
        returnval = cc.run_command(commands[0], commands[1:])

    sys.exit(returnval)


if __name__ == '__main__':
    run()
