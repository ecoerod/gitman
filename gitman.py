import requests
from sys import argv
import os

if not os.path.exists(os.path.join(os.environ["HOME"], ".gitman")):
    # print("Doesn't exist")
    git_setup()

VALID_ARGS = {
    "list": git_list,
    "setup": git_setup,
}

if len(argv) >= 2:
    try:
        VALID_ARGS[argv[1]]()
    except ValueError:
        print("Unknown command.")
