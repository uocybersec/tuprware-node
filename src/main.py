import docker
import os
import requests
import json
from flask_cors import CORS
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
from src.utils.control_containers import get_running_instance_id
from src.utils.custom_exceptions import TuprwareNodeException
from src.utils.response_builder import create_reponse

load_dotenv()
app = Flask(__name__)
CORS(app)
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
app.config['DISCORD_CLIENT_ID'] = os.getenv('DISCORD_CLIENT_ID')
app.config['DISCORD_CLIENT_SECRET'] = os.getenv('DISCORD_CLIENT_SECRET')

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
    if challenge_id:
        try:
            instance_host_port = spawn_challenge(
                challenge_id=challenge_id,
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

# login into Tuprware using your Discord account (we use Discord OAuth on the uOCyberSec website)
@app.route('/login', methods=['POST'])
def login():
    code = request.json.get('code') # temporary code from discord OAuth2
    body = {
        'client_id': app.config.get('DISCORD_CLIENT_ID'),
        'client_secret': app.config.get('DISCORD_CLIENT_SECRET'),
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': 'https://ui.uocybersec.com/callback'
    }

    res = requests.post('https://discord.com/api/oauth2/token', data=body)
    if res.status_code == 200:
        access_token = res.json()['access_token']
        res = requests.get('https://discord.com/api/users/@me', headers={
            'Authorization': f'Bearer {access_token}'
        })
        if res.status_code == 200:
            user_id = res.json()['id']
            return create_access_token(
                identity=user_id,
                expires_delta=timedelta(days=1)
            )
        else:
            print(res.content)
    else:
        print(res.content)

    return "Something went wrong", 401

@app.route('/get-challenges', methods=['POST'])
@jwt_required()
def get_challenges():
    user_id = get_jwt_identity()
    running_instance_id = get_running_instance_id(user_id)
    total_info = {
        'running': running_instance_id
    }
    with open('../challenge_info.json', mode='r') as challenge_info:
        info = json.loads(challenge_info.read())
        total_info['all_challenges'] = info
    return total_info, 200



if __name__ == '__main__':
    print("""
 _____                                  
|_   _|  _ _ __ _ ___ __ ____ _ _ _ ___ 
  | || || | '_ \ '_\ V  V / _` | '_/ -_)
  |_| \_,_| .__/_|  \_/\_/\__,_|_| \___|
          |_|                                                                    
    """)
    app.run(host='0.0.0.0', debug=False)
