# !/bin/bash
version=$1
# gcloud config set auth/impersonate_service_account batchen-instance-sa@grunitech-mid-project.iam.gserviceaccount.com

# gcloud compute ssh batchen-first-instance --project grunitech-mid-project --zone me-west1-a 
# gcloud auth configure-docker me-west1-docker.pkg.dev

# docker pull me-west1-docker.pkg.dev/grunitech-mid-project/batchen-chat-app-images/chat-app:${version}
# docker run -p 8080:5000 me-west1-docker.pkg.dev/grunitech-mid-project/batchen-chat-app-images/chat-app:${version}



gcloud compute ssh batchen-first-instance --project grunitech-mid-project --zone me-west1-a --command "gcloud auth configure-docker me-west1-docker.pkg.dev; docker volume create chat-data; docker pull me-west1-docker.pkg.dev/grunitech-mid-project/batchen-chat-app-images/chat-app:${version}; docker run -v chat-data:/chatApp/data -v chat-data:/chatApp/rooms -d --name chat_con -p 8080:5000 me-west1-docker.pkg.dev/grunitech-mid-project/batchen-chat-app-images/chat-app:${version};"






# docker run -d --name my-con me-west1-docker.pkg.dev/grunitech-mid-project/batchen-chat-app-images/chat-app:${version}

                            # docker run -p 8080:5000 "me-west1-docker.pkg.dev/$PROJECT_ID/$REPOSITORY/$IMAGE:$TAG"
# if [ "" =  "$version" ]; then
#     echo "Error: Missing parameter, Run again with the version did you want."
#     exit 1
# fi
# docker volume create chat-data
# docker build -t chat_img:${version} .
# docker run -v chat-data:/chatApp/data -v chat-data:/chatApp/rooms -d -p 5000:5000 --name chat_con --memory=1g --memory-reservation=512m --cpus=1 --cpuset-cpus=2 chat_img:${version}

# cmd interval curl  - for route health 


