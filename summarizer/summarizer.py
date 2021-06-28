#!/usr/bin/env python

from gitlab.v4.objects import users
from .utils import remove_markdown_urls, remove_quoted, clean_up

import os

import json
import gitlab

import pytextrank

from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer

from sumy.summarizers.kl import KLSummarizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.summarizers.lex_rank import LexRankSummarizer
from sumy.summarizers.text_rank import TextRankSummarizer


class Summarizer:
    """Download and summarize Gitlab conversations.

    Other types of conversations will be supported in the future.

    """

    ignored = ("changed the description", "mentioned in issue")

    def __init__(
        self, project_id: int, issue_id: int, private_token: chr, database: dict
    ):

        self.database: dict = database
        self.authors: set = set()
        self.private_token = private_token

        self.gl = gitlab.Gitlab(
            "https://gitlab.gnome.org/", private_token=self.private_token
        )

        self.project = self.gl.projects.get(project_id)
        self.issue = self.project.issues.get(issue_id)
        self.discussions = self.issue.discussions.list()

        self.conversation: dict = {}

    def _summarise(self, summarizer):
        """Summarizes the conversation held in self using summarizer.

        Args:
            summarizer (AbstractSummarizer): a summarizer from sumy.

        Returns:
            dict: the summarized conversation in the following format:
        """

        parsers = {}
        summary = {}

        for (k, v) in self.conversation.items():

            # k is just an index (0, 1, 2, ...)
            # v has the following format: {'gitlab_comment_id': ..., 'username': ..., 'name': ..., 'comment': ...}

            parsers[k] = PlaintextParser.from_string(v["comment"], Tokenizer("english"))

            for (k, v) in parsers.items():
                summary[k] = summarizer(v.document, 2)

            for (k, v) in summary.items():
                text_summary = ""
                for sentence in v:
                    text_summary += " " + str(sentence)
                summary[k] = text_summary.strip()

        return summary

    def summarize_with_kld(self) -> None:
        kld_conversation: dict = self._summarise(KLSummarizer())
        with open(self.database["KLD"]["path"], "w") as fp:
            json.dump(kld_conversation, fp)

    def summarize_with_lsa(self) -> None:
        lsa_conversation = self._summarise(LsaSummarizer())
        with open(self.database["LSA"]["path"], "w") as fp:
            json.dump(lsa_conversation, fp)

    def summarize_with_lexrank(self) -> None:
        lex_rank_conversation: dict = self._summarise(LexRankSummarizer())
        with open(self.database["LEXRANK"]["path"], "w") as fp:
            json.dump(lex_rank_conversation, fp)

    def summarize_with_textrank(self) -> None:
        text_rank_conversation: dict = self._summarise(TextRankSummarizer())
        with open(self.database["TEXTRANK"]["path"], "w") as fp:
            json.dump(text_rank_conversation, fp)

    def add_author_to_database(self, username, name, avatar_url):

        entry = {username: {"name": name, "avatar_url": avatar_url}}

        if len(self.authors) > 0:

            with open(self.database["PEOPLE"]["path"], "r") as fp:
                authors = json.load(fp)

            if not authors.get(username):
                authors[username] = entry
                with open(self.database["PEOPLE"]["path"], "w") as fp:
                    json.dump(authors, fp)

        else:
            with open(self.database["PEOPLE"]["path"], "w") as fp:
                json.dump(entry, fp)

        self.authors.add(username)

    def get_discussions(self) -> dict:
        for discussion in self.discussions:
            for n, note in enumerate(discussion.attributes["notes"]):

                gitlab_comment_id: int = note["id"]
                username: str = note["author"]["username"]
                name: str = note["author"]["name"]
                avatar_url: str = note["author"]["avatar_url"]

                self.add_author_to_database(username, name, avatar_url)

                body: str = note["body"]

                if not body.startswith(self.ignored):

                    body = clean_up(body)

                    entry = {
                        "gitlab_comment_id": gitlab_comment_id,
                        "username": username,
                        "name": name,
                        "comment": body,
                    }

                    self.conversation[n] = entry

        with open(self.database["ORIGINAL_CONVERSATION"]["path"], "w") as fp:
            json.dump(self.conversation, fp)
