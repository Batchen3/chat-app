#!/bin/bash
version=$1
if [ "" =  "$version" ]; then
    echo "Error: Missing parameter, Run again with the version did you want."
    exit 1
fi
docker rm -f chat_con
docker rmi -f chat_img:${version}
docker volume rm chat-data