import docker
import json
from utils.manage_host_ports import get_host_port
from typing import Tuple
from utils.db_operations import get_running_instance_id
from utils.db_operations import set_running_instance_id
from utils.db_operations import delete_running_instance_id
from utils.custom_exceptions import InvalidChallengeIDException
from utils.custom_exceptions import NoChallengeToStopException
from utils.custom_exceptions import NoChallengeToRestartException

CONTAINER_PORT = 1337
CONTAINER_ALLOCATED_MEMORY = "128m" # every challenge container is allocated 128 megabytes of memory

client = docker.from_env()

def spawn_challenge(challenge_id: str, instance_id: str, user_id: str) -> None:
    # ALSO FIND A WAY TO LOG SOMEWHERE THAT A CONTAINER RAN OUT OF MEMORY SO WE KNOW WHAT CAUSES ISSUES DURING THE CTF
    if get_running_instance_id(user_id) == None: # check if the user does not already have an instance running
        with open('challenges.json', mode='r') as challenges_json:
            challenges = json.loads(challenges_json.read())

            if challenge_id in challenges.keys():
                host_port = get_host_port()
                instance_id = f'uoctf-{challenge_id}-{instance_id}'

                client.containers.run(
                    image=challenges[challenge_id], 
                    name=instance_id, 
                    detach=True, 
                    ports={CONTAINER_PORT: host_port},
                    mem_limit=CONTAINER_ALLOCATED_MEMORY 
                )

                res_code = set_running_instance_id(user_id, instance_id)
                if res_code != 200:
                    raise Exception(f"[WRITE] Response code from AWS Lambda invokation was {res_code}.")
            else:
                raise InvalidChallengeIDException
    else: # if the user already has an instance running, shutdown the instance and start this one
        stop_challenge(user_id)
        spawn_challenge(challenge_id, instance_id, user_id)


def stop_challenge(user_id: str) -> Tuple[str, str]:
    container_id = get_running_instance_id(user_id)
    if container_id:
        target_container = client.containers.get(
            container_id=container_id
        )
        target_container.stop()
        target_container.remove()
        res_code = delete_running_instance_id(user_id)
        if res_code != 200:
            raise Exception(f"[DELETE] Response code from AWS Lambda invokation was {res_code}.")
        
        _, challenge_id, instance_id = container_id.split('-')
        return challenge_id, instance_id
    else:
        raise NoChallengeToStopException


def restart_challenge(user_id: str) -> None:
    try:
        challenge_id, instance_id = stop_challenge(user_id)
        spawn_challenge(challenge_id, instance_id, user_id)
    except Exception as e:
        if isinstance(e, NoChallengeToStopException):
            raise NoChallengeToRestartException
        else:
            raise e