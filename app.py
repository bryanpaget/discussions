#!/usr/bin/env python

import os
import subprocess
import json
import pandas as pd
import numpy as np

import nltk

nltk.download("punkt")

from summarizer.summarizer import Summarizer
from summarizer.database import *

import streamlit as st


@st.cache  # 👈 This function will be cached
def do_summarize(project_id, issue_id, private_token):
    summarizer = Summarizer(project_id, issue_id, private_token, database)
    summarizer.get_discussions()

    summarizer.summarize_with_textrank()
    summarizer.summarize_with_kld()
    summarizer.summarize_with_lexrank()
    summarizer.summarize_with_lsa()

    return


@st.cache
def do_load_data():
    with open("./summarizer/data/conversation/conversation.json", "r") as f:
        conversation = json.load(f)
    with open("./summarizer/data/summarized/kld_conversation.json", "r") as f:
        kld = json.load(f)
    with open("./summarizer/data/summarized/lex_rank_conversation.json", "r") as f:
        lexrank = json.load(f)
    with open("./summarizer/data/summarized/lsa_conversation.json", "r") as f:
        lsa = json.load(f)
    with open("./summarizer/data/summarized/text_rank_conversation.json", "r") as f:
        textrank = json.load(f)

    return conversation, kld, lexrank, lsa, textrank


def do_print(conversation):
    st.write(conversation)
    # for (k, v) in conversation.items():
    #     st.title(v.get("name"))
    #     st.write(v.get("comment"))


def create_db():
    if not os.path.exists("./summarizer/data"):
        os.mkdir("./summarizer/data/")
        os.mkdir("./summarizer/data/conversation/")
        os.mkdir("./summarizer/data/people/")
        os.mkdir("./summarizer/data/secrets/")
        os.mkdir("./summarizer/data/summarized/")


if __name__ == "__main__":

    create_db()

    project_id = st.text_input("Project ID: ", value="426")
    issue_id = st.text_input("Issue ID: ", value="1413")
    private_token = st.text_input("Private Token: ", value="NuhXFqQ63_cdrf4ohAxF")

    do_summarize(
        project_id=int(project_id),
        issue_id=int(issue_id),
        private_token=private_token,
    )

    conversation, kld, lexrank, lsa, textrank = do_load_data()

    st.title("Discussions")

    st.write("Summarize discussions and compare methods.")

    option = st.selectbox("Show:", ("Original", "Text Rank", "KLD", "Lex Rank", "LSA"))

    if option == "Original":
        do_print(conversation)
    elif option == "Text Rank":
        do_print(textrank)
    elif option == "KLD":
        do_print(kld)
    elif option == "Lex Rank":
        do_print(lexrank)
    elif option == "LSA":
        do_print(lsa)
