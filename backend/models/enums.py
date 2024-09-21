from enum import Enum


class BuildingsDataSource(str, Enum):
    BDOT = 'BDOT'  # From 'budynki' server
    EGIB = 'EGiB'  # From 'egib-plbuildings' server


class DataSourceFormat(Enum):
    GEOJSON = 'geojson'
    OSMJSON = 'osmjson'
