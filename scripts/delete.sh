#!/bin/bash
version=$1
# if [ "" =  "$version" ]; then
#     echo "Error: Missing parameter, Run again with the version did you want."
#     exit 1
# fi
# docker rm -f chat_con
# docker rmi -f chat_img:${version}
# docker volume rm chat-data

gcloud compute ssh batchen-first-instance --project grunitech-mid-project --zone me-west1-a --command "gcloud auth configure-docker me-west1-docker.pkg.dev; docker stop chat_con; docker rm -f chat_con; docker rmi -f chat_img:${version}; docker volume rm chat-data;"
