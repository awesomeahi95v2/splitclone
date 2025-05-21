#!/bin/bash

# Step 1: Generate a version tag from Git commit hash
VERSION=$(git rev-parse --short HEAD)
IMAGE_URI="395720230803.dkr.ecr.us-east-1.amazonaws.com/splitclone:$VERSION"

echo "🚀 Building Docker image: $VERSION"

# Step 2: Build and push Docker image
docker build -t splitclone:$VERSION .
docker tag splitclone:$VERSION $IMAGE_URI
docker push $IMAGE_URI

# Step 3: Generate Terraform variable override
echo "docker_image_url = \"$IMAGE_URI\"" > deploy_version.auto.tfvars

# Step 4: Run Terraform apply with that tag
cd infra/fargate
echo "📦 Applying Terraform with image: $IMAGE_URI"
terraform apply -var-file=../../deploy_version.auto.tfvars
