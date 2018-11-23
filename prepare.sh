docker info --format "{{.OperatingSystem}}"
if [[ $? -ne 0 ]]; then
   echo "You need to install docker"
   exit 0
fi

docker-compose version
if [[ $? -ne 0 ]]; then
   echo "You need to install docker-compose"
   exit 0
fi

echo "building docker image for raspberry pi3"
docker-compose build
