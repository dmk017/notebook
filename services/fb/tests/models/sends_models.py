import json
from .data_models import API_BASE_URL


def _send_request(client, method, endpoint, request_body=None, args=None):
    params = {
        "args": ",".join(args) if args else "",
        "kwargs": json.dumps(request_body) if request_body else "{}",
    }
    return client.request(method, endpoint, json=request_body, params=params)


def send_add_model_request(client, request_body, args=[]):
    return _send_request(client, "POST", API_BASE_URL, request_body, args)


def send_delete_model_request(client, request_body, id, args=[]):
    return _send_request(client, "DELETE", f"{API_BASE_URL}/{id}", request_body, args)


def send_get_models_request(client, request_body, page, limit, args=[]):
    return _send_request(
        client,
        "POST",
        f"{API_BASE_URL}/list?page={page}&limit={limit}",
        request_body,
        args,
    )


def send_get_model_by_id_request(client, request_body, id, args=[]):
    return _send_request(client, "GET", f"{API_BASE_URL}/{id}", request_body, args)


def send_get_model_history_request(client, request_body, id, args=[]):
    return _send_request(
        client, "GET", f"{API_BASE_URL}/{id}/history", request_body, args
    )


def send_get_recove_model_request(client, request_body, id, args=[]):
    return _send_request(
        client, "POST", f"{API_BASE_URL}/{id}/recove", request_body, args
    )


def send_update_model_request(client, request_body, id, args=[]):
    return _send_request(client, "PUT", f"{API_BASE_URL}/{id}", request_body, args)


def send_get_example_file_model_request(client, request_body, id, args=[]):
    return _send_request(
        client, "GET", f"{API_BASE_URL}/{id}/example/file", request_body, args
    )
