FROM tiangolo/uvicorn-gunicorn-starlette:python3.7

COPY ./app /app

RUN ["uvicorn", "main:app"]