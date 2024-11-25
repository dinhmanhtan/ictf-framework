import boto3
import threading
from queue import Queue
from settings import GAME_CONFIG_PATH
import json
from botocore.exceptions import ClientError

access_key = ""
secret_key = ""
aws_region = ""
registry_url = ""
ecr_client = boto3.client(
    "ecr",
    region_name=aws_region,
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_key,
)
ictf_repository_ecr = {
    "ictf_database": True,
    "ictf_router": True,
    "ictf_gamebot": True,
    "ictf_scriptbot": True,
    "ictf_dispatcher": True,
    "ictf_teaminterface": True,
    "ictf_logger": False,
    "ictf_scoreboard" : True
}


def get_ecr_images(ecr_client, repositoryName, images):
    paginator = ecr_client.get_paginator("list_images")
    image_tags = []
    try:
        for page in paginator.paginate(repositoryName=repositoryName):
            image_tags.extend(page["imageIds"])
            # print(f"Images in repository '{repositoryName}' ({repository_uri}):")
            for image_tag in image_tags:
                if "imageTag" in image_tag and image_tag["imageTag"] == "latest":
                    images.append(repositoryName)
                    return

    except ClientError as e:
        if e.response["Error"]["Code"] == "RepositoryNotFoundException":
            print(repositoryName)
            return


def list_ecr_images():
    #response = ecr_client.describe_repositories()

    threads = []
    ictf_repositories = []
    scriptbot_repositories = []

    game_config = json.load(open(GAME_CONFIG_PATH, "r"))
    services = game_config["services"]
    for repository in ictf_repository_ecr:
        thread = threading.Thread(
            target=get_ecr_images, args=(ecr_client, repository, ictf_repositories)
        )
        threads.append(thread)

    for service in services:
        thread = threading.Thread(
            target=get_ecr_images, args=(ecr_client, f"{service["name"]}_scripts", scriptbot_repositories)
        )
        threads.append(thread)

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    print(ictf_repositories,scriptbot_repositories )
    result = {"infrastructure_images": [], "scriptbot_images": []}	
    infrastructure_images = []
    scriptbot_images = []

    for repository_name,required in ictf_repository_ecr.items():
        if repository_name in ictf_repositories:
            infrastructure_images.append({"name": repository_name, "status": "available", "required": required}) 
        else:
            infrastructure_images.append({"name": repository_name, "status": "unavailable", "required": required}) 

    result["infrastructure_images"] = infrastructure_images

    for service in services:
        service_image = f"{service["name"]}_scripts"
        if service_image in scriptbot_repositories:
            scriptbot_images.append({"name": service_image, "status": "available", "required": True})
        else:
            scriptbot_images.append({"name": service_image, "status": "unavailable", "required": True})

    result["scriptbot_images"] = scriptbot_images

    return result
