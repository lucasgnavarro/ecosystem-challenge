
FROM python:3.7

ENV PYTHONPATH "${PYTHONPATH}:/ecosystem"

RUN mkdir /ecosystem

COPY ./app ./requirements.txt ./Makefile ./cli.py  /ecosystem/

RUN pip install -r /ecosystem/requirements.txt

EXPOSE 8000

CMD make server
