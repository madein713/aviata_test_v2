FROM python:3.9
ENV PYTHONUNBUFFERED=1 
ENV PYTHONPATH "${PYTHONPATH}:/code/"
RUN apt-get update && apt-get install build-essential -y && apt-get install -y vim && apt-get clean
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false
ENV PATH = "${PATH}:/root/.poetry/bin"
WORKDIR /code/
COPY pyproject.toml  poetry.lock /code/
RUN poetry install --no-root --no-dev
COPY . /code/
