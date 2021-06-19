#!/usr/bin/env python

import re


def remove_quoted(text: str) -> str:
    text_split = text.split("\n")
    non_quotes = list(filter(lambda str: not str.startswith(">"), text_split))
    return " ".join(non_quotes)


def remove_markdown_urls(text: str) -> str:
    return re.sub(r"(?:__|[*#])|\[(.*?)\]\(.*?\)", "", text)
