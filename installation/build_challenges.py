import boto3
import docker
import os
import shutil
import json
import zipfile
from dotenv import load_dotenv

def main():
    load_dotenv()

    docker_client = docker.from_env()
    s3_client = boto3.client(
        's3',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY'),
        aws_secret_access_key=os.getenv('AWS_SECRET_KEY')
    )

    CHALLENGES_S3_BUCKET_NAME = os.getenv('AWS_CHALLENGE_S3_BUCKET_NAME')
    PATH_TO_CHALLENGES = '/tmp/uoctf-challenges/'
    NUM_OF_CHALLENGES = s3_client.list_objects_v2(Bucket=CHALLENGES_S3_BUCKET_NAME)['KeyCount']
    CHALLENGE_IDS = range(1, NUM_OF_CHALLENGES+1) # Challenge IDs range from 1...N for N challenges
    challenges_object = {}

    for id_ in CHALLENGE_IDS:
        print(f'Fetching challenge with ID {id_} from S3 bucket...', end='', flush=True)
        s3_client.download_file(
            CHALLENGES_S3_BUCKET_NAME, 
            f'{id_}.zip', 
            os.path.join(PATH_TO_CHALLENGES, f'{id_}.zip')
        )
        print('done.')

        print(f'Decompressing challenge ZIP file with ID {id_}...', end='', flush=True)
        with zipfile.ZipFile(os.path.join(PATH_TO_CHALLENGES, f'{id_}.zip'), mode='r') as challenge_zip:
            challenge_zip.extractall(PATH_TO_CHALLENGES)
        os.remove(os.path.join(PATH_TO_CHALLENGES, f'{id_}.zip'))
        print('done.')

        print(f'Building challenge with ID {id_}...', end='', flush=True)
        image_tag = f"uoctf-{id_}"
        image, logs = docker_client.images.build(path=os.path.join(PATH_TO_CHALLENGES, str(id_)), dockerfile="Dockerfile", tag=image_tag)
        challenges_object[id_] = image_tag
        print('done.')
    
    print('Creating challenges.json file...', end='', flush=True)
    with open('../challenges.json', mode='w') as challenges_json_file:
        challenges_json_file.write(json.dumps(challenges_object))
    print('done.')

    print(f'Deleting the {PATH_TO_CHALLENGES} directory...', end='', flush=True)
    shutil.rmtree(PATH_TO_CHALLENGES)
    print('done.')
    

if __name__ == '__main__':
    main()