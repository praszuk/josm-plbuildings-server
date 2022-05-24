from pydantic import BaseModel, validator

from datetime import datetime
from typing import Optional

from backend.models.enums import BuildingsDataSource


class BuildingsLogBase(BaseModel):
    rq_recv_dt: datetime
    rq_duration_ms: int

    data_source: BuildingsDataSource
    lat: float
    lon: float

    building_count: Optional[int] = 0

    @validator('rq_duration_ms')
    def rq_duration_ms_gte_zero(cls, val):
        if val < 0:
            raise ValueError('must be gte 0')

        return val

    @validator('building_count')
    def building_count_gte_0_or_none(cls, val):
        if val is not None and val < 0:
            raise ValueError('must be gte 0 or None')


class BuildingsLogCreate(BuildingsLogBase):
    class Config:
        orm_mode = True
