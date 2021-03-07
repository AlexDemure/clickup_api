from .utils import decode_json_data_from_base64


def login_success(request) -> tuple:
    """Webhook EndPoint для получения уведомлений от сервисов что клиент успешно авторизировался в системе."""
    try:
        state = decode_json_data_from_base64(request.query.get("state"))
        code = request.query.get("code")
    except Exception as e:
        raise ValueError(str(e))

    return code, state
