import docker

CONTAINER_PORT = 1337
client = docker.from_env()

def spawn_challenge(challenge_id, instance_id):
    memory_allocated = "128m" # fetch it from the specific challenge
    # ALSO FIND A WAY TO LOG SOMEWHERE THAT A CONTAINER RAN OUT OF MEMORY SO WE KNOW WHAT CAUSES ISSUES DURING THE CTF
    client.containers.run(
        image=f'uoctf-{challenge_id}', 
        name=f'uoctf-{challenge_id}-{instance_id}', 
        detach=True, 
        ports={CONTAINER_PORT: 7000}, # HANDLE HOST PORT SELECTION,
        mem_limit=memory_allocated
    )


def stop_challenge(challenge_id, instance_id):
    target_container = client.containers.get(
        container_id=f'uoctf-{challenge_id}-{instance_id}'
    )
    target_container.stop()
    target_container.remove()


def restart_challenge(challenge_id, instance_id):
    stop_challenge(challenge_id, instance_id)
    spawn_challenge(challenge_id, instance_id)