import cv2
import numpy as np
from fastapi import APIRouter, UploadFile, File, Depends
from starlette.responses import RedirectResponse

from security.authorize import oauth2_scheme, get_current_user, credentials_exception

"""
    routers for attendance marking
"""

router = APIRouter(
    prefix="/api/attendance",
    tags=["attendance"],
    responses={404: {"description": "The requested page was not found"}},
)


@router.post("/facerec")
async def mark_by_face(
        image: UploadFile = File(...),
        token: str = Depends(oauth2_scheme)
):
    """
    
    :param image:
    :param token:
    :return:
    """
    if image.content_type != "image/jpeg":
        return "Only jpeg images are supported"

    if get_current_user(token) is None:
        raise credentials_exception

    contents = await image.read()

    nparray = np.fromstring(contents, np.uint8)
    img = cv2.imdecode(nparray, cv2.IMREAD_COLOR)

    # TODO evaluate image

    # TODO mark attendance if evaluated for a user

    # TODO redirect attendance page
    return RedirectResponse("/home", status_code=200)
