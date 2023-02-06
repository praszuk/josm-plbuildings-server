from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from typing import List

from backend.api.deps import get_db
from backend.services.buildings import BuildingsService
from backend.schemas.buildings_data import  BuildingsData

from .deps import BuildingsNearestParams


router = APIRouter()


@router.get('/nearest')
async def get_nearest_building(
    nearest: BuildingsNearestParams = Depends(BuildingsNearestParams),
    db: Session = Depends(get_db)
) -> List[BuildingsData]:
    buildings_data = await BuildingsService(db).get_nearest_building(nearest)
    return buildings_data
