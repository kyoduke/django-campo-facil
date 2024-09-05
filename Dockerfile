FROM python:3.11.9-alpine3.18
LABEL mantainer="caioduque.dev@gmail.com"

ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONUNBUFFERED 1

COPY djangoapp /djangoapp
COPY scripts /scripts
COPY certs/localhost.crt /etc/nginx/ssl/localhost.crt
COPY certs/localhost.key /etc/nginx/ssl/localhost.key
COPY default.conf /etc/nginx/conf.d/

WORKDIR /djangoapp


EXPOSE 443

RUN python -m venv /.venv
RUN adduser --disabled-password --no-create-home duser

RUN chown -R duser:duser /.venv
RUN chmod -R +x /scripts
USER duser

RUN /.venv/bin/pip install --upgrade pip
RUN /.venv/bin/pip install -r /djangoapp/requirements.txt


ENV PATH="/scripts:/.venv/bin:$PATH"


CMD [ "commands.sh" ]