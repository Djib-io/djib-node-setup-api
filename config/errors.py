class ErrorMessages:
    InvalidRequest = {
        "status": -1,
        "message": "Invalid Request",
        "data": "The JSON sent is not a valid Request object."
    }
    MethodNotFound = {
        "status": -1,
        "message": "Method Not Found",
        "data": "The method does not exist / is not available."
    }
    InvalidParams = {
        "status": -1,
        "message": "Invalid Params",
        "data": "Invalid method parameter(s)."
    }
    InternalError = {
        "status": -1,
        "message": "Internal Error",
        "data": "Internal JSON-RPC error."
    }
    ServerError = {
        "status": -1,
        "message": "Server Error",
        "data": "Reserved for implementation-defined server-errors."
    }
