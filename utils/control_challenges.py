import docker
import redis
import json
from utils.manage_host_ports import get_host_port
from typing import Tuple

CONTAINER_PORT = 1337
CONTAINER_ALLOCATED_MEMORY = "128m" # every challenge container is allocated 128 megabytes of memory

client = docker.from_env()

def spawn_challenge(challenge_id: str, instance_id: str, redis_conn: redis.Redis, user_id: str) -> None:
    # ALSO FIND A WAY TO LOG SOMEWHERE THAT A CONTAINER RAN OUT OF MEMORY SO WE KNOW WHAT CAUSES ISSUES DURING THE CTF
    if redis_conn.get(user_id) == None: # check if the user does not already have an instance running
        with open('challenges.json', mode='r') as challenges_json:
            challenges = json.loads(challenges_json.read())
            if challenge_id in challenges.keys():
                host_port = get_host_port()
                instance_name = f'uoctf-{challenge_id}-{instance_id}'
                client.containers.run(
                    image=challenges[challenge_id], 
                    name=instance_name, 
                    detach=True, 
                    ports={CONTAINER_PORT: host_port},
                    mem_limit=CONTAINER_ALLOCATED_MEMORY # memory is not being allocated to containers when ran on my laptop. this is an issue with my laptop's install of docker. but its important to note that this issue could also happen on nodes. 
                )
                redis_conn.set(user_id, instance_name)
            else:
                raise Exception("Invalid challenge ID.")
    else: # if the user already has an instance running, shutdown the instance and start this one
        stop_challenge(redis_conn, user_id)
        spawn_challenge(challenge_id, instance_id, redis_conn, user_id)


def stop_challenge(redis_conn: redis.Redis, user_id: str) -> Tuple[str, str]:
    container_id = redis_conn.get(user_id)
    if container_id:
        target_container = client.containers.get(
            container_id=container_id
        )
        target_container.stop()
        target_container.remove()
        redis_conn.delete(user_id)
        _, challenge_id, instance_id = container_id.split('-')
        return challenge_id, instance_id
    else:
        raise Exception("There is no challenge to stop.")


def restart_challenge(redis_conn: redis.Redis, user_id: str) -> None:
    try:
        challenge_id, instance_id = stop_challenge(redis_conn, user_id)
        spawn_challenge(challenge_id, instance_id, redis_conn, user_id)
    except Exception as e:
        if str(e) == "There is no challenge to stop.":
            raise Exception("There is no challenge to restart.")
        else:
            raise e