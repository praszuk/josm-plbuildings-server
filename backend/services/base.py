from abc import ABC, abstractmethod

from httpx import AsyncClient
from sqlalchemy.orm import Session

from backend.api.v2.deps import BuildingAtParams
from backend.models.enums import BuildingsDataSource, DataSourceFormat
from backend.schemas.buildings_data import BuildingsData


class BaseService:
    def __init__(self, db: Session):
        self.db = db


class BaseDataSourceService(ABC):
    FORMAT: DataSourceFormat
    DATA_SOURCE: BuildingsDataSource
    TIMEOUT = 10  # seconds

    def __init__(self, client: AsyncClient):
        assert self.FORMAT is not None
        assert self.DATA_SOURCE is not None

        self._client = client
        self._buildings_data = None

    @property
    @abstractmethod
    def buildings_data(self) -> BuildingsData: ...

    @property
    @abstractmethod
    def buildings_count(self) -> int: ...

    @abstractmethod
    async def fetch_building_at(self, location: BuildingAtParams) -> dict: ...
