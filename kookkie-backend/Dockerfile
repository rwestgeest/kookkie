FROM python:3.10-alpine AS builder

RUN apk add --update build-base

ADD .flaskenv *.py VERSION run.sh requirements.txt /opt/kookkie-backend/
ADD app /opt/kookkie-backend/app
ADD migrations /opt/kookkie-backend/migrations

WORKDIR /opt/kookkie-backend

RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

FROM python:3.10-alpine

COPY --from=builder /opt/kookkie-backend /opt/kookkie-backend
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

RUN adduser -D kookkie

RUN mkdir -p /opt/kookkie-backend/data && chown kookkie:kookkie /opt/kookkie-backend/data

VOLUME /opt/kookkie-backend/data

USER kookkie

WORKDIR /opt/kookkie-backend

EXPOSE 5000

CMD ./run.sh
