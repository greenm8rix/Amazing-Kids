import os
from flask import jsonify
from google.cloud import storage

GOOGLE_APPLICATION_CREDENTIALS = "./application_default_credentials.json"

storage_client = "storage.Client()"
from py_topping.data_connection.gcp import lazy_GCS

gcs =""
# lazy_GCS(
#     project_id="stellar-vista-371513",
#     bucket_name="amazing_kids",
#     credential=GOOGLE_APPLICATION_CREDENTIALS,
# )


def delete_blob(
    blob,
):
    """Deletes a blob from the bucket."""
    # bucket_name = "your-bucket-name"
    # blob_name = "your-object-name"
    blob.delete()

    print(f"Blob {blob} deleted.")


def create_folder(
    username,
    filename,
    username_downloads,
    bucket_name="amazing_kids",
):

    bucket = storage_client.get_bucket(bucket_name)  # your bucket name

    blob = bucket.blob(f"{username}/{username_downloads}")

    blob.upload_from_filename(filename)
    blob.make_public()
    return blob.public_url, blob


def create_folder_tmp(
    username,
    filename,
    username_downloads,
    bucket_name="amazing_kids",
):

    bucket = storage_client.get_bucket(bucket_name)  # your bucket name

    blob = bucket.blob(f"{username}+tmp/{username_downloads}")

    blob.upload_from_filename(filename)
    blob.make_public()
    return blob.public_url, blob


def test():
    j = gcs.list_folder(
        bucket_folder=("4-6"),
        as_blob=False,  # If False : return as name
        include_self=False,  # If True : also return bucket_folder
        get_file=True,  # Get files in a list or not
        get_folder=False,  # Get Folder in a list or not, not include bucket_folder
        all_file=False,  # If True : Will get all files from folder and sub-folder(s)
    )
    bucket = storage_client.get_bucket("amazing_kids")
    l = []  # your bucket name
    for i in j:
        blob = bucket.blob(f"{i}")
        blob.make_public()
        l.append(blob.public_url)
    return l


def test1():
    j = gcs.list_folder(
        bucket_folder=("6-8"),
        as_blob=False,  # If False : return as name
        include_self=False,  # If True : also return bucket_folder
        get_file=True,  # Get files in a list or not
        get_folder=False,  # Get Folder in a list or not, not include bucket_folder
        all_file=False,  # If True : Will get all files from folder and sub-folder(s)
    )
    bucket = storage_client.get_bucket("amazing_kids")
    l = []  # your bucket name
    for i in j:
        blob = bucket.blob(f"{i}")
        blob.make_public()
        l.append(blob.public_url)
    return l
