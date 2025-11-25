from flask import jsonify
from datetime import datetime

def success_response(data=None, message="Success", status_code=200):
    response = {
        "success": True,
        "message": message,
        "timestamp": datetime.now().isoformat()
    }
    if data is not None:
        response["data"] = data
    return jsonify(response), status_code

def error_response(message="Error", status_code=400, error_type="BadRequest"):
    response = {
        "success": False,
        "error": message,
        "error_type": error_type,
        "timestamp": datetime.now().isoformat()
    }
    return jsonify(response), status_code
