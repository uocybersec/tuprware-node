# USEFUL REDDIT THREAD: https://www.reddit.com/r/docker/comments/u73dxw/starting_containers_dynamically_question/

import docker
import redis
import os
from dotenv import load_dotenv
from time import time
from flask import Flask
from flask import request
from flask_jwt_extended import JWTManager
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import create_access_token
from utils.control_challenges import spawn_challenge
from utils.control_challenges import stop_challenge
from utils.control_challenges import restart_challenge

load_dotenv()
app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

jwt = JWTManager(app)
docker_client = docker.from_env()
redis_conn = redis.Redis(
    host='localhost', 
    port=6379, 
    decode_responses=True
)

# ERROR PROOF ALL ROUTES
# DEAL WITH TOKENS EXPIRING
@app.route('/spawn-challenge', methods=["POST"])
@jwt_required()
def spawn():
    user_id = get_jwt_identity()
    challenge_id = request.json['challenge_id']
    instance_id = time() # figure out new way to generate instance ID. Ideas: UNIX timestamp, username or handle in the CTF, teamname, etc.
    spawn_challenge(
        challenge_id=challenge_id,
        instance_id=instance_id,
        redis_conn=redis_conn,
        user_id=user_id
    )
    return "Challenge instance spawned.", 200


@app.route('/stop-challenge', methods=["POST"])
@jwt_required()
def stop():
    user_id = get_jwt_identity()
    stop_challenge(
        redis_conn=redis_conn,
        user_id=user_id
    )
    return "Challenge instance stopped.", 200


@app.route('/restart-challenge', methods=["POST"])
@jwt_required()
def restart():
    user_id = get_jwt_identity()
    restart_challenge(
        redis_conn=redis_conn,
        user_id=user_id
    )
    return "Challenge instance restarted.", 200


@app.route('/get-node-available-memory', methods=["GET"])
def get_avail_mem():
    return "work in progress", 200


# ***** REMOVE LATER *****
@app.route('/test') # test route to give myself a JWT to authenticate myself
def test():
    return create_access_token(identity='e0df7f84-0061-44d3-b531-e4bc22428a27')

if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=False)
