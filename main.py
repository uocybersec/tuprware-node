import docker
import os
from dotenv import load_dotenv
from datetime import timedelta
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

@app.route('/spawn-challenge', methods=["POST"])
@jwt_required()
def spawn():
    user_id = get_jwt_identity()
    challenge_id = request.json.get('challenge_id')
    instance_id = user_id.replace('-', '_')
    if challenge_id:
        try:
            spawn_challenge(
                challenge_id=challenge_id,
                instance_id=instance_id,
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
            user_id=user_id
        )
        return "Challenge instance restarted.", 200
    except Exception as e:
        return str(e), 400


@app.route('/get-node-available-memory', methods=["GET"])
def get_avail_mem():
    return "work in progress", 200

# ***** REMOVE LATER *****
@app.route('/test') # test route to give myself a JWT to authenticate myself
def test():
    return create_access_token(
        identity='e0df7f84-0061-44d3-b531-e4bc22428a27',
        expires_delta=timedelta(days=1)
    )


if __name__ == '__main__':
    print("""
 _____                                  
|_   _|  _ _ __ _ ___ __ ____ _ _ _ ___ 
  | || || | '_ \ '_\ V  V / _` | '_/ -_)
  |_| \_,_| .__/_|  \_/\_/\__,_|_| \___| [Node]
          |_|                                                                    
    """)
    app.run(host='0.0.0.0', debug=False)
