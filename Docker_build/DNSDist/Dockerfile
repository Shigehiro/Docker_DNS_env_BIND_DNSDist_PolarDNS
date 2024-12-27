FROM docker.io/ubuntu:24.04

COPY entrypoint.sh /
RUN apt-get update && apt-get install -y dnsdist --no-install-recommends && chmod +x /entrypoint.sh
EXPOSE 53/udp 53/tcp

ENTRYPOINT ["/entrypoint.sh"]
