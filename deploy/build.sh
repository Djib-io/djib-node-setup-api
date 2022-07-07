export IMAGE_NAME="<imagename>"
export TAG_NAME=latest;

git pull

docker build -t djunoltd/$IMAGE_NAME:$TAG_NAME -f ./deploy/Dockerfile .

docker tag djunoltd/$IMAGE_NAME:$TAG_NAME djunoltd/$IMAGE_NAME:$TAG_NAME

docker push djunoltd/$IMAGE_NAME:$TAG_NAME
