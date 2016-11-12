import requests
import os

def api_call(method, token=None):
    if token:
        token = {'Authorization': 'token {}'.format(token)}
    data = requests.get('https://api.github.com/{}'.format(method),
                        headers=token)
    return data.status_code, data.json()


def git_list(token, args):

    if args.user:
        status_code, repos_data = api_call('users/{}/repos'.format(args.user))
    else:
        status_code, repos_data = api_call('user/repos', token=token)

    if status_code == 200:
        print('Repositories for user: {}'.format(repos_data[0]['owner']['login']))
        for repo in repos_data:
            print('* {} - {}'.format(repo['full_name'], repo['description']))
    else:
        print('User "{}" not found'.format(args.user))


def git_setup(*args, **kwargs):
    with open(os.path.join(os.environ['HOME'], ".gitman"), "w") as cf:
        print('Please provide your Github OAuth token with "repos" permission.')
        token = input('Github OAuth token: ')
        cf.write(token)

