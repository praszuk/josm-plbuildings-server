from sqlalchemy import (
    BigInteger,
    CheckConstraint,
    Column,
    DateTime,
    Enum,
    Float,
    Integer
)

from backend.database.base import Base
from .enums import BuildingsDataSource


class BuildingsLog(Base):
    __tablename__ = 'buildings_logs'
    __table_args__ = (
        CheckConstraint('rq_duration_ms >= 0'),
        CheckConstraint('building_count is null or building_count >= 0'),
    )
    id = Column(BigInteger, primary_key=True)
    rq_recv_dt = Column(DateTime(timezone=True), nullable=False)
    rq_duration_ms = Column(Integer, nullable=False)

    data_source = Column(Enum(BuildingsDataSource), nullable=False)
    lat = Column(Float, nullable=False)
    lon = Column(Float, nullable=False)

    building_count = Column(Integer, default=0, nullable=True)
