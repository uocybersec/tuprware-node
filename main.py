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

# DEAL WITH TOKENS EXPIRING
@app.route('/spawn-challenge', methods=["POST"])
@jwt_required()
def spawn():
    user_id = get_jwt_identity()
    challenge_id = request.json.get('challenge_id')
    if challenge_id:
        try:
            instance_id = time() # figure out better way to generate instance ID. Ideas: UNIX timestamp, username or handle in the CTF, teamname, etc.
            spawn_challenge(
                challenge_id=challenge_id,
                instance_id=instance_id,
                redis_conn=redis_conn,
                user_id=user_id
            )
            return "Challenge instance spawned.", 200
        except Exception as e:
            return str(e), 400
    else:
        return "Challenge ID is missing.", 400


@app.route('/stop-challenge', methods=["POST"])
@jwt_required()
def stop():
    try:
        user_id = get_jwt_identity()
        stop_challenge(
            redis_conn=redis_conn,
            user_id=user_id
        )
        return "Challenge instance stopped.", 200
    except Exception as e:
        return str(e), 400


@app.route('/restart-challenge', methods=["POST"])
@jwt_required()
def restart():
    try:
        user_id = get_jwt_identity()
        restart_challenge(
            redis_conn=redis_conn,
            user_id=user_id
        )
        return "Challenge instance restarted.", 200
    except Exception as e:
        return str(e), 400


@app.route('/get-node-available-memory', methods=["GET"])
def get_avail_mem():
    return "work in progress", 200


if __name__ == '__main__':
    print("""
 _____                                  
|_   _|  _ _ __ _ ___ __ ____ _ _ _ ___ 
  | || || | '_ \ '_\ V  V / _` | '_/ -_)
  |_| \_,_| .__/_|  \_/\_/\__,_|_| \___| [Node]
          |_|                                                                    
    """)
    app.run(host='0.0.0.0', debug=False)
