FROM python:3-alpine

ENV FLASK_APP="howl"

WORKDIR /howl
COPY requirements.txt ./
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD python3 howl
