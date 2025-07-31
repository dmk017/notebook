from src.objects.objects_router_api_schema import SearchFiltersList, SearchFilter
from typing import Optional

def parse_filters_auth(filters: list[SearchFiltersList], search_name: str) -> dict:
    found_values = []
    for filter in filters:
        found_values.append(parse_filter_group_auth(filter, search_name))

    return {search_name: [value for value in flatten(found_values) if value is not None]}

def parse_filter_group_auth(search_filters_list: SearchFiltersList, search_name: str) -> Optional[str]:
    values = []
    for condition in search_filters_list.conditions:
        if condition.type == "isolated":
            values.append(parse_filter_isolated_auth(condition, search_name))
        if condition.type == "group":
            values.append(parse_filter_group_auth(condition, search_name))
    return values

def parse_filter_isolated_auth(search_filter: SearchFilter, search_name: str) -> Optional[str]:
    if search_filter.property == search_name:
        return search_filter.value
    return None

def flatten(nested_list: list) -> list:
    flat_list = []
    for item in nested_list:
        if isinstance(item, list):
            flat_list.extend(flatten(item))
        else:
            flat_list.append(item)
    return flat_list
