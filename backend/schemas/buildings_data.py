from typing import Any

from pydantic import BaseModel

from backend.models.enums import BuildingsDataSource, DataSourceFormat


class BuildingsData(BaseModel):
    """
    Response model for one datasource
    """

    source: BuildingsDataSource
    format: DataSourceFormat
    data: dict[str, Any] | None
