from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.api.deps import get_db
from backend.services.buildings import BuildingsService

from .deps import BuildingsNearestParams


router = APIRouter()


@router.get('/nearest')
async def get_nearest_building(
    nearest: BuildingsNearestParams = Depends(BuildingsNearestParams),
    db: Session = Depends(get_db)
):
    # TODO temporary – it should return object from schema instead raw data
    raw_result = await BuildingsService(db).get_nearest_building(nearest)
    return raw_result
