from pydantic import BaseModel

from backend.models.enums import BuildingsDataSource


class DataSourceProfile(BaseModel):
    """
    Response model for static DataSources profiles which are used
    by plbuildings plugin
    """

    name: str
    geometry: BuildingsDataSource
    tags: BuildingsDataSource
