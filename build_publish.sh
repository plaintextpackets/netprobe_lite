#!/bin/bash

registry=$DOCKER_REGISTRY
echo "registry=$DOCKER_REGISTRY"

python_version=$PYTHON_VERSION
echo "Python version=$python_version"

echo " "

# AMD64
docker build -t $registry:manifest-amd64 \
--build-arg BASE_IMAGE_ARCH=amd64 \
--build-arg PYTHON_VERSION=$python_version \
--platform windows/amd64 .

docker push $registry:manifest-amd64

# ARM32V7
docker build -t $registry:manifest-arm32v7 \
--build-arg BASE_IMAGE_ARCH=arm32v7 \
--build-arg PYTHON_VERSION=$python_version \
--platform linux/arm/v7 .

docker push $registry:manifest-arm32v7


# ARM64V8
docker build -t $registry:manifest-arm64v8 \
--build-arg BASE_IMAGE_ARCH=arm64v8 \
--build-arg PYTHON_VERSION=$python_version \
--platform linux/arm64 .

docker push $registry:manifest-arm64v8


# Crete Manifest
docker manifest create \
$registry:latest \
--amend $registry:manifest-amd64 \
--amend $registry:manifest-arm32v7 \
--amend $registry:manifest-arm64v8


# Publish manifest to docker.io
docker manifest push $registry:latest

echo " "
echo "Published to https://hub.docker.com/repository/docker/$registry"