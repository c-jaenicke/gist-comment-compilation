# Gist Comment Compilation Automation

Uses a codeword at the top of the comment to identify what should be added, and limits the addition to comments by authorized users.

## Setup

### Python

Required modules

- `os`
- `datetime`
- `requests`
- `json`
- `python-dotenv`

### .env

Create a `.env` file in the root directory, containing the following key pairs:

```text
PAT_TOKEN = <TOKEN HERE>
GIST_ID = <GIST ID HERE>
GIST_NAME = <GIST FILE NAME HERE>
KEYWORD  = <KEYWORD HERE>
```

| Variable  | Usage                                                                             |
| --------- | --------------------------------------------------------------------------------- |
| PAT_TOKEN | your personal GitHub access token to manage the gist. Only needs gist permissions |
| GIST_ID   | the gist that will be updated and has the comments                                |
| GIST_NAME | name of the actual file defined in the gist                                       |
| KEYWORD   | specify what the comments have to start with to be considered as an entry         |

### Adding Authorized Users

Add their GitHub login name to the `authorized-users.txt`.

**Each name in a new line.**

### Setting a preset Gist

The gist will be rewritten each time. This requires a pre made gist, to which the comments will be appended to.

Use the `preset.md` to set that gist.

### Parsing Comments

Edit the `add_comments` function in the `main.py` to parse the values you want, and how they should be added to the gist.

## Example

The code right now works for this gist [https://gist.github.com/c-jaenicke/3506d42d858a60098d63392180dca2cf](https://gist.github.com/c-jaenicke/3506d42d858a60098d63392180dca2cf)
