from logging import getLogger
from json import JSONDecodeError

from httpx import HTTPError

from backend.api.v2.deps import BuildingAtParams
from backend.core.config import settings
from backend.models.enums import BuildingsDataSource, DataSourceFormat
from backend.schemas.buildings_data import BuildingsData
from backend.services.base import BaseDataSourceService


logger = getLogger(settings.DEFAULT_LOGGER)


class BDOTService(BaseDataSourceService):
    """
    BDOTService is responsible for getting buildings data from BDOT source
    which uses budynki.openstreetmap.org.pl site to get data.
    """

    FORMAT: DataSourceFormat = DataSourceFormat.GEOJSON
    DATA_SOURCE: BuildingsDataSource = BuildingsDataSource.BDOT
    SEARCH_DISTANCE = 1  # meters

    async def fetch_building_at(self, location: BuildingAtParams) -> None:
        url = (
            f'{settings.BUDYNKI_SERVER_URL}'
            '/josm_plugins/v2/nearest_building'
            f'?lon={location.lon}'
            f'&lat={location.lat}'
            f'&search_distance={self.SEARCH_DISTANCE}'
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

        # Move OSM tags from nested key ("tags") to upper key ("properties")
        for feature in data['features']:
            feature['properties'].update(feature['properties'].pop('tags'))

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
