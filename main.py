
# USEFUL REDDIT THREAD: https://www.reddit.com/r/docker/comments/u73dxw/starting_containers_dynamically_question/

from flask import Flask, request
import docker
from utils.control_challenges import spawn_challenge, stop_challenge, restart_challenge
from time import time

app = Flask(__name__)
docker_client = docker.from_env()

# ********************** ADD AUTHENTICATION ********************************
@app.route('/spawn-challenge', methods=["POST"])
def spawn():
    challenge_id = request.json['challenge_id']
    instance_id = time() # figure out new way to generate instance ID. Ideas: UNIX timestamp, username or handle in the CTF, teamname, etc.
    spawn_challenge(
        challenge_id=challenge_id,
        instance_id=instance_id
    )
    return "Challenge instance spawned.", 200


@app.route('/stop-challenge', methods=["POST"])
def stop():
    challenge_id = request.json['challenge_id']
    instance_id = request.json['instance_id']
    stop_challenge(
        challenge_id=challenge_id,
        instance_id=instance_id
    )
    return "Challenge instance stopped.", 200


@app.route('/restart-challenge', methods=["POST"])
def restart():
    challenge_id = request.json['challenge_id']
    instance_id = request.json['instance_id']
    restart_challenge(
        challenge_id=challenge_id,
        instance_id=instance_id
    )
    return "Challenge instance restarted.", 200


if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=False)
