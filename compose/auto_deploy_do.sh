#! /bin/bash

# This shell script quickly deploys your project to your
# DigitalOcean Droplet

# generate TAR file from git
git archive --format tar --output ./app.tar master

echo 'Uploading project...'
rsync ./app.tar root@$DIGITAL_OCEAN_IP_ADDRESS:/tmp/app.tar
echo 'Uploaded complete.'

echo 'Building image...'
ssh -o StrictHostKeyChecking=no root@$DIGITAL_OCEAN_IP_ADDRESS << 'ENDSSH'
    mkdir -p /app
    rm -rf /app/* && tar -xf /tmp/app.tar -C /app
    docker-compose -f /app/docker-compose.prod.yml build
ENDSSH
echo 'Build complete.'