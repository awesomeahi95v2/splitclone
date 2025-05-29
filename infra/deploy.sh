#!/bin/bash
set -e

# Step 1: Authenticate to ECR (if not already logged in)
aws ecr get-login-password --region us-east-1 \
  | docker login --username AWS --password-stdin 395720230803.dkr.ecr.us-east-1.amazonaws.com

# Step 2: Use Git hash + timestamp for version
VERSION="$(git rev-parse --short HEAD)-$(date +%s)"
IMAGE_URI="395720230803.dkr.ecr.us-east-1.amazonaws.com/splitclone:$VERSION"

echo "🚀 Building Docker image: $VERSION"

# Step 3: Build and push
docker build -t splitclone:$VERSION .
docker tag splitclone:$VERSION $IMAGE_URI
docker push $IMAGE_URI

# Step 4: Update Terraform override
echo "docker_image_url = \"$IMAGE_URI\"" > deploy_version.auto.tfvars

# Step 5: Deploy
cd infra/fargate
echo "📦 Applying Terraform with image: $IMAGE_URI"
terraform apply -var-file=../../deploy_version.auto.tfvars
