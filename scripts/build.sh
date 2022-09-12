#!/usr/bin/env bash

export IMAGE_URI=$REGION-docker.pkg.dev/$PROJECT_ID/$REGISTRY_NAME/commodore
docker build . -t "$IMAGE_URI"
docker push "$IMAGE_URI"
