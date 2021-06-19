#!/usr/bin/env python

import re
import json
import gitlab
from cleantext import clean

import spacy
import pytextrank

from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer

from sumy.summarizers.kl import KLSummarizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.summarizers.lex_rank import LexRankSummarizer
from sumy.summarizers.text_rank import TextRankSummarizer


class Summarizer:
    def __init__(self, project_id, issue_id):

        with open("./data/secrets/secrets.json", "r") as f:
            secrets = json.load(f)
            private_token = secrets["private_token"]

        gl = gitlab.Gitlab("https://gitlab.gnome.org/", private_token=private_token)

        project = gl.projects.get(project_id)
        issue = project.issues.get(issue_id)
        discussions = issue.discussions.list()

        conversation_dict = {}

        pass

    def summarise_with_spacy(conversation):

        summaries = {}

        nlp = spacy.load("en_core_web_sm")

        nlp.add_pipe("textrank")

        for (k, v) in conversation.items():

            doc = nlp(v)
            tr = doc._.textrank
            summaries[k] = " ".join(
                str(x) for x in tr.summary(limit_phrases=8, limit_sentences=2)
            ).strip()

        return summaries

    def summarise(conversation: dict, summarizer) -> dict:

        parsers = {}
        summaries = {}

        for (k, v) in conversation.items():

            parsers[k] = PlaintextParser.from_string(v, Tokenizer("english"))

            for (k, v) in parsers.items():
                summaries[k] = summarizer(v.document, 2)

            for (k, v) in summaries.items():
                text_summary = ""
                for sentence in v:
                    text_summary += " " + str(sentence)
                summaries[k] = text_summary.strip()

        return summaries


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
