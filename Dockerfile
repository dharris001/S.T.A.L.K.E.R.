FROM python:alpine

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade --no-cache-dir pip setuptools && \
    pip install -r requirements.txt

COPY . .
RUN pip install -e .

EXPOSE 80

CMD ["stalker"]
