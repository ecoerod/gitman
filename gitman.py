#! /usr/bin/env python3

import os
import argparse
from git_functions import git_list, git_setup


if not os.path.exists(os.path.join(os.environ['HOME'], '.gitman')):
    # print("Doesn't exist")
    git_setup()
else:
    with open(os.path.join(os.environ['HOME'], '.gitman'), 'r') as cf:
        GIT_TOKEN = cf.readline()

VALID_ARGS = {
    'list': git_list,
    'setup': git_setup,
}

parser = argparse.ArgumentParser(description='Gitman - Github repository manager')
parser.add_argument('method', help='Action to take.', choices=VALID_ARGS.keys())

args = parser.parse_args()

try:
    VALID_ARGS[args.method](GIT_TOKEN, args)
except:
    parser.print_usage()
