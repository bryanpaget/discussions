#!/usr/bin/env python

from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route


async def homepage(request):
    return JSONResponse({"hello": "world"})


app = Starlette(
    debug=True,
    routes=[
        Route("/", homepage),
    ],
)

# TODO: be able to use just the URL.
# https://gitlab.gnome.org/GNOME/gnome-builder/-/issues/1413

if __name__ == "__main__":

    project_id = 426

    issue_id = 1413

    with open("./data/conversation/conversation.json") as json_file:
        conversation = json.load(json_file)

    text_rank_conversation = summarise(conversation, TextRankSummarizer())
    with open("./data/summarized/text_rank_conversation.json", "w") as fp:
        json.dump(text_rank_conversation, fp)

    lex_rank_conversation = summarise(conversation, LexRankSummarizer())
    with open("./data/summarized/lex_rank_conversation.json", "w") as fp:
        json.dump(lex_rank_conversation, fp)

    lsa_conversation = summarise(conversation, LsaSummarizer())
    with open("./data/summarized/lsa_conversation.json", "w") as fp:
        json.dump(lsa_conversation, fp)

    kld_conversation = summarise(conversation, KLSummarizer())
    with open("./data/summarized/kld_conversation.json", "w") as fp:
        json.dump(kld_conversation, fp)

    spacy_conversation = summarise_with_spacy(conversation)
    with open("./data/summarized/spacy_conversation.json", "w") as fp:
        json.dump(spacy_conversation, fp)
