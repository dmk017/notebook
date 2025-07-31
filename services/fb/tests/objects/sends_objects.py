import json
from .data_objects import API_BASE_URL


def _send_request(client, method, endpoint, request_body=None, args=None, files=None):
    params = {
        "args": ",".join(args) if args else "",
        "kwargs": json.dumps(request_body) if request_body else "{}",
    }
    return client.request(
        method, endpoint, json=request_body, params=params, files=files
    )


def send_add_object_request(client, request_body, args=[]):
    return _send_request(client, "POST", API_BASE_URL, request_body, args)


def send_get_object_request(client, request_body, id, args=[]):
    return _send_request(client, "GET", f"{API_BASE_URL}/{id}", request_body, args)


def send_get_all_objects_request(client, request_body, page, limit, args=[]):
    return _send_request(
        client, "GET", f"{API_BASE_URL}?page={page}&limit={limit}", request_body, args
    )


def send_get_count_objects_request(client, request_body, page, limit, args=[]):
    return _send_request(
        client,
        "GET",
        f"{API_BASE_URL}/count?page={page}&limit={limit}",
        request_body,
        args,
    )


def send_approve_objects_request(client, request_body, args=[]):
    return _send_request(client, "PUT", f"{API_BASE_URL}/approve", request_body, args)


def send_decline_objects_request(client, request_body, args=[]):
    return _send_request(client, "PUT", f"{API_BASE_URL}/decline", request_body, args)


def send_search_objects_request(client, request_body, args=[]):
    return _send_request(client, "POST", f"{API_BASE_URL}/search", request_body, args)


def send_upload_file_request(client, files=None, request_body={}, args=[]):
    return _send_request(
        client, "POST", f"{API_BASE_URL}/package/file", request_body, args, files
    )


def send_unloading_objects(client, request_body, args=[]):
    return _send_request(
        client, "POST", f"{API_BASE_URL}/unloading", request_body, args
    )
