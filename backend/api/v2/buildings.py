from fastapi import APIRouter, Depends, Query
from httpx import AsyncClient
from sqlalchemy.orm import Session

from datetime import datetime
from typing import List

from backend.core.config import settings
from backend.crud.buildings_log import create_buildings_log
from backend.models.enums import BuildingsDataSource
from backend.schemas.buildings_log import BuildingsLogCreate
from backend.api.deps import get_db


router = APIRouter()


def count_buildings(osm_data: str) -> int:
    """
    :param osm_data: Response from server parsed as osm (xml) data
    :return: building count if there is any building, 0 if not or None if
        something is wrong with osm_data and not contain only header
    """
    data = osm_data.strip()
    if data == '<osm version="0.6"/>':
        return 0

    building_count = data.count('k="building"')
    return building_count if building_count else None


@router.get('/nearest')
async def get_nearest_building(
        data_sources: List[BuildingsDataSource] = Query(),
        lat: float = Query(gt=-90, lt=90),
        lon: float = Query(gt=-180, lt=180),
        search_distance: float = Query(3, gt=0),
        db: Session = Depends(get_db)
):
    """
    :param data_sources: sources from which will be data obtained
    :param lat: EPSG4326
    :param lon: EPSG4326
    :param search_distance: radius in meters
    :param db: database session
    """
    request_receive_dt = datetime.utcnow()

    result_data = {}
    # empty_osm_data = '<osm version="0.6"/>'

    async with AsyncClient() as client:
        building_count = 0
        if BuildingsDataSource.BDOT.value in data_sources:
            response = await client.get(
                f'{settings.BUDYNKI_SERVER_URL}'
                '/josm_plugins/nearest_building'
                f'?lon={lon}&lat={lat}&search_distance={search_distance}'
            )
            result_data[BuildingsDataSource.BDOT.value] = response.text
            building_count = count_buildings(response.text)

        request_timedelta = datetime.utcnow() - request_receive_dt
        request_duration_ms = request_timedelta.total_seconds() * 1000

        if BuildingsDataSource.EGIB.value in data_sources:
            # TODO
            pass

        create_buildings_log(
            db,
            buildings_log=BuildingsLogCreate(
                rq_recv_dt=request_receive_dt,
                rq_duration_ms=request_duration_ms,
                lat=lat,
                lon=lon,
                data_sources=data_sources,
                building_count=building_count,
            )
        )
        return result_data
