from logging import getLogger
from json import JSONDecodeError

from httpx import HTTPError

from backend.api.v2.deps import BuildingAtParams
from backend.core.config import settings
from backend.models.enums import BuildingsDataSource, DataSourceFormat
from backend.schemas.buildings_data import BuildingsData
from backend.services.base import BaseDataSourceService


logger = getLogger(settings.DEFAULT_LOGGER)


class EGIBService(BaseDataSourceService):
    """
    EGIBService is responsible for getting buildings data from EGiB source
    which uses external EGIB_PLBUILDINGS server to get data.
    """

    FORMAT: DataSourceFormat = DataSourceFormat.GEOJSON
    DATA_SOURCE: BuildingsDataSource = BuildingsDataSource.EGIB

    async def fetch_building_at(self, location: BuildingAtParams) -> None:
        url = (
            f'{settings.EGIB_PLBUILDINGS_SERVER_URL}'
            '/api/v1/buildings/'
            f'?lat={location.lat}'
            f'&lon={location.lon}'
        )

        data = {}
        try:
            response = await self._client.get(url, timeout=self.TIMEOUT)
            data = response.json()
        except HTTPError as e:
            logger.error(f'Error on downloading building from: {url} {e}')
        except JSONDecodeError as e:
            logger.error(f'Error on parsing response: {data} {e}')

        # empty response or unexpected server error
        if 'features' not in data:
            return

        self._buildings_data = data

    @property
    def buildings_data(self) -> BuildingsData:
        return BuildingsData(
            format=self.FORMAT.value,
            source=self.DATA_SOURCE.value,
            data=self._buildings_data,
        )

    @property
    def buildings_count(self) -> int:
        if self._buildings_data:
            return len(self._buildings_data.get('features', []))

        return 0
