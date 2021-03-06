# General
from flask import Flask
from flask_restx import Api

# Resources
from resources.closest_match import ClosestMatchFromFile, ClosestMatch
from resources.auto_correct import Autocorrect
from resources.similarity import Similarity

app = Flask(__name__)
api = Api(app, version='1.0', title='Bevvy OCR API',
          description='Bevvy OCR API docs')

api.add_resource(ClosestMatch, '/match')
api.add_resource(ClosestMatchFromFile, '/matching_from_file')
api.add_resource(Autocorrect, '/autocorrect')
api.add_resource(Similarity, '/similarity')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
