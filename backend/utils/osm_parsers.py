def count_buildings(osm_data: str) -> int:
    """
    :param osm_data: Response from server parsed as osm (xml) data
    :return: building count if there is any building, 0 if not or None if
        something is wrong with osm_data and not contain only header
    """
    data = osm_data.strip()
    if data == '<osm version="0.6"/>':
        return 0

    building_count = data.count('k="building"')
    return building_count if building_count else None
