#!/bin/bash
set -euxo pipefail
exec > >(tee /var/log/user-data.log) 2>&1

echo "Updating system..."
apt update -y

echo "Installing base packages..."
apt install -y \
  curl \
  ca-certificates \
  unzip \
  gnupg \
  lsb-release \
  apt-transport-https

# Docker Installation
echo "Installing Docker..."
mkdir -p /etc/apt/keyrings

curl -fsSL https://download.docker.com/linux/ubuntu/gpg \
  | tee /etc/apt/keyrings/docker.asc > /dev/null

chmod a+r /etc/apt/keyrings/docker.asc

echo \
"deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] \
https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" \
| tee /etc/apt/sources.list.d/docker.list

apt update -y

apt install -y \
  docker-ce \
  docker-ce-cli \
  containerd.io \
  docker-buildx-plugin \
  docker-compose-plugin

systemctl enable docker
systemctl start docker

# Allow ubuntu user to use docker
usermod -aG docker ubuntu || true

# AWS CLI Installation
echo "Installing AWS CLI..."
curl -fsSL https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip -o awscliv2.zip

unzip awscliv2.zip
./aws/install
rm -rf aws awscliv2.zip

# kubectl Installation
echo "Installing kubectl..."
curl -LO "https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl"

chmod +x kubectl
mv kubectl /usr/local/bin/

# Validation
echo "=== Installed Versions ==="
docker --version
aws --version
kubectl version --client