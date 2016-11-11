import requests
import json
import os

def api_call(method, token=None):
    if token:
        token = {'Authorization': 'token {}'.format(token)}
    data = requests.get('https://api.github.com/{}'.format(method),
                        headers=token).content
    return json.loads(data.decode('utf-8'))


def git_list(token, argv):
    repos_data = api_call('user/repos', token=token)
    print('Repositories for user: {}'.format(repos_data[0]['owner']['login']))
    for repo in repos_data:
        print('* {} - {}'.format(repo['full_name'], repo['description']))


def git_setup():
    with open(os.path.join(os.environ['HOME'], ".gitman"), "w") as cf:
        print('Please provide your Github OAuth token with "repos" permission.')
        token = input('Github OAuth token: ')
        cf.write(token)


def git_help():
    raise NotImplementedError
