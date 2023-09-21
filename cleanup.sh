#!/bin/bash
image=$1
container=$2

if [ "" !=  "$container" ]; then
    docker rm -f $container
fi
if [ "" !=  "$image" ]; then
    docker rmi -f $image
fi
docker volume rm chat-data