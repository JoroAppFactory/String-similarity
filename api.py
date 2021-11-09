# General
import json
from flask import Flask
from flask_restx import Api

# Resources
from resources.closest_match import ClosestMatchFromFile, ClosestMatch
from resources.auto_correct import Autocorrect
from resources.similarity import Similarity
# from resources.services.similarity_service import Result

app = Flask(__name__)

# class CustomEncoder(json.JSONEncoder):
#     def default(self, obj):
#         if isinstance(obj, Result):
#             return {"value": obj.value, "percentage": obj.percentage}
#         return json.JSONEncoder.default(self, obj)

# app.json_encoder = CustomEncoder

api = Api(app, version='1.0', title='Bevvy OCR API',
          description='Bevvy OCR API docs')



api.add_resource(ClosestMatch, '/match/')
api.add_resource(ClosestMatchFromFile, '/matching_from_file/')
api.add_resource(Autocorrect, '/autocorrect/')
api.add_resource(Similarity, '/similarity/')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
