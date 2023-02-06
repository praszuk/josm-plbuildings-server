from enum import Enum


class BuildingsDataSource(str, Enum):
    BDOT = 'bdot'  # From 'budynki' site
    EGIB = 'egib'  # From WFSes gugik.gov.pl services (in feature)


class DataSourceFormat(Enum):
    GEOJSON = 'geojson'
    OSMJSON = 'osmjson'
