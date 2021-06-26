#!/usr/bin/env python

import re
from cleantext import clean


def remove_quoted(text: str) -> str:
    text_split = text.split("\n")
    non_quotes = list(filter(lambda str: not str.startswith(">"), text_split))
    return " ".join(non_quotes)


def remove_markdown_urls(text: str) -> str:
    return re.sub(r"(?:__|[*#])|\[(.*?)\]\(.*?\)", "", text)


def clean_up(comment):
    comment = remove_quoted(comment)
    comment = remove_markdown_urls(comment)
    comment = clean(
        comment,
        fix_unicode=True,
        to_ascii=True,
        lower=False,
        no_line_breaks=False,
        no_urls=True,
        no_emails=True,
        no_phone_numbers=True,
        no_numbers=False,
        no_digits=False,
        no_currency_symbols=True,
        no_punct=False,
    )
    return comment
