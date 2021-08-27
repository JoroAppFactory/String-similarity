import flask
import nltk
import json
import string
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from nltk.corpus import stopwords
from flask import request, jsonify


class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Result):
            return {"value": obj.value, "percentage": obj.percentage}
        # Let the base class handle the problem.
        return json.JSONEncoder.default(self, obj)


class Result:
    def __init__(self, value, percentage):
        self.value = value
        self.percentage = percentage


app = flask.Flask(__name__)
app.config["DEBUG"] = True
app.json_encoder = CustomEncoder

# nltk.download('stopwords')
stopwords = stopwords.words('english')


def clean_string(text):
    text = ''.join([word for word in text if word not in string.punctuation])
    text = text.lower()
    text = ' '.join([word for word in text.split() if word not in stopwords])

    return text


def cosine_sim_vectors(vec1, vec2):
    vec1 = vec1.reshape(1, -1)
    vec2 = vec2.reshape(1, -1)

    return cosine_similarity(vec1, vec2)[0][0]


def get_similarity_percentage(str1, str2):
    sentences = [
        str1,
        str2
    ]

    cleaned = list(map(clean_string, sentences))
    vectorizer = CountVectorizer().fit_transform(cleaned)
    vectors = vectorizer.toarray()

    percentage = cosine_sim_vectors(vectors[0], vectors[1])
    return percentage


@app.route('/test', methods=['GET'])
def test():
    return "<h1>FOR TEST PURPOSE</h1><p>Ignore this...</p>"

@app.route('/similarity', methods=['POST'])
def similarity():
    data = request.get_json()
    input = data.get('input', '')
    strings = data.get('strings', '')

    results = []

    for x in strings:
        results.append(Result(x, get_similarity_percentage(input, x)))

    results.sort(key=lambda x: x.percentage, reverse=True)

    return jsonify({"input": input, "strings": results})


if __name__ == "__main__":
  app.run(host='0.0.0.0', port=5000)


