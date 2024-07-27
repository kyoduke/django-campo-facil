FROM python:3.11.9-alpine3.18
LABEL mantainer="caioduque.dev@gmail.com"

ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONNUNBUFFERED 1

COPY djangoapp /djangoapp
COPY scripts /scripts

WORKDIR /djangoapp


EXPOSE 8000

RUN python -m venv /.venv
RUN /.venv/bin/pip install --upgrade pip
RUN /.venv/bin/pip install -r /djangoapp/requirements.txt
RUN adduser --disabled-password --no-create-home duser
RUN chown -R duser:duser /.venv
#RUN chown -R duser:duser /djangoapp

#RUN chmod -R 755 /djangoapp 
RUN chmod -R +x /scripts

ENV PATH="/scripts:/.venv/bin:$PATH"

USER duser

CMD [ "commands.sh" ]