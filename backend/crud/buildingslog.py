from sqlalchemy.orm import Session

from backend.models.buildingslog import BuildingsLog
from backend.schemas.buildingslog import BuildingsLogCreate


def create_buildings_log(db: Session, buildings_log: BuildingsLogCreate):
    db_buildings_log = BuildingsLog(**buildings_log.dict())
    db.add(db_buildings_log)
    db.commit()
    db.refresh(db_buildings_log)

    return db_buildings_log
