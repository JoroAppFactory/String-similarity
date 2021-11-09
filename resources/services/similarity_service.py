import string
import nltk
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from nltk.corpus import stopwords

nltk.download('stopwords')
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


# class Result:
#     def __init__(self, value, percentage):
#         self.value = value
#         self.percentage = percentage


def find(input, strings):
    results = []
    for x in strings:

        results.append(
            {"value": x, "percentage": get_similarity_percentage(input, x)})

        # results.append(
        #     Result(x, get_similarity_percentage(input, x)))

    results.sort(key=lambda x: x['percentage'], reverse=True)
    return {'input': input, 'strings': results}
