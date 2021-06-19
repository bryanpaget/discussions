#!/usr/bin/env python

from .utils import remove_markdown_urls, remove_quoted

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


PROJECT_ID = 426
ISSUE_ID = 1413


class Summarizer:
    """Download and summarize Gitlab conversations."""

    def __init__(self, project_id, issue_id):

        with open("./data/secrets/secrets.json", "r") as f:
            secrets = json.load(f)
            self.private_token = secrets["private_token"]

        self.gl = gitlab.Gitlab(
            "https://gitlab.gnome.org/", private_token=self.private_token
        )

        self.project = self.gl.projects.get(project_id)
        self.issue = self.project.issues.get(issue_id)
        self.discussions = self.issue.discussions.list()

        self.conversation_dict = {}

    def _summarise(self, summarizer) -> dict:

        parsers = {}
        summaries = {}

        for (k, v) in self.conversation_dict.items():

            parsers[k] = PlaintextParser.from_string(v, Tokenizer("english"))

            for (k, v) in parsers.items():
                summaries[k] = summarizer(v.document, 2)

            for (k, v) in summaries.items():
                text_summary = ""
                for sentence in v:
                    text_summary += " " + str(sentence)
                summaries[k] = text_summary.strip()

        return summaries

    def summarize_with_kl(self) -> dict:
        kld_conversation: dict = self._summarise(KLSummarizer())
        with open("./data/summarized/kld_conversation.json", "w") as fp:
            json.dump(kld_conversation, fp)
        return kld_conversation

    def summarize_with_lsa(self):
        lsa_conversation = self._summarise(LsaSummarizer())
        with open("./data/summarized/lsa_conversation.json", "w") as fp:
            json.dump(lsa_conversation, fp)
        return lsa_conversation

    def summarize_with_lexrank(self) -> dict:
        lex_rank_conversation: dict = self._summarise(LexRankSummarizer())
        with open("./data/summarized/lex_rank_conversation.json", "w") as fp:
            json.dump(lex_rank_conversation, fp)
        return lex_rank_conversation

    def summarize_with_textrank(self) -> dict:
        text_rank_conversation: dict = self._summarise(TextRankSummarizer())
        with open("./data/summarized/text_rank_conversation.json", "w") as fp:
            json.dump(text_rank_conversation, fp)
        return text_rank_conversation

    def summarise_with_spacy(self) -> dict:

        summaries = {}

        nlp = spacy.load("en_core_web_sm")

        nlp.add_pipe("textrank")

        for (k, v) in self.conversation_dict.items():

            doc = nlp(v)
            tr = doc._.textrank
            summaries[k] = " ".join(
                str(x) for x in tr.summary(limit_phrases=8, limit_sentences=2)
            ).strip()

        return summaries

    def add_author_to_database(self, author_name, author_avatar_url):
        pass

    def get_discussions(self) -> dict:
        for discussion in self.discussions:
            for note in discussion.attributes["notes"]:

                comment_id: int = note["author"]["id"]
                author: str = note["author"]["name"]
                author_avatar: str = note["author"]["avatar_url"]

                self.add_author_to_database(author, author_avatar)

                body: str = note["body"]

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

                    if not self.conversation_dict.get(author):
                        self.conversation_dict[author] = body
                    else:
                        self.conversation_dict[author] += " " + body

        with open() as fp:
            json.dump(self.conversation_dict, fp)

        with open("./data/conversation/conversation.json", "w") as fp:
            json.dump(self.conversation_dict, fp)

        return self.conversation_dict
