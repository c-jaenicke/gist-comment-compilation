import requests
import json
import os
from datetime import datetime

# pip install python-dotenv
from dotenv import load_dotenv

# load env file
load_dotenv(".env")

PAT_TOKEN = os.environ.get("PAT_TOKEN")
GIST_ID = os.environ.get("GIST_ID")
GIST_NAME = os.environ.get("GIST_NAME")
KEYWORD = os.environ.get("KEYWORD")


def add_comments(comments):
    """MODIFY THIS FUNCTION

    Iterates through the comments of the gist
    if the user of the comment is authorized
        split the comment content into lines
        if the comment starts with the keyword
            try to get all needed attributes
                if yes, insert new comment into gist
                if not, dont insert new comment into gist
        if not, dont check further
    if not, dont insert new comment into gist"""

    file = open("gist.md", "a")
    users = get_auth_users()

    # iterate through all comments
    for comment in comments:
        # check if user is authorized
        if (comment["user"]["login"] in users):
            contentString = comment["body"]
            # check if comment starts with keyword
            # change length of content string excerpt when changing keyword
            if (contentString[:6] == KEYWORD):
                try:
                    file.write("\n\rWritten by: {0} on the {1}".format(comment["user"]["login"], (comment["updated_at"].replace("T", " at ").replace("Z", " UTC"))))
                    file.write("{0}".format(contentString[6:]))
                    file.write("\n\r---")
                    print("Adding comment\n\tusername {0}\n\tcomment id: {1}".format(comment["user"]["login"], comment["id"]))

                except:
                    print("Invalid comment detected, missing an attribute\n\t comment id: {0}".format(comment["id"]))

    file.close()


def get_comments():
    """Gets comment of th gist

    Returns: json object of the response, containing an array of all comments"""

    urlBase = "https://api.github.com/gists/{0}/comments".format(GIST_ID)
    headers = {"Accept": "application/vnd.github+json",
               "Authorization": "token {0}".format(PAT_TOKEN)
               }

    try:
        resp = requests.get(urlBase, headers=headers)
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.HTTPError as error:
        print(error)
        raise


def prepare_file():
    """Creates or resets the gist file that will be pushed, based on th preset.md provided"""

    writeFile = open("gist.md", "w")
    readFile = open("preset.md", "r")
    content = readFile.read()
    writeFile.write(content)
    writeFile.close()
    readFile.close()


def post_update_gist():
    """Post the updated gist"""

    file = open("gist.md", "r")
    changes = file.read()
    file.close()

    urlBase = "https://api.github.com/gists/{0}".format(GIST_ID)

    # set headers
    headers = {"Accept": "application/vnd.github+json",
               "Authorization": "token {0}".format(PAT_TOKEN)
               }

    # create data payload
    data = {"public": True,
            "files": {
                "DynamicTest-FullMarkdown.md": {
                    "content": "changes"
                }
            }
            }

    # change values to actual data that needs to be send
    data["files"] = {GIST_NAME: {"content": str(changes)}}
    data = json.dumps(data, sort_keys=False)

    try:
        resp = requests.post(urlBase, headers=headers, data=data)
        resp.raise_for_status()
        print("--- Successfully updated ---")
        return resp.json()
    except requests.exceptions.HTTPError as error:
        print("--- FAILED to update ---")
        print(error)
        raise


def get_auth_users():
    """get the list of authorized users

    Returns: an array of users"""
    with open("authorized-users.txt", "r") as file:
        users = file.read().splitlines()

    file.close()
    return users


if __name__ == "__main__":
    print(
        "\n--- Running {0}---".format(datetime.utcnow().strftime("%Y.%m.%d-%H:%M")))
    prepare_file()
    comments = get_comments()
    add_comments(comments)
    post_update_gist()
