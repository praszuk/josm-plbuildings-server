from pydantic import BaseModel

from typing import Any, Dict, Optional

from backend.models.enums import BuildingsDataSource, DataSourceFormat


class BuildingsData(BaseModel):
    """
    Response model for one datasource
    """
    source: BuildingsDataSource
    format: DataSourceFormat
    data: Optional[Dict[str, Any]]
