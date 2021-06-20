#!/usr/bin/env python

from summarizer import Summarizer
from database import database

PROJECT_ID = 426
ISSUE_ID = 1413


if __name__ == "__main__":

    summarizer = Summarizer(PROJECT_ID, ISSUE_ID, database=database)
    summarizer.get_discussions()
    summarizer.summarize_with_textrank()
    summarizer.summarize_with_kld()
    summarizer.summarize_with_lexrank()
    summarizer.summarize_with_lsa()
    summarizer.summarize_with_spacy()
