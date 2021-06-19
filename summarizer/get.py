#!/usr/bin/env python

import re
import json
import gitlab
from cleantext import clean

project_id = 426
issue_id = 1413

with open("./data/secrets/secrets.json", "r") as f:
    secrets = json.load(f)
    private_token = secrets["private_token"]

gl = gitlab.Gitlab("https://gitlab.gnome.org/", private_token=private_token)

project = gl.projects.get(project_id)
issue = project.issues.get(issue_id)
discussions = issue.discussions.list()

conversation_dict = {}


def remove_quoted(text: str) -> str:
    text_split = text.split("\n")
    non_quotes = list(filter(lambda str: not str.startswith(">"), text_split))
    return " ".join(non_quotes)


def remove_markdown_urls(text: str) -> str:
    return re.sub(r"(?:__|[*#])|\[(.*?)\]\(.*?\)", "", text)


for discussion in discussions:
    for elem in discussion.attributes["notes"]:

        author: str = elem["author"]["name"]
        body: str = elem["body"]

        ignored = ("changed the description", "mentioned in issue")

        if not body.startswith(ignored):

            body = remove_quoted(body)
            body = remove_markdown_urls(body)
            body = clean(
                body,
                fix_unicode=True,
                to_ascii=True,
                lower=False,
                no_line_breaks=True,
                no_urls=True,
                no_emails=True,
                no_phone_numbers=True,
                no_numbers=False,
                no_digits=False,
                no_currency_symbols=True,
                no_punct=False,
            )

            if not conversation_dict.get(author):
                conversation_dict[author] = body
            else:
                conversation_dict[author] += " " + body

with open("./data/conversation/conversation.json", "w") as fp:
    json.dump(conversation_dict, fp)
