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
    word_size = 6
    cutoff = 0.75
    search_field = ["bayer","bühler","druffel","ehringhausen","eiger","feller","friz","gruel","hack","henrich","hubertus vallendar","höck","höhler","hübner","kramer","lanz","lettner","liebl","lippert","ludwig faber","ro&szlig;mann","roder","roman kraus","schwab","spielberger","stapf","steinlein","volker theurer im gasthof lamm","ziegler","zürcher","&aelig;ppeltreow","1000 hills","10th mountain","10th street","12.05","1769","18th street","2bar","3 badge","3 howls","45th parallel","5 artisan","52eighty","5nines","66 gilead","7k","a. smith bowman","aare bier","aber falls","aber falls","aberfeldy","aberlour","abhainn dearg","acha","acre","adams","adelaide hills","adirondack","adnams","aero whisky","ag&aacute;rdi p&aacute;linkafőzde","agder","agitator","aichinger","ailsa bay","aioi unibio","aisling","akkeshi","alambik","alaska","albany","alberta","alchemy","alde gott","aldea","alex clark","alexander biselli","all points west","alley 6","allgäu","allt a bhainne","alpenwhisky","alpirsbacher","alt enderle","alte","alte haus a. wecklein","altore","altstadthof","amador","ambler","american fifth","american freedom","amrut","anchor","andalusia","anglesey","annandale","anno","anno 1940","antiquary","appalachian","applewood","arbikie","arbutus","archie rose","arcola","arcus","ardbeg","ardgowan","ardmore","ardnahoe","ardnamurchan","arizona","arizona high spirits","armagnac veuve goudoulin","arnsteiner","arran","artist in residence","asaka","ascendant","asheville","astidama","asw","auchentoshan","auchnagie","auchroisk","august dinsing","augustus rex","aultmore","aurora spirit","authentic seacoast","avadis","axe and the oak","ayutla","az granata","bachgau","backbone","backwoods","backwoods craft spirits","bad dog","badmils black","bainbridge","baker williams","bakery hill","balblair","balcones","ballantine","ballykeefe","balmenach","baltimore","balvenie","bandon","banff","bankhall","baoilleach","bardstown","bardstown","baronie","barrel house","barrell","barton 1792","basilico","basque moonshiners","batch 206","bauhöfer","baumgartner","bay area","beam suntory","bear wallow","belgian owl","belgrove","bell's","belle isle","bellerhof","belmont","belmont farm","ben nevis","ben wyvis","benachie","bendistillery","bendt","benriach","benrinnes","benromach","bent","bergslagens","bergwelt","berkshire mountain","bernheim","bernheim","bertrand","betz","bflo","bieri bauernhof","big bottom","bimber","bimber","biolandhof köhler","biospirits","birgitta","birkenhof","birkenhof","bischof","bivrost","bières michard","black bear","black bridge","black button","black canyon","black dirt","black draft","black gate","black heron","black velvet","black's","blackfish","blackmoon","blackwater","bladnoch","blair athol","blanton's","blaue maus","blaum","blinking owl","blue monkey","blue ridge","blue sky","blue spirits","bluegrass","boann","bodega abasolo","bogner","bolanachi","boldizar","bondi","bone spirits","booker's","boone","boone county","boone county jail","boplaas","borchert","borders","bosch edelbrand","bossche stokers","boston harbor","bouck brothers","bourbon 30","bow more","bow street","bows","box Destilleri","braeckman","braeval","brain brew","brandhaus 7","branger","brasch","braugasthof","braunstein","breckenridge","brehmer","brenne","breuckelen","brickway","broad branch","broadbent","broger","broken bones","bronckhorst","brora","brother justus","browar ciechan","brown forman","bruckners erz bräu","brugse","bruichladdich","brunschwiler","brænderiet limfjorden","bröderna bommen","brûlerie du revermont","buchanan's","buffalo trace","bull run","bulleit","bully boy","bunnahabhain","burgdorfer","burger","burke's","burwood","bus","bushmills","békési manufaktura","böckenhoff","böckl","böttchehof","cadushy","caiseal","caldera","caledonian","cali","cambus","cameronbridge","camp 1805","Camus","canadian mist","caol ila","caperdonich","carbon glacier","cardhu","cardrona","caroni","carsebridge","cascade hollow","castan","castle & key","cathead","catoctin creek","catskill","cave de la crausaz","cedar ridge","central city","central standard","ch","chambers bay","chankaska spirits","charbay","charles medley","charlier","charpentier","chateau du breuil","chattanooga","cherry rocher","chicago","chichibu","chicken cock","chicken hill","chief's son","chita","chivas","chugoku jozo","churfirsten","circumstance","cirka","claeyssens de wambrechies","clara hof","clear creek","cleveland","cley","clonakilty","clydeside","clynelish","clynelish","coleburn","coleraine","coles","collier","colonel e.h. taylor","colorado gold","compass box","conecuh ridge","connacht","continental distillers","convalmore","cooley","cooper king","cooperstown","copenhagen","copper fox","copper rebublic","copper rivet","copper run","coppersea","copperworks","corby spirit","corio","cornelius pass roadhouse","corowa","corra linn","corsair","cotswolds","courvoisier","cradle mountain","craft distillers","craft works","cragganmore","craigellachie","creag dearg","crianza","crooked water","crown royal","cut spike","cutler's","cutty sark","cutwater","czeglédi pálinkafőzde","d'hautefeuille","dachstein destillerie mandlberggut","dads hat","daftmill","dailuaine","dakota spirits","dalaruan","dallas dhu","dallas distilleries","dalmore","dalmunach","dalwhinnie","dambachler","dancing cows","dancing goat","dancing pines","dark corner","dark horse","dartmoor","de bercloux","de biercée","de graal","de la quintessence","de laguiole","de monsieur balthazar","de paris","deanston","death's door","deception","deerhammer","deheck","dehner","delaware phoenix","denning's point","derwent","des bughes","des menhirs","destylarnia piasecki","det norske","detroit city","devil's distillery","devils river","devine spirits","dewars","didier barbe","die klein rackelmann","die kleine","diedenacker","diesdorfer","dietrich","dillon's","dirker","distillery 291","diwisa  willisau sa","dixon&rsquo;s distilled spirits","do good","dobson's","doc porter's","dogfish head","dolleruper","domaine de bourjac","domaine des hautes glaces","don michael","don quixote","donner peltier","door county","dornoch","douglas laing","downslope","doz de dauzanges","dr. clyde","drentsche schans","dreum","drexler","driftless glen","drilling","drumlin","dry county","dry fly","du castor","du pays d'othe","du périgord","du risoux","du st. laurent","du vercors","dubh glas","dublin liberties","dueling barrels","dufftown","dumbarton","dundashill","dunglass","durango","duvel moortgat","dyreh&oslash;j ving&aring;rd","dà mhìle","dürr edelbranntweine","eaglesburn","east london","eastside","eau claire","echlinville","eckerts","edelbrandwein","edelobst","eden mill","edgefield","edradour","egg","egilse","egnach","eifel","eifel","eigashima","eigashima shuzo","eimverk","einar's","einbach","eleven wells","elkins","ellensburg","emperador","enghaven","english spirit","english spirit","ergaster","erismann","erongo mountain","eschenbräu","etter","evan william","evan williams","exeter","ezra cox","falckenthal","falken","fallstein","familie franz lauritsch","famous grouse","fannys bay","farny","farthofer","fary lochan","fein simon's","feiner kappler","feisty spirits","ferintosh","fesslermill","fettercairn","feuergraben","few spirits","fifth state","filibuster","finch","finger lakes","finlaggan","firestone","fisselier","five & 20","five points","flag hill","flat rock spirits","fleurieu","florida caribbean","florida farm","fogs's end","foothills","forgan","forschungs","forty creek","fossey's","four roses","foursquare","franken bräu","frankfort","franklin county","franz kostenzer","franz stettner & sohn","franziska","franzlahof","freeland spirits","fremont mischief","frey ranch","friedrich düll","frongoch","fugitives spirits","fuji gotemba","fukano","furneaux","g. miclo","gammelstilla","garnheath","garrison brothers","gasthof dinkel","gasthof hirsch","geiger","geistreich","gelephu","gemenc","George T. Stagg","george washington's","georges lacroix","georgia","gerhard büchner","gerhard wagner","gerlachus","gerston & auchnagie","ghost coast","gibson canadian","gierer","gilbert holl","gimli","ginebra san miguel","girvan","glacier","glann ar mor","glasgow","glen albyn","glen elgin","glen els","glen flagler","glen garioch","glen grant","glen keith","glen kella","glen mhor","glen moray","glen ord","glen ord","glen scotia","glen spey","glen wyvis","glenallachie","glenburgie","glencadam","glencraig","glendalough","glendronach","glendullan","glenfarclas","glenfiddich","glenfoyle","glenfyne","glenglassaugh","glengoyne","glengyle","glenkinchie","glenlivet","glenlochy","glenlossie","glenmorangie","glenmore","glenns creek","glenora","glenrothes","glentauchers","glenturret","glenugie","glenury royal","glina whisky","goalong liquor","godet","golan heights","golden distillery","golden moon","gols","gooderham","goodridge","gordon mac phails","gotland","gourmet berner","graanstokerij","grallet","grand traverse","grandten","granit","grants","graton","great lakes","great northern","great northern distillery","great outback","great southern","great wagon road","green river","greenbar","greenbrier","griffin ranch","griffo","grumsiner","grythyttan","grüner baum","guglhof","guillon","gulf coast","gute","gutshof andres","gwalia","gyokusendo shuzo","gö&szlig;wein","gölles","günter busch","h.clark","haas","habbel's","hafendestillerie","hagen rühli","haig's","hakushu","halber mond","hali'imaile","hamilton","hanson of sonoma","hanyu","harald keckeis","hard truth","hardenberg","hart family brewers","hartfield","hartges","haus hettig","hawkshead","hazelburn","headframe","headlands","healeys","heaven hill","helios","hellyers","hellyers road","hennessy","henry farms","henstone","hepp","hercynian","heritage","hessische spezialitätenbrennerei","hibiki","hibiki suntory","hiebl","hierber","high coast","high west","high wire","highglen","highland park","highspire whiskey","highwood","hill's liquere","hillrock estate","hillside","hinrichsen's","hinricus noyte's spirituosen","hiram walker","hiram walker sons","hirtner","hoffman","hollen","holweger","holy","holyrood","homberg","hood river","horstman","hotel tango","hounds tooth","humbel","hven","höllberg","IJsvogel","immortal spirits","imperial","inchdairnie","inchgower","ingendael","invergordon","inverleven","irish whiskey to delete","iron house","iron smoke","iron wolf","ironbridge","ironclad","ironroot republic","irten'ge","isaiah morgan","isanti","isarnhoe","isfjord","ivy mountain","j & b","j et m lehmann","j. carver","j. rieger","j. riley","j.w. kelly","jack daniels","james e. pepper","james sedgwick","jameson","janot","japanese whisky","jb","jeptha creed","jersey spirits","jf strothman","jim beam","jim beam","joadja","jobst","joe morgan's black diamond","joh. b. geuting","john distilleries","john emerald","john haig","john power & son","john's lane","johnnie walker","jonasberg stokerij","jones road","jos a magnus","josiah thedford","journeyman","jura","kaerilis","kagoshima","kaikyo","kaiyo","kalkwijck","kaltenthaler","kampen","kanosuke","kanosuke","kartveli","karuizawa","kauzen bräu","kavalan","kavalan","kawasaki","kellerstrass","kemper","kentucky artisan","kentucky bourbon distillers","kentucky owl","kentucky peerless","kern & schweigert","keuris","kgb spirits","khoday india","kilbeggan","kilchoman","kilkerran","killara","killowen","killyloch","kinclaith","kindschi söhne ag","king car","kings county","kingsbarns","kininvie","kinsip","kinzig","kiwi spirit","klein duimpje","klein fitzke","kleinhenz","kloster zinna","klosterdistille machern","knaplund","knockando","knockdhu","ko","ko'olau","koenig","kohler hofladen","kord","koval","kozuba","krauss","krobār craft","krucefix","kuenz","kumesen","kymsee","kyoto","kyoto","kyrö","kötztinger","kümin weinbau","la alazana","la piautre","la roche aux fées","la rouget de l'isle","ladyburn","lagavulin","lagg","lagler","lake george","lakes","lakes","lamas","lambicool","langatun","laphroaig","lark","las vegas","last mountain","last straw","launceston","lautergold","lava bräu braumanufaktur","lawrenceburg","lawrenny","laws whiskey house","lebe &geniesse","lechtaler haussegen","ledaig","lee spirits","leiper's fork","leopold bros","lepelaar","lexington","liber","liberty call","likörfabrik mikolasch","limestone branch","limtuaco","lindores","lindores abbey","linkwood","litchfield","littlemill","lo artisan","lobangernich","loburger brennereimanufaktur","loch brewery","loch ewe","loch lomond","locher","lochhead","lochindaal","lochside","lohn keiser","london distillers","london distillery","lonerider spirits","long island spirits","longhorn","longmorn","longrow","los 2 compadres","lost republic","lost spirits","lost state","lou&acirc;pre","louis royer","louisville","luca mariano","lucky bastard","ludlow","lux row","lynchburg","lyon","lübbehusen","lüthy","m&h","macardo","macduff","mackmyra","mad river","magdalene","mahrs bräu","maiden derry","maison daucourt","maison du vigneron","maison sivo","maker's mark","Maker's Mark","makers mark","malahats","malibreiz","malt mill","mammoth","manifest","manly","mannochmore","maraska","marder","marillenhof","marrowbone lane","mars shinshu","martell","martes santo","matsui shuzo","matter spirits","mavela","mb roland","mcclintock","mccormick","mcdowell's","mchenry","mclain kyne","mclaren vale","medley","meiers allgäuer","meissener","mellwood","meukow","meyer","mgp","michelehof","michter","micil","middle west","midleton","mighty oak","mile high","milk & honey","millburn","miltonduff","miltonduff","minhas","minsk grape wines factory","miscellaneous","mississippi river","missouri spirits","miyagikyo","Miyagikyo","miyashita sake brewery","moe","molen","monde shuzou","monkey hollow","monstein","mont saint jean","moon distilling","moon harbour","morris of rutherglen","mortlach","mosgaard whisky","mosstowie","mosswood distillers","mosterei","mosterei","mountain laurel","mountain state","mourne dew","moutard","mt. uncle","muller lemmer","murree brewery","mw&oacute;rveld  b.v.","myagikyo","myer farm","myken","mykulynetsky brovar","mystic farm","märkische","mönchguter","mück","mühle4","mühlenbrennerei","mühlhäuser","nacallan","nagahama","naguelann","nahmias et fils","nant","nantou","nc'nean","ncnean","nearest green","nelson's green brier","nelsons green brier","nestville","neuenburg","nevada h&c","new deal","new england","new holland","new liberty","new riff","new riff","new york distilling","newport","nibelungengold","niederrhein","niigata","nikka","ninkasi","nishinomiya","noble elite","nonesuch","nordik","nordisk br&aelig;nderi","nordlicht","nordmarkens","norrtelje","north british","north of 7","north of scotland","north of scotland","north port","north shore","northmaen","northoff","number nine","nun's island","nyborg","o'begley","o.f.c. stagg","o.z. tyler","oban","obst","obst dirk böckenhoff","ocean king","odd society","off the clock","ohishi","okanagan spirits","old carrick mill","old carter","old comber","old crow","old dominick","old elk","old fitzgerald","Old fitzgerald","old forester","old forester","old forge","old gamundia whisky","old grand dad","old grand-dad","old hobart","old kempton","old line spirits","old pogue","old pulteney","old raven","old rip van winkle","old sandhill","old school","old sugar","old tahoe","old taylor castle","old world spirits","ole smoky","one eight","oola","oppidan","orange county","orcas island","oregon spirit","original texas legend","orma","orphan barrel","osumi","osuzuyama","otter craft","ouche nanon","outlaw rum","oxford artisan","ozark","palmetto","palìrna u zeleného stromu","panimoravintola beer hunter's","panimoravintola koulu","panther","parkmore","parliament","parzmair","pasquet","patrick breindl","peach street","pearse lyons","peloni","pelter","pemberton","penderyn","penderyn","pennco","penninger","pennington","peter affenzeller","peterseil","pfanner","pfau brennerei","philadelphia","pianta brand","piedmont","pierde almas","piet van gent","pirlot stokerij","pittermanns","pittsburgh","pittyvaich","pocketful of stones","popcorn sutton","port charlotte","port chilkoot","port dundas","port ellen","potter","pradlo","praskoveya","preiser","preuschens","preussische","prichards","primushäusl","prince edward","prohibition distillery","proof artisan distillers","proof wood ventures","psenner","puchas","pulteney","puni","qvänum mat","r. jelìnek","r.m. rose","raasay","raasay","rabbit hole","rabel","radermacher","radico khaitan","ragged branch","ralf hauer","ranger creek","ransom","re:find","rebecca creek","red bordner","red bull","red eagle","redbreast","reece's","refer to images","reisetbauer","remy martin","republic restoratives","reservoir","restless spirits","rich grain","rieger","rittmeister","riverbourne","robert meisner","rochfort","rock town","rockfilter","rogner","rogue spirits","rose valley feinbrand","rosebank","roseisle","roser","rothaus","roughstock","royal brackla","royal brewhouse","royal irish","royal lochnagar","royal oak","rugenbräu","ryan & wood","safe house","sagamore spirit","saint james spirits","sakurao","sall whisky","salm bräu","sammerhof","samuel smith","san diego","san diego sunshine","santa fe spirits","santamanía","santan","sas distilleries","sasanokawa shuzo","sasse","sauerländer","savage & cooke","saxa vord","scapa","scheibel mühle","schenley","schlitzer korn","schloss marienburg","schlossbrauerei autenried","schmalwieser","schwane","schäffler bräu","scissortail","scriptor","seacrets","seagram","seagram","seattle","second chance spirits","seetal","sempione","senft","seppelbauer","seven brothers","seven stills","seven three","sheep dip","shelter","shelter point","shene estate","shinobu","shinshu","shinshu mars","shinzato","shirakawa","shizuoka","short mountain","shot in the dark craft","sibling","siegfried herzog","sierra norte","signal hill spirits","sikkim","silk city","silver trail","sin gold","sinnesfreuden neber hagemann","six & twenty","skaalvenn","skip rock distillers","skånska","slane","sliabh liag","slijterij","slyrs","small","small concern","smith bowman","smooth ambler spirits","smugglers' notch","smws","smögen","snitching lady","sonnenbräu","sonnenscheiner","sonoma brothers","sonoma county","sons of liberty","sons of vancouver","southern  company","southern artisan spirits","southern coast","southern distilleries","southern grace","southern grain","southern tier","souwester spirits","sperbers","sperling silver","spessarthof","speyburn","speyside","spezialitäten assulzerhof","spezialitäten weidhof","spezialitätenbrauerei eckart","spirit hound","spirit of york","spirit of yorkshire","spirit of yorkshire","spirit works","spirits of french lick","spirits workshop","splinter group","split rock","spreewald","spreewood","spring bay","springbank","springbrook hollow farm","square one","st augustine","st george","st. george spirits","st. kilian distillers","st. patrick's","st. petersburg","st. urban","stadler","stadsbrouwerij de hemel","stammheimer","standard wormwood","stark spirits","starkenberg","starlaw","starlight","starward","starward new world","stauning","steigmiller","stein","steinhauser","steinwälder","stenger","still 630","still austin","still waters","stilltheone","stillwater","stitzel","stitzel","stoaninger","stock","stokerij de molenberg","stokerij de onrust","stokerij sculte","stone barn brandyworks","stonecutter","stranahan's colorado","strathclyde","strathearn","stratheden","strathisla","strathmill","stromness","stronachie","studio","stöfflbräu","suerlaenner","sugarlands","sullivans cove","suntory","surselva bräu","svach","sweet potato spirits","swift","syntax spirits","sächsische","säntisblick","t koelschip","t.o.s","taconic","tahoe moonshine","tahwahkaro","talisker","tamar valley","tamdhu","tamnavulin","tanduay distillers","tanqueray","tarnished truth","tasmania","tatoosh","tattersall","tawny corn","teaninich","teeling","teerenpeli","tekel","telser","temperance","tesetice","tevsjö","the black bottle","the block","the cooper spirits","the family jones","the grove experience","the helsinki","the liberty","the shed","the shed","the vintage malt","the vogel","the waters","the wild alps","theo preiss","think destillers","thirteenth colony distilleries","thistle finch","thomas sippel","thomas street george roe","thomas wilhelm","thomson whisky new zealand ltd","thorn&aelig;s destilleri","three boys farm","thuisbrunner elch bräu","thumb butte","thunder road","thy whisky","tiger juice","timboon railway shed","tin shed","tipperary boutique","tirado","tirril brewery","to t&aring;rn bryggeri as","tobermory","tobias schmid","tom&#039;s foolery","tomatin","tomintoul","tommyrotter","top of the hill","top shelf distillers","top shelf international","torabhaig","tormore","toronto","tovuz","towcester mill brewery","towiemore","trail town still","traverse city whiskey","trebitsch old town","treecraft","tria prima","triple eight","trolden","tsunuki","tullamore","tullamore dew","tullamore dew","tullibardine","turabauer maass","turin","turv exloo","tuthilltown spirits","tweeddale","tweekoppige","twenty third street","twin creeks","twin stills moonshine","twin valley","two doves","two james","tōsh","uerige","ugelris","ulex schnäpse","union horse","union maltwhisky do brasil","united  group","uppsala destilleri","urban distilleries","us heit","valamo monastery","valentine","vallei distilleerderij","van brunt stillhouse","vapor","vara","vareler brauhaus","vattudalen","venakki","venus spirits","victoria distillers","vielanker brauhaus","vienna craft","vikre","viktor senn","village brewer","ving&aring;rden lille gadeg&aring;rd","vinn","virgil kaine lowcountry","virginia","virginia sweetwater","vitis industries","vulkan brauerei","w.l. weller","wakatsuru saburomaru","waldbrand destillerie","waldhorn klotz gbr","waldkircher","waldviertler roggenhof","wallner","walsh whiskey","walter seeger","wannborga","warenghem","waterford","waterford","watershed","wave distil","wayne gretzky estate","weidenauer","weidmann & groh","wein und likörfabrik h. a. wagner","weinbau zur krone","weingut dotzauer","weingut etl","weingut mö&szlig;lein","weinhaus kilian","weinkellerei spielmann","west cork distillers","west virginia","western reserve","western son","western spirits","westland","westward","weutz","weyermann destillerie","wharf","wheat state","whipper snapper","whiskey acres","whisky castle","whistlepig","whistling andy","white horse","white peak","whitmeyer's","whyte & mackay","wibblers","widow jane","widow jane","wieser","wijnhuis texel","wild brennerei","wild river mountain","wild turkey","wilderen","wilderness trail","wilhelm behr","willett","willie's","willowbank","willy macheiner","windecker dorfbrennerei","winter park","wishkah river","wolf & oak","wolfburn","wollbrink","wondertucky","wood hat spirits","wood&rsquo;s high mountain","woodford reserve","woodinville","woodstone creek","woody creek","workshops","wright & brown","wylie howell","wyndberg","wyoming","wädi","yack creek","yahara bay","yalaha bootlegging","yamazaki","yamazakura","yellow rose","yerushalmi","yeti","yoichi","york brewery","yserrain","yukon brewing","z&#039;graggen","z&aacute;meck&aacute; palìrna blatn&aacute;","z.kozuba i synowie","zauser","zeitzer whisky manufactur","zogg mosterei","zuidam","zum lobmüller","zweiger","zweistein","zöchmeister","öufi brauerei"]

    # Request
    data = request.get_json()

    # Body
    input = data.get('input', '')
    forbidden_words = data.get('forbidden_words', '')
    cutoff_input = data.get('cutoff', '')

    if(cutoff_input != ''):
        cutoff = cutoff_input

    forbidden_words_default.extend(forbidden_words)
    print(forbidden_words_default)
    for w in forbidden_words_default:
        input.replace(w, '')

    # logic
    splitted_input = input.split(" ")
    splitted_input = filter(lambda x: len(x)>=word_size, splitted_input)

    result = []
    for word in splitted_input:
        currentResult = difflib.get_close_matches(word, search_field,cutoff=cutoff)
        for i in currentResult:
            result.append(i)

    result = list(set(result))
    return jsonify(result)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)



# for Joro