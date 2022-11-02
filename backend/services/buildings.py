from httpx import AsyncClient

from datetime import datetime

from backend.api.v2.deps import BuildingsNearestParams
from backend.core.config import settings
from backend.crud.buildings_log import create_buildings_log
from backend.models.enums import BuildingsDataSource
from backend.schemas.buildings_log import BuildingsLogCreate
from backend.services.base import BaseService
from backend.utils import osm_parsers


class BuildingsService(BaseService):
    async def get_nearest_building(self, nearest: BuildingsNearestParams):
        request_receive_dt = datetime.utcnow()

        result_data = {}
        # empty_osm_data = '<osm version="0.6"/>'

        async with AsyncClient() as client:
            building_count = 0
            if BuildingsDataSource.BDOT.value in nearest.data_sources:
                response = await client.get(
                    f'{settings.BUDYNKI_SERVER_URL}'
                    '/josm_plugins/nearest_building'
                    f'?lon={nearest.lon}'
                    f'&lat={nearest.lat}'
                    f'&search_distance={nearest.search_distance}'
                )
                result_data[BuildingsDataSource.BDOT.value] = response.text
                building_count = osm_parsers.count_buildings(response.text)

            request_timedelta = datetime.utcnow() - request_receive_dt
            request_duration_ms = request_timedelta.total_seconds() * 1000

            if BuildingsDataSource.EGIB.value in nearest.data_sources:
                # TODO
                pass

            create_buildings_log(
                self.db,
                buildings_log=BuildingsLogCreate(
                    rq_recv_dt=request_receive_dt,
                    rq_duration_ms=request_duration_ms,
                    lat=nearest.lat,
                    lon=nearest.lon,
                    data_sources=nearest.data_sources,
                    building_count=building_count,
                )
            )

        return result_data
