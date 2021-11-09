# General
from flask_restx import Resource
from flask import request

# Service
from resources.services.autocorrect_service import run_autocorrect


class Autocorrect(Resource):
    @classmethod
    def post(cls):
        data = request.get_json()
        input = data.get('input', '')
        forbidden_words = data.get('forbidden_words', '')
        forbidden_distilleries = data.get('forbidden_distilleries', '')
        cutoff_input = data.get('cutoff', '')

        try:
            obj = run_autocorrect(input, forbidden_words,
                                  forbidden_distilleries, cutoff_input)
            return obj, 200
        except:
            return {'status': 'failed', 'message': 'The autocorrect failed.'}, 202
