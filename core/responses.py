def success_response(data=None, message="Sucesso"):
    return {
        "status": "success",
        "message": message,
        "data": data
    }


def error_response(message="Erro"):
    return {
        "status": "error",
        "message": message
    }
