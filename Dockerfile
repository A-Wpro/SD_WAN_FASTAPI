FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

COPY ./app /app

RUN pip install networkx &&\ 
pip install pulp &&\
pip install ortools &&\
pip install fastapi &&\
pip install matplotlib &&\
pip install mysql-connector-python
