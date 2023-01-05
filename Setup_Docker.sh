#!/bin/sh
sudo docker build -t "camera_server:latest" .
sudo docker image prune
sudo docker container rm -f CameraAPI
sudo docker container rm -f ImagePool
sudo docker run --detach --publish 8082:8082 --name CameraAPI --restart always camera_server:latest /bin/sh -c 'cd /Camera; python3 CameraAPI.py'
sudo docker run --detach --name ImagePool --restart always camera_server:latest /bin/sh -c 'cd /Camera; python3 ImagePool.py'