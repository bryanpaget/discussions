#!/usr/bin/env python

import json

from summarizer.summarizer import Summarizer
from summarizer.database import *

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
    summary = """Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed sed posuere metus. Vivamus et tellus vel magna venenatis convallis vitae eu lectus. Proin vel facilisis nisl. Maecenas lacus felis, mattis id mi ac, gravida ullamcorper tortor. Nulla id lacus eu mauris accumsan faucibus eget at massa. Vestibulum ac fermentum justo. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Duis viverra ut nunc vitae suscipit. Vivamus cursus leo et justo fermentum viverra. Nulla suscipit suscipit tellus, quis efficitur augue commodo sit amet. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Nulla porta pharetra elementum. Aliquam lorem orci, ultricies ut nulla vel, bibendum lacinia erat. Sed nec massa a justo laoreet hendrerit id quis turpis. Mauris eu tincidunt nulla, vitae tempus dui. Fusce auctor aliquet dolor, ut scelerisque mauris faucibus vestibulum.

    Phasellus vel quam fermentum, efficitur lacus vitae, gravida turpis. Integer a magna sed quam tempus tristique id a lectus. Suspendisse magna lacus, pharetra sagittis orci a, mattis lobortis felis. Mauris porttitor placerat mi id luctus. Curabitur tincidunt rutrum erat sit amet gravida. Quisque in sem interdum, ornare mi et, sollicitudin nisi. Nulla ligula libero, tincidunt nec lorem et, aliquet mattis nunc. Phasellus vitae neque ullamcorper, ultricies eros id, malesuada ante. Etiam mollis porta tempor. Donec nunc leo, lobortis eget risus vel, luctus rutrum sapien. Etiam venenatis mauris purus, a iaculis tellus efficitur tempus.

    Donec vestibulum nec neque maximus congue. Mauris pulvinar nibh mauris, sed molestie orci ultricies id. Pellentesque arcu mi, rhoncus quis libero vitae, aliquam ornare urna. Curabitur auctor quam a lacinia viverra. Suspendisse rutrum mauris erat, nec vestibulum risus sodales quis. Vestibulum commodo nunc ut risus vulputate congue. Quisque viverra lorem sapien, id egestas lorem facilisis eu. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Duis ut erat vitae quam posuere euismod eget non ex. Phasellus in volutpat lacus. Morbi hendrerit odio sed placerat maximus. Pellentesque finibus tortor vitae risus mollis, a consequat lacus ornare.

    Nunc vel ipsum dictum, viverra quam eu, suscipit massa. Suspendisse potenti. Nullam ac ipsum quam. Curabitur lobortis dolor nec quam efficitur faucibus. Vestibulum pellentesque id urna quis accumsan. Curabitur ut gravida lorem, at varius turpis. Maecenas sed lorem rutrum, sodales nunc sed, fermentum dui. Phasellus volutpat fermentum nibh nec volutpat. Nunc semper urna in dui consequat hendrerit. Nunc eu libero dolor. Fusce leo augue, pulvinar in libero in, rhoncus malesuada justo. Sed bibendum tempus lacus, in malesuada arcu varius non. Pellentesque interdum enim et hendrerit blandit. Curabitur faucibus ultrices congue. Duis volutpat euismod massa sit amet interdum.

    Nulla congue dapibus orci a iaculis. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce consectetur risus nec vulputate hendrerit. Proin porttitor sapien luctus libero varius dignissim. Morbi efficitur a odio id iaculis. Aenean vitae arcu felis. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos.
    """
    template = "index.html"
    context = {"request": request, "summary": summary}
    return templates.TemplateResponse(template, context)


@app.route("/kld")
async def kld(request):
    summary = "KLD"
    template = "index.html"
    context = {"summary": summary, "request": request}
    return templates.TemplateResponse(template, context)


@app.route("/lsa")
async def lsa(request):
    summary = "LSA"
    template = "index.html"
    context = {"summary": summary, "request": request}
    return templates.TemplateResponse(template, context)


@app.route("/lexrank")
async def lexrank(request):
    summary = "Lex Rank"
    template = "index.html"
    context = {"summary": summary, "request": request}
    return templates.TemplateResponse(template, context)


@app.route("/textrank")
async def textrank(request):
    summary = "Text Rank"
    template = "index.html"
    context = {"summary": summary, "request": request}
    return templates.TemplateResponse(template, context)


@app.route("/spacy")
async def spacy(request):
    summary = "spaCy"
    template = "index.html"
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
