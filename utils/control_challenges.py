import docker
import redis
from utils.manage_host_ports import get_host_port

CONTAINER_PORT = 1337
CONTAINER_ALLOCATED_MEMORY = "128m" # every challenge container is allocated 128 megabytes of memory

client = docker.from_env()

def spawn_challenge(challenge_id: str, instance_id: str, redis_conn: redis.Redis, user_id: str) -> None:
    # ALSO FIND A WAY TO LOG SOMEWHERE THAT A CONTAINER RAN OUT OF MEMORY SO WE KNOW WHAT CAUSES ISSUES DURING THE CTF
    host_port = get_host_port()
    instance_name = f'uoctf-{challenge_id}-{instance_id}'
    client.containers.run(
        image=f'uoctf-{challenge_id}', 
        name=instance_name, 
        detach=True, 
        ports={CONTAINER_PORT: host_port},
        mem_limit=CONTAINER_ALLOCATED_MEMORY # memory is not being allocated to containers when ran on my laptop. this is an issue with my laptop's install of docker. but its important to note that this issue could also happen on nodes. 
    )
    redis_conn.set(user_id, instance_name)


def stop_challenge(challenge_id: str, instance_id: str, redis_conn: redis.Redis, user_id: str) -> None:
    target_container = client.containers.get(
        container_id=f'uoctf-{challenge_id}-{instance_id}'
    )
    target_container.stop()
    target_container.remove()
    redis_conn.delete(user_id)


def restart_challenge(challenge_id: str, instance_id: str, redis_conn: redis.Redis, user_id: str) -> None:
    stop_challenge(challenge_id, instance_id, redis_conn, user_id)
    spawn_challenge(challenge_id, instance_id, redis_conn, user_id)