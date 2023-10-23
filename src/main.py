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
from src.utils.control_containers import spawn_challenge
from src.utils.control_containers import stop_challenge
from src.utils.control_containers import restart_challenge
from src.utils.custom_exceptions import TuprwareNodeException
from src.utils.response_builder import create_reponse

load_dotenv()
app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

jwt = JWTManager(app)
docker_client = docker.from_env()

@jwt.unauthorized_loader
@jwt.invalid_token_loader
def unauthorized(error): # response for request with invalid JWT
    return create_reponse(error="Unauthorized."), 401

@app.route('/spawn-challenge', methods=["POST"])
@jwt_required()
def spawn():
    user_id = get_jwt_identity()
    challenge_id = request.json.get('challenge_id')
    instance_id = user_id.replace('-', '_')
    if challenge_id:
        try:
            instance_host_port = spawn_challenge(
                challenge_id=challenge_id,
                instance_id=instance_id,
                user_id=user_id
            )

            return create_reponse(instance_port=instance_host_port), 200
        except TuprwareNodeException as e:
            return create_reponse(error=str(e)), 400
        except Exception as e:
            print(e)
            return create_reponse(error="An internal error occured."), 500 
    else:
        return create_reponse(error="Challenge ID is missing."), 400


@app.route('/stop-challenge', methods=["POST"])
@jwt_required()
def stop():
    try:
        user_id = get_jwt_identity()
        stop_challenge(
            user_id=user_id
        )
        return "", 200
    except TuprwareNodeException as e:
            return create_reponse(error=str(e)), 400
    except Exception as e:
        print(e)
        return create_reponse(error="An internal error occured."), 500


@app.route('/restart-challenge', methods=["POST"])
@jwt_required()
def restart():
    try:
        user_id = get_jwt_identity()
        new_host_port = restart_challenge(
            user_id=user_id
        )
        return create_reponse(instance_port=new_host_port), 200
    except TuprwareNodeException as e:
            return create_reponse(error=str(e)), 400
    except Exception as e:
        print(e)
        return create_reponse(error="An internal error occured."), 500


@app.route('/get-node-available-resources', methods=["GET"])
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
  |_| \_,_| .__/_|  \_/\_/\__,_|_| \___|
          |_|                                                                    
    """)
    app.run(host='0.0.0.0', debug=False)
