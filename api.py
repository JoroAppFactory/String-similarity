import flask
import nltk
import json
import string
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from nltk.corpus import stopwords
from flask import request, jsonify
import difflib


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


@app.route('/autocorrect', methods=['POST'])
def autocorrect():
    # settings
    forbidden_words_default = []
    forbidden_distilleries_defaults = []
    word_size = 6
    cutoff = 0.75
    search_field = [
        "aberlour",
        "kavalan",
        "glen garioch",
        "michter",
        "glen grant",
        "royal lochnagar",
        "Big Peat",
        "ardgowan",
        "blair athol",
        "jim beam",
        "hazelburn",
        "longrow",
        "glen elgin",
        "compass box",
        "haig's",
        "buchanan's",
        "bell's",
        "ardnahoe",
        "ben wyvis",
        "breuckelen",
        "four roses",
        "bivrost",
        "north british",
        "kanosuke",
        "cardrona",
        "lindores abbey",
        "finlaggan",
        "gerston & auchnagie",
        "strathearn",
        "kaiyo",
        "annandale",
        "macallan",
        "hibiki suntory",
        "willett",
        "dalmore",
        "mars shinshu",
        "lagavulin",
        "fettercairn",
        "talisker",
        "1779",
        "beam suntory",
        "nikka",
        "benromach",
        "wild turkey",
        "ardbeg",
        "teaninich",
        "glonfarcias",
        "carsebridge",
        "glenfiddich",
        "convalmore",
        "glenmorangie",
        "midleton",
        "laphroaig",
        "linkwood",
        "rosebank",
        "naturally rich",
        "strathisla",
        "bimber",
        "beriach",
        "amrut",
        "glendronach",
        "bunnahabhain",
        "whyte & mackay",
        "bruichladdich",
        "heaven hill",
        "glenrothes",
        "high west",
        "nevada h&c",
        "hillside",
        "coleburn",
        "shizuoka",
        "old pulteney",
        "old forester",
        "glen mhor",
        "jameson",
        "kilkerran",
        "knockdhu",
        "daftmill",
        "dalwhinnie",
        "balvenie",
        "cola",
        "littlemill",
        "inchgower",
        "caledonian",
        "dallas dhu",
        "glen keith",
        "caperdonich",
        "mosstowie",
        "imperial",
        "garrison brothers",
        "sullivans cove",
        "teeling",
        "glen albyn",
        "tomintoul",
        "pittyvaich",
        "kentucky owl",
        "inverleven",
        "strathclyde",
        "garnheath",
        "ardnamurchan",
        "tamdhu",
        "balblair",
        "scapa",
        "north of scotland",
        "cragganmore",
        "jack daniels",
        "tomatin",
        "suntory whisky",
        "raasay",
        "dailuaine",
        "glenglassaugh",
        "port dundas",
        "lochside",
        "wolfburn",
        "glenlossie",
        "chita",
        "bushmills",
        "invergordon",
        "tormore",
        "clynelish",
        "glenallachie",
        "brown forman",
        "ambler",
        "glen scotia",
        "yamazakura",
        "orphan barrel",
        "barrell craft",
        "royal brackla",
        "edradour",
        "limestone branch",
        "ledaig",
        "tamnavulin",
        "cambus",
        "glenkinchie",
        "glen spey",
        "deanston",
        "ben nevis",
        "glengoyne",
        "torabhaig",
        "glen moray",
        "kilchoman",
        "glenturret",
        "speyburn",
        "glencadam",
        "kininvie",
        "benrinnes",
        "waterford",
        "whistlepig",
        "westland",
        "balcones",
        "nelsons green brier",
        "cardhu",
        "mclain kyne",
        "balmenach",
        "lakes",
        "penderyn",
        "jura",
        "cutwater",
        "akkeshi",
        "oban",
        "nc'nean",
        "tullamore",
        "barton 1792",
        "eden mill",
        "kingsbarns",
        "auchroisk",
        "braeval",
        "auchentoshan",
        "grants",
        "tuthilltown spirits",
        "mannochmore",
        "tullibardine",
        "copper rivet",
        "aberfeldy",
        "stronachie",
        "glenburgie",
        "white horse123",
        "kawasaki",
        "glendullan",
        "lux row",
        "aultmore",
        "new riff",
        "glenury",
        "magdalene",
        "millburn",
        "antiquary",
        "bardstown",
        "old carter",
        "macduff",
        "one eight",
        "western spirits",
        "boone",
        "cotswolds",
        "louisville",
        "jos a magnus",
        "proof wood ventures",
        "st augustine",
        "maker's mark",
        "strathmill",
        "ardmore",
        "bourbon 30",
        "filibuster",
        "smith bowman",
        "backbone",
        "glen flagler",
        "dalmunach",
        "woodford reserve",
        "finger lakes",
        "hiram walker",
        "high coast",
        "kinclaith",
        "glenlochy",
        "stitzel",
        "dornoch",
        "glenugie",
        "glencraig",
        "ailsa bay",
        "breckenridge",
        "schenley",
        "starward new world",
        "dads hat",
        "catskill",
        "cutty sark",
        "ranger creek",
        "boston harbor",
        "fremont mischief",
        "glenmore",
        "ladyburn",
        "crown royal",
        "cooley",
        "allt a bhainne",
        "prichards",
        "buffalo trace",
        "tobermory",
        "killyloch",
        "james e. pepper",
        "willowbank",
        "brora",
        "gasthof hirsch",
        "loch ewe",
        "abhainn dearg",
        "widow jane",
        "reservoir distillery",
        "blaum",
        "cleveland",
        "chattanooga",
        "arbikie",
        "coppersea",
        "three boys farm",
        "glen wyvis",
        "holyrood",
        "lagg",
        "borders",
        "inchdairnie",
        "american freedom",
        "ferintosh",
        "parkmore",
        "glenfyne",
        "bainbridge",
        "blue ridge",
        "glenfoyle",
        "bulleit",
        "miltonduff",
        "croftengea",
        "inchfad",
        "rhosdhu",
        "port ellen",
        "arran",
        "lochindaal",
        "glen avon",
        "mortlach",
        "craigellachie",
        "highland park",
        "dufft own",
        "glentauchers",
        "drumguish",
        "banff",
        "knockando",
        "1770",
        "girvan",
        "port charlotte",
        "dumbarton",
        "lagmern",
        "bladnoch",
        "north port",
        "springbank",
        "glenlivet",
        "loch lomond",
        "craigduff",
        "armore",
        "bardowie",
        "beninnes",
        "haig club",
        "dunglass",
        "ballechin",
        "glencraig",
        "octomore",
        "black bull",
        "ben bracken",
    ]

    # Request
    data = request.get_json()

    # Body
    input = data.get('input', '')
    forbidden_words = data.get('forbidden_words', '')
    forbidden_distilleries = data.get('forbidden_distilleries', '')
    cutoff_input = data.get('cutoff', '')

    if(cutoff_input != ''):
        cutoff = cutoff_input

    # forbidden words filtering
    forbidden_words_default.extend(forbidden_words)
    for w in forbidden_words_default:
        input = input.replace(w, '')

    # logic
    splitted_input = input.split(" ")
    splitted_input = filter(lambda x: len(x) >= word_size, splitted_input)

    output = []
    for word in splitted_input:
        currentResult = difflib.get_close_matches(
            word, search_field, cutoff=cutoff)
        for i in currentResult:
            output.append(i)

    output = list(set(output))

    # forbidden distilleries filtering
    forbidden_distilleries_defaults.extend(forbidden_distilleries)
    for word in forbidden_distilleries_defaults:
        if word in output:
            output.remove(word)

    return jsonify(output)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
