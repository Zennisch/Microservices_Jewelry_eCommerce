#!/bin/bash

exec > >(tee -a /var/log/startup-script.log)
exec 2>&1

echo "Starting setup script at $(date)"

apt update && apt upgrade -y

echo "Installing Git..."
apt install git -y

git config --global user.name "JEC User"
git config --global user.email "user@jec-project.com"

echo "Git version: $(git --version)"

echo "Installing Docker..."
apt install ca-certificates curl -y
install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
chmod a+r /etc/apt/keyrings/docker.asc

echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  tee /etc/apt/sources.list.d/docker.list > /dev/null

apt update
apt install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin docker-compose -y

groupadd docker 2>/dev/null || true
usermod -aG docker ray

systemctl start docker
systemctl enable docker

docker run hello-world

echo "Setup completed at $(date)"
echo "Docker version: $(docker --version)"
echo "Docker Compose version: $(docker-compose --version)"

touch /home/ray/setup-complete.txt
chown ray:ray /home/ray/setup-complete.txt