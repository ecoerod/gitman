#! /usr/bin/env python3

import os
from sys import argv
from git_functions import git_list, git_setup, git_help


if not os.path.exists(os.path.join(os.environ["HOME"], '.gitman')):
    # print("Doesn't exist")
    git_setup()
else:
    with open(os.path.join(os.environ['HOME'], '.gitman'), 'r') as cf:
        GIT_TOKEN = cf.readline()

VALID_ARGS = {
    'list': git_list,
    'setup': git_setup,
}

if len(argv) >= 2:
    try:
        VALID_ARGS[argv[1]](GIT_TOKEN, argv[2:])
    except IndexError:
        VALID_ARGS[argv[1]](GIT_TOKEN, [])
    except ValueError:
        git_help()
