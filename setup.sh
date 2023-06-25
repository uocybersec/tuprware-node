if [[ $(groups $USER) == *"docker"* ]]; then
    sudo apt install lsb-release curl gpg
    curl -fsSL https://packages.redis.io/gpg | sudo gpg --dearmor -o /usr/share/keyrings/redis-archive-keyring.gpg

    echo "deb [signed-by=/usr/share/keyrings/redis-archive-keyring.gpg] https://packages.redis.io/deb $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/redis.list

    sudo apt-get update -y
    sudo apt-get install python3-pip -y
    sudo apt-get install docker.io -y
    sudo apt-get install redis -y

    if test ! -f .env; then
        echo -e "\n\nCreating .env file";
        echo "JWT_SECRET_KEY=$(openssl rand -hex 32)" > .env
        echo "Tuprware Node needs an IAM user in AWS to access certain resources. Enter the following credentials for this IAM user.";
        read -p "Access Key: " access_key
        read -p "Secret Key: " secret_key
        read -p "AWS S3 bucket name for storing the challenges: " challenge_bucket_name
        echo "AWS_ACCESS_KEY=$access_key" >> .env
        echo "AWS_SECRET_KEY=$secret_key" >> .env
        echo "AWS_CHALLENGE_S3_BUCKET_NAME=$challenge_bucket_name" >> .env
    fi

    pip3 install -r requirements.txt

    rm -rf /tmp/uoctf-challenges
    mkdir /tmp/uoctf-challenges
    python3 build_challenges.py
else
    sudo apt-get update -y
    sudo apt-get install docker.io -y
    sudo usermod -aG docker $USER
    echo -e "\n\n[!] This current user is not in the 'docker' group. They have now been added to the group.";
    echo "PLEASE LOG BACK IN AS THIS USER FOR THE EFFECTS TO TAKE PLACE. THEN RUN THIS SCRIPT AGAIN.";
fi