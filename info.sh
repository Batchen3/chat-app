#!/bin/bash
echo "containers"
docker ps -a

echo "images"
docker images

echo "volums"
docker volume ls

echo "networks"
docker network ls