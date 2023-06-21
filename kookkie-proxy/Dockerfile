FROM haproxy:2.1.7-alpine
COPY haproxy.cfg /usr/local/etc/haproxy/haproxy.cfg

RUN adduser -D afp
USER afp
