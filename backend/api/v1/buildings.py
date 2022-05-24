from fastapi import APIRouter, Depends, Response
from httpx import AsyncClient
from sqlalchemy.orm import Session

from datetime import datetime

from backend.crud.buildingslog import create_buildings_log
from backend.models.enums import BuildingsDataSource
from backend.schemas.buildingslog import BuildingsLogCreate
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


@router.get('')
async def get_nearest_building(
        lat: float,
        lon: float,
        data_source: BuildingsDataSource,
        search_distance: float = 3,
        db: Session = Depends(get_db)
):
    """
    :param lat EPSG4386
    :param lon EPSG4386
    :param data_source source from which will be data obtained
    :param search_distance radius in meters
    :param db: database session
    """
    request_receive_dt = datetime.utcnow()
    response_data = '<osm version="0.6"/>'
    building_count = None

    async with AsyncClient() as client:

        if data_source == BuildingsDataSource.BDOT:
            response = await client.get(
                'https://budynki.openstreetmap.org.pl'
                '/josm_plugins/nearest_building'
                f'?lon={lon}&lat={lat}&search_distance={search_distance}'
            )
            response_data = response.text
            building_count = count_buildings(response_data)

        request_timedelta = datetime.utcnow() - request_receive_dt
        request_duration_ms = request_timedelta.total_seconds() * 1000

        create_buildings_log(
            db,
            buildings_log=BuildingsLogCreate(
                rq_recv_dt=request_receive_dt,
                rq_duration_ms=request_duration_ms,
                lat=lat,
                lon=lon,
                data_source=data_source,
                building_count=building_count,
            )
        )

        return Response(content=response_data, media_type='application/xml')
