
def Response(json_data, message, error):
    return {
        "data": json_data,
        "message": message,
        "error": error
    }

