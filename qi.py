#
# QI - Qwantinuous Integration
#
import sys
import re
import subprocess
import os
sys.path.append('afp-backend')


def read_file(filename): 
    with open(filename, 'r') as file:
        return file.read()


def write_file(filename, contents):
    with open(filename, 'w') as file:
        file.write(contents)


def patch_file(filename, f):
    contents = read_file(filename)
    new_contents = f(contents)
    write_file(filename, new_contents)


def is_valid_version(version):
    return re.match(r'\d+\.\d+\.\d+',version)


def fail_with(reason):
    print(reason)
    exit(1)


def run_pipeline(*tasks):
    for task in tasks:
        if task() != 0: fail_with('Releasing failed')


def chdir(dir):
    return ChDirTask(dir)


def task(*cmdline):
    return Task(*cmdline)


class ChDirTask:
    def __init__(self, dir):
        self.dir = dir

    def __call__(self) -> int:
        try:
            os.chdir(self.dir)
            return 0
        except OSError as e:
            print(e)
            return 1


class Task:
    def __init__(self, *cmdline):
        self.cmdline = cmdline

    def __call__(self):
        print("running {}".format(self.cmdline))
        return subprocess.call(self.cmdline)    
