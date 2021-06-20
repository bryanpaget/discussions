#!/usr/bin/env python

PEOPLE = {
    "username": {"name": "", "avatar_url": ""},
    "path": "./summarizer/data/people/people.json",
}
ORIGINAL_CONVERSATION = {
    "id": {"gitlab_comment_id": "", "name": "", "comment": ""},
    "path": "./summarizer/data/conversation/conversation.json",
}
KLD = {
    "id": {"name": "", "comment": ""},
    "path": "./summarizer/data/summarized/kld_conversation.json",
}
LSA = {
    "id": {"name": "", "comment": ""},
    "path": "./summarizer/data/summarized/lsa_conversation.json",
}
TEXTRANK = {
    "id": {"name": "", "comment": ""},
    "path": "./summarizer/data/summarized/text_rank_conversation.json",
}
LEXRANK = {
    "id": {"name": "", "comment": ""},
    "path": "./summarizer/data/summarized/lex_rank_conversation.json",
}
SPACY = {
    "id": {"name": "", "comment": ""},
    "path": "./summarizer/data/summarized/spacy_conversation.json",
}
SECRETS = {"path": "./summarizer/data/secrets/secrets.json"}

database = {
    "PEOPLE": PEOPLE,
    "ORIGINAL_CONVERSATION": ORIGINAL_CONVERSATION,
    "KLD": KLD,
    "LSA": LSA,
    "TEXTRANK": TEXTRANK,
    "LEXRANK": LEXRANK,
    "SPACY": SPACY,
    "SECRETS": SECRETS,
}
