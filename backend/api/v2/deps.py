from fastapi import Query

from typing import List

from backend.models.enums import BuildingsDataSource


class BuildingsNearestParams:
    def __init__(
        self,
        data_sources: List[BuildingsDataSource] = Query(),
        lat: float = Query(gt=-90, lt=90),
        lon: float = Query(gt=-180, lt=180),
        search_distance: float = Query(3, gt=0)
    ):
        self.data_sources = data_sources
        self.lat = lat
        self.lon = lon
        self.search_distance = search_distance
