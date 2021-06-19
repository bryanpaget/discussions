#!/usr/bin/env python

import json

from summarizer.summarizer import Summarizer

import databases
import sqlalchemy
from starlette.applications import Starlette
from starlette.config import Config
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.applications import Starlette
from starlette.routing import Route, Mount
from starlette.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles
import uvicorn

templates = Jinja2Templates(directory="templates")

PARTICIPANTS = {
    "id": {"name": "", "avatar_url": ""},
    "path": "./data/people/people.json",
}
ORIGINAL_CONVERSATION = {
    "id": {"gitlab_comment_id": "", "name": "", "comment": ""},
    "path": "./data/conversation/conversation.json",
}
KLD = {
    "id": {"name": "", "comment": ""},
    "path": "./data/summarized/kld_conversation.json",
}
LSA = {
    "id": {"name": "", "comment": ""},
    "path": "./data/summarized/lsa_conversation.json",
}
TEXTRANK = {
    "id": {"name": "", "comment": ""},
    "path": "./data/summarized/text_rank_conversation.json",
}
LEXRANK = {
    "id": {"name": "", "comment": ""},
    "path": "./data/summarized/lex_rank_conversation.json",
}
SPACY = {
    "id": {"name": "", "comment": ""},
    "path": "./data/summarized/spacy_conversation.json",
}

database = {
    "PARTICIPANTS": PARTICIPANTS,
    "ORIGINAL_CONVERSATION": ORIGINAL_CONVERSATION,
    "KLD": KLD,
    "LSA": LSA,
    "TEXTRANK": TEXTRANK,
    "LEXRANK": LEXRANK,
    "SPACY": SPACY
}

for (k, v) in database.items():
    with open(v["path"], "w") as fp:
        json.dump(dict, fp)

app = Starlette(debug=True)
app.mount("/static", StaticFiles(directory="statics"), name="static")


@app.route("/", methods=["GET", "POST"])
async def homepage(request):
    project_id = 0
    issue_id = 0
    template = "index.html"
    context = {"request": request, "project_id": project_id, "issue_id": issue_id}
    return templates.TemplateResponse(template, context)


@app.route("/summarize", methods=["GET", "POST"])
async def summarize(request):
    form = await request.form()
    print(form)
    if ("project_id" in form) and ("issue_id" in form):
        project_id = request.form["project_id"]
        issue_id = request.form["issue_id"]
        print(issue_id, project_id)
    summarizer = Summarizer(project_id=project_id, issue_id=issue_id, database)
    template = "summarize.html"
    context = {"request": request, "summarizer": summarizer}
    return templates.TemplateResponse(template, context)


@app.route("/kld")
async def kld(request):
    summary = "KLD"
    template = "summarize.html"
    context = {"summary": summary, "request": request}
    return templates.TemplateResponse(template, context)


@app.route("/lsa")
async def lsa(request):
    summary = "LSA"
    template = "summarize.html"
    context = {"summary": summary, "request": request}
    return templates.TemplateResponse(template, context)


@app.route("/lexrank")
async def lexrank(request):
    summary = "Lex Rank"
    template = "summarize.html"
    context = {"summary": summary, "request": request}
    return templates.TemplateResponse(template, context)


@app.route("/textrank")
async def textrank(request):
    summary = "Text Rank"
    template = "summarize.html"
    context = {"summary": summary, "request": request}
    return templates.TemplateResponse(template, context)


@app.route("/spacy")
async def spacy(request):
    summary = "spaCy"
    template = "summarize.html"
    context = {"summary": summary, "request": request}
    return templates.TemplateResponse(template, context)


@app.route("/error")
async def error(request):
    """
    An example error. Switch the `debug` setting to see either tracebacks or 500 pages.
    """
    raise RuntimeError("Oh no")


@app.exception_handler(404)
async def not_found(request, exc):
    """
    Return an HTTP 404 page.
    """
    template = "404.html"
    context = {"request": request}
    return templates.TemplateResponse(template, context, status_code=404)


@app.exception_handler(500)
async def server_error(request, exc):
    """
    Return an HTTP 500 page.
    """
    template = "500.html"
    context = {"request": request}
    return templates.TemplateResponse(template, context, status_code=500)


if __name__ == "__main__":

    uvicorn.run(app, host="0.0.0.0", port=8001)

    # Defualt project_id = 426, issue_id = 1413
