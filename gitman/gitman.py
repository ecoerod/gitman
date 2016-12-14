import requests
import os
import locale
import click
import json
from sys import exit
from importlib import import_module
from subprocess import call


# HELPER FUNCTIONS
def _localization():
    '''Returns a module object containing all the help strings according to the
       locale of the user'''
    try:
        locale.setlocale(locale.LC_ALL, "")
        return import_module(".locales.{}".format(locale.getlocale()[0]),
                             package="gitman")
    except ImportError:
        return import_module(".locales.en_US", package="gitman")


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
    try:
        return data.status_code, data.json()
    except json.decoder.JSONDecodeError:
        print(loc.API_ERROR)
        exit(1)
# END HELPER FUNCTIONS


@click.group(help=loc.DESCRIPTION)
@click.pass_context
def main(ctx):
    '''Entry point.'''
    if not os.path.exists(os.path.join(os.environ['HOME'], '.gitman')):
        git_setup()

    with open(os.path.join(os.environ['HOME'], '.gitman'), 'r') as cf:
        ctx.obj = cf.readline()


@main.command(name='list', help=loc.LIST_HELP)
@click.pass_obj
@click.option('-u', '--user', help=loc.USER_HELP,
              default=None)
def git_list(token, user):
    '''Lists the repositories of a user.

    Args:
        token (str): To provide authorization for the call if needed.
        user (str): User to target in Github.

    Outputs:
        The list of the repositories belonging to the user to stdin.'''
    if user:
        status_code, repos_data = api_call('users/{}/repos'.format(user))
    else:
        status_code, repos_data = api_call('user/repos', token=token)

    if status_code == 200:
        print(loc.LIST_USERNAME.format(repos_data[0]['owner']['login']))
        for repo in repos_data:
            print('* {} - {}'.format(repo['full_name'], repo['description']))
    else:
        print(loc.LIST_NOTFOUND.format(user))


@main.command(name='setup', help=loc.SETUP_HELP)
def git_setup():
    '''Stores the token provided by the user for future use.

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
        if not token.isspace():
            cf.write(token)
        else:
            print(loc.SETUP_CANCEL)


@main.command(name='clone', help=loc.CLONE_HELP)
@click.pass_obj
@click.argument('repo')
@click.option('-u', '--user', help=loc.USER_HELP)
def git_clone(token, repo, user):
    '''Clones a given repository.

    Args:
        token (str): Always passed by the main software, serves to identify the
                     user in case it is not specified in the repo name.
        repo (str): Name of the repository to clone, in the format
                    <username?>/<repo_name>.

    Outputs:
        Calls 'git' and clones the specified repository in the CWD.

    '''
    if len(repo.split('/')) == 1:
        _, user_data = api_call("user", token)
        repo = "{}/{}".format(user_data['login'], repo)
    try:
        call(['git', 'clone', 'https://github.com/{}'.format(repo)])
    except FileNotFoundError:
        print(loc.CLONE_NOTFOUND)


if __name__ == "__main__":
    main()
