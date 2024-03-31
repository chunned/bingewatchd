FROM python:3.10-slim

RUN pip3 install gunicorn
COPY . /spotufy
WORKDIR /spotufy

COPY reqs.txt requirements.txt
RUN pip3 install -r requirements.txt

EXPOSE 8080

CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]
