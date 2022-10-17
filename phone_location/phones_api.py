from fastapi import APIRouter
from .get_phone_location import get_phone_locaion
from tools.record_log import recordLog

logger = recordLog()

router = APIRouter(
    prefix="/phones",
    tags=["phones"],
    responses={404: {"description": "Not Found"}}
)


@router.get("/msg/{phone_number}")
async def get_msg(phone_number: str):
    gpl = get_phone_locaion(phone_number)
    logger.info("")
    return gpl.get_phone_json_msg()


@router.get("/province/{phone_number}")
async def get_msg(phone_number: str):
    gpl = get_phone_locaion(phone_number)
    # return {"province": gpl.get_phone_province()}
    return gpl.get_phone_province()
