import boto3
import threading
from queue import Queue
from settings import GAME_CONFIG_PATH
import json
from botocore.exceptions import ClientError

access_key = "AKIAXKN6XAVIBH6ODTOZ"
secret_key = "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"
aws_region = "ap-southeast-1"
registry_url = "503448012112.dkr.ecr.ap-southeast-1.amazonaws.com"
ecr_client = boto3.client(
    "ecr",
    region_name=aws_region,
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_key,
)
ictf_repository_ecr = [
    "ictf_database",
    "ictf_router",
    "ictf_gamebot",
    "ictf_scriptbot",
    "ictf_dispatcher",
    "ictf_teaminterface",
    "ictf_logger",
]


def get_ecr_images(ecr_client, repositoryName, queue):
    paginator = ecr_client.get_paginator("list_images")
    image_tags = []
    try:
        for page in paginator.paginate(repositoryName=repositoryName):
            image_tags.extend(page["imageIds"])
            # print(f"Images in repository '{repositoryName}' ({repository_uri}):")
            for image_tag in image_tags:
                if "imageTag" in image_tag:
                    queue.put(f"{repositoryName}:{image_tag['imageTag']}")
    except ClientError as e:
        if e.response["Error"]["Code"] == "RepositoryNotFoundException":
            print(f"Repository not found {repositoryName}")


def list_ecr_images():
    response = ecr_client.describe_repositories()

    threads = []
    image_queue = Queue()
    # for repository in response["repositories"]:
    #     repository_uri = repository["repositoryUri"]
    #     repositoryName = repository["repositoryName"]
    #     thread = threading.Thread(
    #         target=get_ecr_images, args=(ecr_client, repositoryName, image_queue)
    #     )
    #     threads.append(thread)
    game_config = json.load(open(GAME_CONFIG_PATH, "r"))
    for repository in ictf_repository_ecr:
        thread = threading.Thread(
            target=get_ecr_images, args=(ecr_client, repository, image_queue)
        )
        threads.append(thread)

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    ecr_images = []
    while not image_queue.empty():
        image = image_queue.get()
        ecr_images.append(image)

    return ecr_images
