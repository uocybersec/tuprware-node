import docker
import os
import json

def main():
    client = docker.from_env()

    # further enhance this to make it more efficient. 
    PATH_TO_CHALLENGES = '/tmp/uoctf-challenges'
    CHALLENGE_IDS = ['1', '2', '3'] # figure out a way to get the challenge IDs instead of hardcoding it. 
    challenges_object = {}

    for id_ in CHALLENGE_IDS:
        print(f'[*] Building challenge with ID: {id_}...', end='', flush=True)
        image_tag = f"uoctf-{id_}"
        image, logs = client.images.build(path=os.path.join(PATH_TO_CHALLENGES, id_), dockerfile="Dockerfile", tag=image_tag)
        challenges_object[id_] = image_tag
        print('done.')
    
    print('[*] Creating challenges.json file...', end='', flush=True)
    with open('challenges.json', mode='w') as challenges_json_file:
        challenges_json_file.write(json.dumps(challenges_object))
    print('done.')

if __name__ == '__main__':
    main()