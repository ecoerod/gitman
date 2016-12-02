import requests
import os
import locale
#import locales
from importlib import import_module
from subprocess import call


def _localization():
    try:
        locale.setlocale(locale.LC_ALL, "")
        return import_module(".locales.{}".format(locale.getlocale()[0]),
                             package="gitman")
    except ImportError:
        return import_module(".locales.us_EN", package="gitman")

loc = _localization()


def api_call(method, token=None):
    '''Sends an api call to github.com and returns the json contained.

    Args:
        method (str): Represents the URI to query for data.
        token (str or None): If provided, provides authorization for queries.

    Returns:
        tuple: Status code of the query and the json contained in the response.
    '''

    if token:
        token = {'Authorization': 'token {}'.format(token)}
    data = requests.get('https://api.github.com/{}'.format(method),
                        headers=token)
    return data.status_code, data.json()


def git_list(token, args):
    '''Lists the repositories of a user.

    Args:
        token (str): To provide authorization for the call if needed.
        args (argparse.Namespace): For optional arguments.

    Outputs:
        The list of the repositories belonging to the user to stdin.

    Returns:
        nothing
    '''

    if args.user:
        status_code, repos_data = api_call('users/{}/repos'.format(args.user))
    else:
        status_code, repos_data = api_call('user/repos', token=token)

    if status_code == 200:
        print(loc.LIST_USERNAME.format(repos_data[0]['owner']['login']))
        for repo in repos_data:
            print('* {} - {}'.format(repo['full_name'], repo['description']))
    else:
        print(loc.LIST_NOTFOUND.format(args.user))


def git_setup(*args, **kwargs):
    '''Stores the token provided by the user for future use.

    Args:
        nothing. *args and **kwargs for simplicity of code in gitman.py

    Inputs:
        A string from stdout representing the Github OAuth token of the caller.
        Required at least the "repos" permission, for now.

    Outputs:
        A file ".gitman" on the $HOME of the user containing this token string.

    TODO:
        - Maybe allow the user to delete his own repositories if given a valid
        token.
    '''
    with open(os.path.join(os.environ['HOME'], ".gitman"), "w") as cf:
        print(loc.SETUP_INSTRUCTIONS)
        token = input(loc.SETUP_INPUT)
        cf.write(token)


def git_clone(token, args):
    '''Clones a given repository.

    Args:
        token (str): Always passed by the main software, serves to identify the
                     user in case it is not specified in the repo name.
        args (argparse.Namespace): Contains the repo name as as argument passed
                                   in the CLI.
    Outputs:
        Calls 'git' and clones the specified repository in the CWD.

    '''
    repo = args.repo
    if len(args.repo.split('/')) == 1:
        _, user_data = api_call("user", token)
        repo = "{}/{}".format(user_data['login'], repo)
    try:
        call(['git', 'clone', 'https://github.com/{}'.format(repo)])
    except FileNotFoundError:
        print(loc.CLONE_NOTFOUND)
