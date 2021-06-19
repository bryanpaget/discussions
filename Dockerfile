FROM tiangolo/uvicorn-gunicorn-starlette:python3.7

COPY . /app

RUN pip3 install -r /app/requirements.txt

CMD ["python3", "/app/app.py"]
