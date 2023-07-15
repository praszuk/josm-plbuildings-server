from typing import List

from fastapi import APIRouter

from backend.models.enums import BuildingsDataSource
from backend.schemas.data_source_profile import DataSourceProfile

router = APIRouter()


DATA_SOURCES_PROFILES = [
    DataSourceProfile(
        name='BDOT',
        geometry=BuildingsDataSource.BDOT,
        tags=BuildingsDataSource.BDOT,
    ),
    DataSourceProfile(
        name='EGiB',
        geometry=BuildingsDataSource.EGIB,
        tags=BuildingsDataSource.EGIB,
    ),
    DataSourceProfile(
        name='BDOT/EGiB',
        geometry=BuildingsDataSource.EGIB,
        tags=BuildingsDataSource.BDOT,
    ),
]


@router.get('/')
async def get_data_sources_profiles() -> List[DataSourceProfile]:
    return DATA_SOURCES_PROFILES
