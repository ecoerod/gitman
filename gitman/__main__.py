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
    - Extract help strings for the parser into locale files.
'''


import os
import argparse
from gitman import git_list, git_setup, git_clone


def main():
    if not os.path.exists(os.path.join(os.environ['HOME'], '.gitman')):
        git_setup()
    else:
        with open(os.path.join(os.environ['HOME'], '.gitman'), 'r') as cf:
            GIT_TOKEN = cf.readline()


    # Setup main parser
    parser = argparse.ArgumentParser(description='Gitman - Github repository manager')
    subparser = parser.add_subparsers(dest="method")

    # 'list' method
    list_parser = subparser.add_parser('list', help='List the repositories of the user.',
                                       description='Gitman - List: list the repositories of the user')
    list_parser.add_argument('-u', '--user',
                             help='Targets a user in Github. Default: user configured by setup')

    # 'setup' method
    setup_parser = subparser.add_parser('setup', help='Setup user credentials.')

    # 'clone' parser
    clone_parser = subparser.add_parser('clone', help='Clones the specified repository.',
                                        description='Gitman - Clone: clones the specified repository.')
    clone_parser.add_argument('repo', help='Repository to clone in the format <user>/<repo>. Defaults to the authenticated user if no <user> specified.') 

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
