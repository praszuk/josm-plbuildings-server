from fastapi import APIRouter, Response
from httpx import AsyncClient

from backend.models.enums import BuildingsDataSource


router = APIRouter()


@router.get('')
async def get_nearest_building(
        lat: float,
        lon: float,
        data_source: BuildingsDataSource,
        search_distance: float = 3,
):
    """
    :param lat EPSG4386
    :param lon EPSG4386
    :param data_source source from which will be data obtained
    :param search_distance radius in meters
    """
    async with AsyncClient() as client:
        if data_source == BuildingsDataSource.BDOT:
            response = await client.get(
                'https://budynki.openstreetmap.org.pl'
                '/josm_plugins/nearest_building'
                f'?lon={lon}&lat={lat}&search_distance={search_distance}'
            )

            return Response(
                content=response.text,
                media_type='application/xml'
            )

        return Response(
            content='<osm version="0.6"/>',
            media_type='application/xml'
        )
