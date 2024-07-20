FROM python:3.10.4

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt && rm requirements.txt

COPY /quicknote /quicknote
