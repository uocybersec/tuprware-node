import docker
import json
from typing import Tuple
from src.utils.manage_host_ports import get_host_port
from src.utils.custom_exceptions import InvalidChallengeIDException
from src.utils.custom_exceptions import NoChallengeToStopException
from src.utils.custom_exceptions import NoChallengeToRestartException
from src.utils.custom_exceptions import ChallengeAlreadyRunningException

CONTAINER_PORT = 1337
CONTAINER_ALLOCATED_MEMORY = "128m" # every challenge container is allocated 128 megabytes of memory
#CONTAINER_ALLOCATED_STORAGE = "128m" # every challenge container is allocated X megabytes of storage

client = docker.from_env()

def get_running_instance_id(user_id: str) -> str:
    running_instance_id = None
    containers = client.containers.list(all=True) # get the actual running instance id on the server
    for container in containers:
        if container.name.split('-')[2] == user_id: # if we actually have the instance id on the server
            running_instance_id = container.name
            
    return running_instance_id

def spawn_challenge(challenge_id: str, user_id: str) -> int:
    current_running_instance_id = get_running_instance_id(user_id)
    if current_running_instance_id == None: # check if the user does not already have an instance running
        with open('challenges.json', mode='r') as challenges_json:
            challenges = json.loads(challenges_json.read())

            if challenge_id in challenges.keys():
                host_port = get_host_port()
                instance_id = f'uoctf-{challenge_id}-{user_id}'

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

                return host_port
            else:
                raise InvalidChallengeIDException
    else: # if the user already has an instance running, shutdown the instance and start this one
        if current_running_instance_id.split('-')[1] == challenge_id: # if you are already running the challenge you are trying to spawn
            raise ChallengeAlreadyRunningException
        
        stop_challenge(user_id)
        return spawn_challenge(challenge_id, user_id)


def stop_challenge(user_id: str) -> Tuple[str, str]:
    container_id = get_running_instance_id(user_id)
    if container_id:
        target_container = client.containers.get(
            container_id=container_id
        )
        target_container.stop()
        target_container.remove()
        
        _, challenge_id, instance_id = container_id.split('-')
        return challenge_id, instance_id
    else:
        raise NoChallengeToStopException


def restart_challenge(user_id: str) -> int:
    try:
        challenge_id, _ = stop_challenge(user_id)
        new_host_port = spawn_challenge(challenge_id, user_id)
        return new_host_port
    except Exception as e:
        if isinstance(e, NoChallengeToStopException):
            raise NoChallengeToRestartException
        else:
            raise e
