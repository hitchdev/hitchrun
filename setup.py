# -*- coding: utf-8 -*
from setuptools.command.install import install
from setuptools import find_packages
from setuptools import setup
from sys import version_info, stderr, exit
import codecs
import sys
import os


if sys.platform == "win32" or sys.platform == "cygwin":
    stderr.write("Hitch will not work on Windows. Sorry.\n")
    exit(1)


if version_info[0] == 2:
    stderr.write("HitchRun will not run in python 2.\n")
    exit(1)


if version_info[0] == 3:
    if version_info[1] < 3:
        stderr.write("HitchRun will not run on versions 3.0.x, 3.1.x or 3.2.x.\n")
        exit(1)


def read(*parts):
    # intentionally *not* adding an encoding option to open
    # see here: https://github.com/pypa/virtualenv/issues/201#issuecomment-3145690
    return codecs.open(os.path.join(os.path.abspath(os.path.dirname(__file__)), *parts), 'r').read()


setup(name="hitchrun",
    version=read('VERSION').replace('\n', ''),
    description="HitchRun - environment set up and command runner for hitchdev framework.",
    long_description=read('README.rst'),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
        'Topic :: Software Development :: Quality Assurance',
        'Topic :: Software Development :: Testing',
        'Topic :: Software Development :: Libraries',
        'Operating System :: Unix',
        'Environment :: Console',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='hitch development environment command line',
    author='Colm O\'Connor',
    author_email='colm.oconnor.github@gmail.com',
    url='https://github.com/hitchtest/hitchrun',
    license='AGPL',
    install_requires=[
        "click",
        "argcomplete>=0.8.1",
        "path.py",
        "commandlib",
        "hitch-pip-tools",
        "pip>=8.0",
        "prettystack>=0.2.6",
        "colorama",
    ],
    packages=find_packages(exclude=["docs", ]),
    package_data={},
    entry_points=dict(console_scripts=['hitchrun=hitchrun:commandline.run',]),
    zip_safe=False,
    include_package_data=True,
)
