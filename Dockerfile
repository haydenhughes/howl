FROM python:3-alpine

WORKDIR /howl
COPY requirements.txt ./
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD python3 -m howl
