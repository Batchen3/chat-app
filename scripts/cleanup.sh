#!/bin/bash
# delete all containers
docker rm -f $(docker ps -a -q)

# delete all images
docker rmi -f $(docker images -aq)

#delete all voluems
docker volume rm $(docker volume ls -q)