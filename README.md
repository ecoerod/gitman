# Gitman - Github repository handler

## Requirements
- Python 3.x
- pip
- Github OAuth authentication token with the `repos` flag enabled (for actions that require user authentication)

## Installation
`pip install github-manager` (different name for conflict reasons)

## Usage
Gitman currently provides four commands:
- `setup`: Creates an authentication token file in the users $HOME. Subject to change.
- `list`: Lists the repositories of a user, either specified with the `--user` flag or defaulting to the authenticated user.
- `clone`: Clones a specified repository (formatted `<user>/<repo>`, defaulting to the authenticated user if `<user>/` not present) in the current working directory.
- `fork`: Forks a specified repository (formattes `<user>/<repo>`) for the authenticated user.

## TODO
- Create repo functionality
- (Maybe) delete repo functionality. Figuring out how to safely implement this.

## License
This project is licensed under the terms of the MIT license (see LICENSE.md for further details).
