FROM python:3.10

# python envs
ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100



# python dependencies
COPY ./requirements.txt /
RUN pip install -r ./requirements.txt


# upload scripts
COPY ./scripts/entrypoint.sh ./scripts/start.sh  /

WORKDIR /app

RUN useradd --uid 10000 runner
RUN chown -R runner:runner /app
USER 10000

COPY . .
