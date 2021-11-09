# General
from flask_restx import Resource
from flask import request

# Resources
from resources.services.similarity_service import find


class Similarity(Resource):
    @classmethod
    def post(cls):
        data = request.get_json()
        input = data.get('input', '')
        strings = data.get('strings', '')

        try:
            obj = find(input, strings)
            return obj, 200
        except:
            return {'status': 'failed', 'message': 'The similarity failed.'}, 202
