#! /usr/bin/env python3

'''Gitman - Github repository manager

Allows users control his own repositories in Github.org and operate on others
easily.

Methods available:
    list - lists the repositories of the users
    setup - creates (or modifies) the Github OAuth token used by the program
    clone - clones a specified repository

Examples:
    $ python gitman.py list
    $ python gitman.py list -u Nelthorim

TODO:
    - Create repository functionality.
'''


import os
import argparse
import gitman
from gitman.gitman import git_list, git_setup, git_clone, loc


def main():
    if not os.path.exists(os.path.join(os.environ['HOME'], '.gitman')):
        git_setup()
    else:
        with open(os.path.join(os.environ['HOME'], '.gitman'), 'r') as cf:
            GIT_TOKEN = cf.readline()

    # Setup main parser
    parser = argparse.ArgumentParser(description=loc.DESCRIPTION)
    subparser = parser.add_subparsers(dest="method")

    # 'list' method
    list_parser = subparser.add_parser('list', help=loc.LIST_HELP,
                                       description=loc.LIST_DESCRIPTION)
    list_parser.add_argument('-u', '--user', help=loc.LIST_USER_HELP)

    # 'setup' method
    setup_parser = subparser.add_parser('setup', help=loc.SETUP_HELP)

    # 'clone' parser
    clone_parser = subparser.add_parser('clone', help=loc.CLONE_HELP,
                                        description=loc.CLONE_DESCRIPTION)
    clone_parser.add_argument('repo', help=loc.CLONE_REPO_HELP) 

    # MAIN PROGRAM
    args = parser.parse_args()

    VALID_ARGS = {
        'list': git_list,
        'setup': git_setup,
        'clone': git_clone
    }

    try:
        VALID_ARGS[args.method](GIT_TOKEN, args)
    except Exception as e:
        parser.print_usage()
