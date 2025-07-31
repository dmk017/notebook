from datetime import datetime
from src.objects.objects_router_api_schema import SearchFilter, SearchFiltersList
from src.objects.data.objects_repository import decode_to_status_filter
from src.models import models_service
from src.utils.mongo import PydanticObjectId


def parse_filter_isolated(search_filter: SearchFilter):
    if search_filter.property == "_id":
        search_filter.value = PydanticObjectId(search_filter.value)
    if search_filter.property == "owner_id":
        search_filter.value = str(search_filter.value)
    if search_filter.property == "model_id":
        models = models_service.get_model_history(search_filter.value)
        search_filter.value = list(map(lambda m: PydanticObjectId(m.id), models))
        search_filter.operator = "in"
    if search_filter.property == 'status':
        value = decode_to_status_filter(search_filter.value)
        return [{'status.approve_at': value[0]}, {'status.decline_at': value[1]}]
    if search_filter.property == 'created_at':
        search_filter.value = datetime.fromisoformat(search_filter.value)
    if search_filter.operator == "": 
        return {search_filter.property: search_filter.value}
    return {search_filter.property: { f"${search_filter.operator}": search_filter.value}}

def parse_filter_group(search_filters_list: SearchFiltersList):
    result = {f"${search_filters_list.group.lower()}": []}
    for condition in search_filters_list.conditions:
        if condition.type == "isolated":
            values = parse_filter_isolated(condition)
            if type(values) is list:
                for val in values:
                    result[f"${search_filters_list.group.lower()}"].append(val)
            else:
                result[f"${search_filters_list.group.lower()}"].append(values)
            
        if condition.type == "group":
            values = parse_filter_group(condition)
            if type(values) is list:
                for val in values:
                    result[f"${search_filters_list.group.lower()}"].append(val)
            else:
                result[f"${search_filters_list.group.lower()}"].append(values)
    return result


def parse_filters(filters) -> dict:
    filtersOr = {}
    filtersAnd = {}
    for filter in filters:
        if filter.group == 'AND':
            filtersAnd = parse_filter_group(filter)
        else:
            filtersOr = parse_filter_group(filter)
    return {'filtersAnd': filtersAnd, 'filtersOr': filtersOr}