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


parser = argparse.ArgumentParser(description='Gitman - Github repository manager')
subparser = parser.add_subparsers(dest="method")

list_parser = subparser.add_parser('list', help="List the repositories of the user.",
                                   description="Gitman - List: list the repositories of the user")

setup_parser = subparser.add_parser('setup', help="Setup user credentials.")

args = parser.parse_args()

VALID_ARGS = {
    'list': git_list,
    'setup': git_setup
}

try:
    VALID_ARGS[args.method](GIT_TOKEN, args)
except:
    parser.print_usage()
