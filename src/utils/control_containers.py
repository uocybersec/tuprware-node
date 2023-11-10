import docker
import json
from typing import Tuple
from src.utils.manage_host_ports import get_host_port
from src.utils.db_operations import get_running_instance_id
from src.utils.db_operations import set_running_instance_id
from src.utils.db_operations import delete_running_instance_id
from src.utils.custom_exceptions import InvalidChallengeIDException
from src.utils.custom_exceptions import NoChallengeToStopException
from src.utils.custom_exceptions import NoChallengeToRestartException

CONTAINER_PORT = 1337
CONTAINER_ALLOCATED_MEMORY = "128m" # every challenge container is allocated 128 megabytes of memory
#CONTAINER_ALLOCATED_STORAGE = "128m" # every challenge container is allocated X megabytes of storage

client = docker.from_env()

def spawn_challenge(challenge_id: str, instance_id: str, user_id: str) -> int:
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
                    mem_limit=CONTAINER_ALLOCATED_MEMORY,
                    #storage_opt={
                    #    'size': CONTAINER_ALLOCATED_STORAGE
                    #}
                )

                res_code = set_running_instance_id(user_id, instance_id)
                if res_code != 200:
                    raise Exception(f"[WRITE] Response code from AWS Lambda invokation was {res_code}.")
                return host_port
            else:
                raise InvalidChallengeIDException
    else: # if the user already has an instance running, shutdown the instance and start this one
        stop_challenge(user_id)
        return spawn_challenge(challenge_id, instance_id, user_id)


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


def restart_challenge(user_id: str) -> int:
    try:
        challenge_id, instance_id = stop_challenge(user_id)
        new_host_port = spawn_challenge(challenge_id, instance_id, user_id)
        return new_host_port
    except Exception as e:
        if isinstance(e, NoChallengeToStopException):
            raise NoChallengeToRestartException
        else:
            raise e
