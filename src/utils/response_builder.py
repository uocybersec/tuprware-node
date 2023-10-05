from flask import jsonify
from flask import Response

def create_reponse(**kwargs: any) -> Response:
    response = {}
    for key, value in kwargs.items():
        response[key] = value
    return jsonify(response)
