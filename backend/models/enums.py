from enum import Enum


class BuildingsDataSource(str, Enum):
    BDOT = 'bdot'  # From 'budynki' server
    EGIB = 'egib'  # From 'egib-plbuildings' server


class DataSourceFormat(Enum):
    GEOJSON = 'geojson'
    OSMJSON = 'osmjson'
