#!/bin/bash

sudo apt-get update -y

if [[ $(groups $USER) == *"docker"* ]]; then
    sudo apt install lsb-release curl gpg -y
    sudo apt-get update -y
    sudo apt-get install python3-pip -y
    sudo apt-get install docker.io -y
    sudo apt install nginx -y
    sudo apt install gunicorn -y

    if test ! -f .env; then
        echo -e "\n\nCreating .env file";
        echo "JWT_SECRET_KEY=$(openssl rand -hex 32)" > .env
        echo "Tuprware Node needs an IAM user in AWS to access certain resources. Enter the following credentials for this IAM user.";
        read -p "Access Key: " access_key
        read -p "Secret Key: " secret_key
        read -p "AWS S3 bucket name for storing the challenges: " challenge_bucket_name
        read -p "Discord App Client ID: " discord_client_id
        read -p "Discord App Client Secret: " discord_client_secret
        echo "AWS_ACCESS_KEY=$access_key" >> .env
        echo "AWS_SECRET_KEY=$secret_key" >> .env
        echo "AWS_CHALLENGE_S3_BUCKET_NAME=$challenge_bucket_name" >> .env
        echo "DISCORD_CLIENT_SECRET=$discord_client_secret" >> .env
        echo "DISCORD_CLIENT_ID=$discord_client_id" >> .env
    fi  

    pip3 install -r requirements.txt
    rm -rf /tmp/uoctf-challenges
    mkdir /tmp/uoctf-challenges
    python3 build_challenges.py

    sudo rm -rf /etc/nginx/sites-available/default
    sudo rm -rf /etc/nginx/sites-enabled/default
    sudo sh -c 'cat <<EOF > /etc/nginx/sites-available/tuprware
server {
    listen 80;

    location / {
        include proxy_params;
        proxy_pass http://unix:/tuprware-node/app.sock;
    }


    location ~ ^/challenge/(?<challenge_port>\d+)/(?<path_info>.*) {
        rewrite ^/challenge/\d+/(.*)$ /$1 break;
        proxy_pass http://127.0.0.1:$challenge_port;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
EOF'
    sudo ln -s /etc/nginx/sites-available/tuprware /etc/nginx/sites-enabled/
    sudo systemctl restart nginx
else
    sudo apt-get update -y
    sudo apt-get install docker.io -y
    sudo usermod -aG docker $USER
    echo -e "\n\n[!] This current user is not in the 'docker' group. They have now been added to the group.";
    echo "PLEASE LOG BACK IN AS THIS USER FOR THE EFFECTS TO TAKE PLACE. THEN RUN THIS SCRIPT AGAIN.";
fi
