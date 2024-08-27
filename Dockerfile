FROM python:3.11.9-alpine3.18
LABEL mantainer="caioduque.dev@gmail.com"

ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONUNBUFFERED 1

COPY djangoapp /djangoapp
COPY scripts /scripts

WORKDIR /djangoapp


EXPOSE 8000

RUN python -m venv /.venv
RUN adduser --disabled-password --no-create-home duser

RUN chown -R duser:duser /.venv
RUN chmod -R +x /scripts
USER duser

RUN /.venv/bin/pip install --upgrade pip
RUN /.venv/bin/pip install -r /djangoapp/requirements.txt


ENV PATH="/scripts:/.venv/bin:$PATH"


CMD [ "commands.sh" ]