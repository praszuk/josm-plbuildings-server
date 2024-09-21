from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.api.deps import get_db
from backend.schemas.buildings_data import BuildingsData
from backend.services.buildings import BuildingsService

from .deps import BuildingAtParams

router = APIRouter()


@router.get('/')
async def get_building_at(
    location: BuildingAtParams = Depends(BuildingAtParams),
    db: Session = Depends(get_db),
) -> List[BuildingsData]:
    buildings_data = await BuildingsService(db).get_building_at(location)
    return buildings_data
