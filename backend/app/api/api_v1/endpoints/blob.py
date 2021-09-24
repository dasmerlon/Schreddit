import os
from uuid import uuid4

from azure.storage.blob import BlobClient, ContentSettings
from fastapi import APIRouter, File, UploadFile, status
from pydantic import HttpUrl

from app.core.config import settings

router = APIRouter()


@router.post(
    "/upload",
    name="Upload Media",
    response_model=HttpUrl,
    status_code=status.HTTP_200_OK,
)
def upload(file: UploadFile = File(...)):
    """
    Upload a video or image as a Blob to Azure Storage.
    Returns the URL of the saved file.

    - `file` : the file to be uploaded
    """
    split = os.path.splitext(file.filename)
    file_extension = split[1]
    if file.content_type.startswith("image"):
        container = "images"
    elif file.content_type.startswith("video"):
        container = "videos"
    blob = BlobClient.from_connection_string(
        conn_str=settings.AZURE_STORAGE_CREDENTIALS,
        container_name=container,
        blob_name=uuid4().hex + file_extension,
    )
    content_settings = ContentSettings(content_type=file.content_type)
    blob.upload_blob(file.file, content_settings=content_settings)

    return blob.url
