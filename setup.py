from setuptools import setup
from setuptools.command.test import test as TestCommand
import sys

class Tox(TestCommand):
    user_options = [('tox-args=', 'a', "Arguments to pass to tox")]
    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.tox_args = None
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True
    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import tox
        import shlex
        errno = tox.cmdline(args=shlex.split(self.tox_args))
        sys.exit(errno)

setup(
    name = "adbpy",
    version = "0.1.2",
    url = "https://github.com/noahgoldman/adbpy",
    license = "MIT",
    author = "Noah Goldman",
    author_email = "noah@phaaze.com",
    description = "A library to communicate with ADB through it's "
                  "internal socket interface, rather than the command"
                  "line.",
    platforms = "any",
    packages = ["adbpy"],
    zip_safe = True,
    tests_require = ['tox'],
    cmdclass = {'test': Tox}, 
)
