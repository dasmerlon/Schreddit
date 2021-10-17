import mimetypes
from uuid import uuid4

import magic
from azure.storage.blob import BlobClient, ContentSettings
from fastapi import APIRouter, Depends, File, UploadFile, status
from pydantic import HttpUrl

from app import models
from app.api import deps
from app.api.api_v1.exceptions import ForbiddenFiletypeException
from app.core.config import settings

router = APIRouter()


@router.post(
    "/upload",
    name="Upload media",
    response_model=HttpUrl,
    status_code=status.HTTP_200_OK,
)
def upload(
    file: UploadFile = File(...),
    current_user: models.User = Depends(deps.get_current_user),
):
    """
    Upload a video or image as a BLOB and return the URL of the uploaded file.

    - `file`: the file to be uploaded
    """
    # get true mimetype of file
    mime = magic.from_buffer(file.file.read(2048), mime=True)
    file.file.seek(0)

    # pick correct storage container
    if mime.startswith("image"):
        container = "images"
    elif file.content_type.startswith("video"):
        container = "videos"
    else:
        raise ForbiddenFiletypeException

    # upload file with a generated filename and the proper file extension
    blob = BlobClient.from_connection_string(
        conn_str=settings.AZURE_STORAGE_CREDENTIALS,
        container_name=container,
        blob_name=uuid4().hex + mimetypes.guess_extension(mime),
    )
    metadata = {"user_uid": current_user.uid}
    content_settings = ContentSettings(content_type=mime)
    blob.upload_blob(file.file, metadata=metadata, content_settings=content_settings)

    return blob.url
