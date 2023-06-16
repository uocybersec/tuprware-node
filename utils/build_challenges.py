import docker
import os

client = docker.from_env()

# make it later so that it fetches the challenges externally 
PATH_TO_CHALLENGES = '/home/ryan-awad/CYBERSECURITY-CLUB/CTF/tuprware/challenges'
CHALLENGE_IDS = ['1', '2', '3']

for id_ in CHALLENGE_IDS:
    print(f'[*] Building challenge with ID: {id_}')
    image, logs = client.images.build(path=os.path.join(PATH_TO_CHALLENGES, id_), dockerfile="Dockerfile", tag=f"uoctf-{id_}")
    print('Done.\n')
