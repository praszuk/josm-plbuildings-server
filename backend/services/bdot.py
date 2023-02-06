import logging

from json import JSONDecodeError

from backend.api.v2.deps import BuildingsNearestParams
from backend.core.config import settings
from backend.schemas.buildings_data import BuildingsData
from backend.services.base import BaseDataSourceService
from backend.models.enums import BuildingsDataSource, DataSourceFormat


class BDOTService(BaseDataSourceService):
    """
    BDOTService is responsible for getting buildings data from BDOT source
    which uses budynki.openstreetmap.org.pl site to get data.
    """
    FORMAT: DataSourceFormat = DataSourceFormat.GEOJSON
    DATA_SOURCE: BuildingsDataSource = BuildingsDataSource.BDOT

    async def fetch_nearest_building(
        self,
        nearest: BuildingsNearestParams
    ) -> None:
        url = f'{settings.BUDYNKI_SERVER_URL}' \
              '/josm_plugins/v2/nearest_building' \
              f'?lon={nearest.lon}' \
              f'&lat={nearest.lat}' \
              f'&search_distance={nearest.search_distance}'

        data = {}
        try:
            response = await self._client.get(url)
            data = response.json()
        except IOError as e:
            logging.warning(f'Error on downloading building from: {url} {e}')
        except JSONDecodeError as e:
            logging.warning(f'Error on parsing response: {data} {e}')

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
            data=self._buildings_data
        )

    @property
    def buildings_count(self) -> int:
        if self._buildings_data:
            return len(self._buildings_data.get('features', []))

        return 0
