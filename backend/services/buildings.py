import asyncio
from datetime import datetime
from typing import List

from httpx import AsyncClient

from backend.api.v2.deps import BuildingAtParams
from backend.crud.buildings_log import create_buildings_log
from backend.models.enums import BuildingsDataSource
from backend.schemas.buildings_data import BuildingsData
from backend.schemas.buildings_log import BuildingsLogCreate
from backend.services.base import BaseService
from backend.services.bdot import BDOTService
from backend.services.egib import EGIBService


class BuildingsService(BaseService):
    async def get_building_at(self, location: BuildingAtParams) -> List[BuildingsData]:
        request_receive_dt = datetime.utcnow()

        result_buildings_data = []
        building_count = 0

        services = []
        async with AsyncClient() as client:
            if BuildingsDataSource.BDOT in location.data_sources:
                services.append(BDOTService(client))

            if BuildingsDataSource.EGIB in location.data_sources:
                services.append(EGIBService(client))

            await asyncio.gather(*[s.fetch_building_at(location) for s in services])

            for service in services:
                result_buildings_data.append(service.buildings_data)
                building_count += service.buildings_count

        request_timedelta = datetime.utcnow() - request_receive_dt
        request_duration_ms = request_timedelta.total_seconds() * 1000

        create_buildings_log(
            self.db,
            buildings_log=BuildingsLogCreate(
                rq_recv_dt=request_receive_dt,
                rq_duration_ms=int(request_duration_ms),
                lat=location.lat,
                lon=location.lon,
                data_sources=location.data_sources,
                building_count=building_count,
            ),
        )

        return result_buildings_data
