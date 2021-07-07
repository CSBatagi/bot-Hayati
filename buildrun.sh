#!/bin/bash
docker stop hayati-bot
docker container rm hayati-bot
docker image rm hayati-bot
docker build ./ -t hayati-bot
docker run -p 8080:8080 -d  --name hayati-bot --env LOGLEVEL=10 --restart always hayati-bot
