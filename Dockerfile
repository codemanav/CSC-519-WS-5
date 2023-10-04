FROM ubuntu:latest
FROM python:3-alpine

RUN apk add --update --no-cache ansible bash openssh

WORKDIR /workspace

ENTRYPOINT []
CMD ["/bin/bash"]
