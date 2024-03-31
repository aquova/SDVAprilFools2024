FROM python:3.11-alpine

ADD requirements.txt /april/requirements.txt
RUN pip3 install -r /april/requirements.txt

WORKDIR /april
CMD ["python3", "-u", "main.py"]
