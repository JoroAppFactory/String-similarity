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
    word_size = 6
    cutoff = 0.75
    search_field = ['w.l. weller','eigashima','kavalan',' king car','hibiki','old rip van winkle','van winkle','lakes','','smögen','glen garioch','raasay','irish whiskey to delete','michter','glen grant','glengrant','blanton\'s','royal lochnagar',' lochnagar','dunglass','redbreast','ardgowan','blair athol','atho','jim beam','hazelburn','','glengyle','longrow','glen elgin','compass box','haig\'s','glen ord',' ord','spirit of yorkshire','buchanan\'s','bell\'s','j & b',' j&b',' justerini','famous grouse','famous egrouse','fgrouse','ardnahoe','ben wyvis','old fitzgerald','breuckelen','four roses','bivrost',' aurora','north british','booker\'s','kanosuke','miyagikyo','the shed','cardrona','mackmyra','milk & honey',' m&h',' milk and honey','japanese whisky','lindores abbey','finlaggan','gerston & auchnagie','shinobu','colonel e.h. taylor','smws',' scotch malt whisky society','nantou','john power & son','strathearn','evan williams','kaiyo','towiemore','annandale','anandale','amandale','refer to images','nacallan','macallan',' maçallan',' themacallan',' macallah','hibiki suntory','willett','dalmore','karuizawa','mars shinshu','springbank','lagavulin','fettercairn','talisker','bowmore','bowmor','gowmore','howmore','yoichi','chivas','beam suntory','chichibu','nikka','benromach','be nromagh','be nromach','beromach','wild turkey','ardbeg','teaninich','glenfarclas','glenfarela!','glenfare','glenfarela','glenfarela!','glonfardla','glenfar','honfarclas','enarclas','carsebridge','hakushu','glenkinchie','convalmore','glenmorangie',' lenmorangie','midleton','longmorn','laphroaig','laphroa','laphroaic','linkwood','rosebank','mortlach','glen ord',' ord',' rd','strathisla','bimber','benriach','bênriach','bënriach','ben riach','enriach','benrrach','amrut','glendronach','bunnahabhain','whyte &mackay','whyte&mack','bruichladdich','bruichiaddich','pruichladdich','bruich laddich',' ruichiaddich','ruich laddich','bruichiladdich','heaven hill','glenrothes','high west','nevada h&c','hillside',' glenesk','coleburn','shizuoka','old pulteney',' pulteney','old forester','glen mhor','jameson','johnnie walker','ohnnie','loch lomond',' inchmurrin','kilkerran','glengyle','glen gyle','knockdhu','daftmill','foursquare','dalwhinnie','balvenie','caol ila','caol iln','littlemill','inchgower','caledonian','dallas dhu','glen keith','caperdonich','mosstowie','gordon mac phails','imperial','garrison brothers','sullivans cove','teeling','douglas laing','glen albyn','tomintoul','pittyvaich','kentucky owl','inverleven','kavalan','bladnoch','bladnoch"','strathclyde','garnheath','ardnamurchan','tamdhu','balblair','scapa','north of scotland','cragganmore','ragganmore','jack daniels','tomatin','omatin','suntory','raasay','dailuaine','glenglassaugh','port dundas','lochside','wolfburn','glenlossie','chita','bushmills','invergordon','tormore','clynelish',' candlekitty','glenallachie','gialachie','genallachie','brown forman','ambler','north port','glen scotia','yamazakura','orphan barrel','barrell','royal brackla','bračkla','ballantine','ballantins','ballantines','edradour','limestone branch','ledaig','ledaigfrom','cameronbridge','haig club','tamnavulin','cambus','glenfiddich','glen spey','deanston','ben nevis','glengoyne','aurora spirit','torabhaig','glen moray','kilchoman','homan','kilc','glenturret','speyburn','glencadam','glen cada','kininvie','benrinnes','dewars',' dewar\'s',' dewar','waterford','whistlepig','westland','balcones','nelsons green brier','cardhu','mclain kyne','balmenach','lakes','penderyn','jb','jura','cutwater','akkeshi','oban','ncnean','tullamore','st george',' st. george','barton 1792',' 1792','eden mill','kingsbarns','auchroisk','braeval','auchentoshan','auchentosha','grants','tuthilltown spirits','john haig','mannochmore','tullibardine','tlibardine','copper rivet','aberfeldy','stronachie','glenburgie','white horse','hanyu','kawasaki','glendullan','lux row','aultmore','new riff','glenury royal','magdalene',' linlithgow','millburn','antiquary','bardstown','caroni','old carter','macduff',' deveron','one eight','western spirits','boone','cotswolds','louisville','jos a magnus','proof wood ventures ','st augustine',' augustine','makers mark','strathmill','widow jane','ardmore','bourbon 30','filibuster','smith bowman',' bowman','backbone','glen flagler','dalmunach','woodford reserve','finger lakes','hiram walker sons','dingle','the vintage malt','high coast','kinclaith','glenlochy','stitzel','dornoch','glenugie','spirit of yorkshire','glencraig','ailsa bay','breckenridge','schenley','chugoku jozo','starward new world','dads hat','catskill','cutty sark','utty sar','utty sark','cuity sark','sarn','ranger creek','boston harbor','fremont mischief','glenmore','ladyburn','crown royal','cooley','allt a bhainne',' bhainne',' alltabhainne','prichards','outlaw rum','buffalo trace ','lawrenceburg ','kentucky bourbon distillers','tobermory','gibson canadian','','bow street',' john jameson','royal irish','jones road ','old grand dad ','john\'s lane',' john power','tullamore dew','maker\'s mark','coleraine ','fuji gotemba','hill\'s liquere','hiram walker','killyloch','arizona','tesetice ','james e. pepper','old forester','anchor','willowbank','charles medley ','blaue maus','kagoshima','north of scotland','potter','cascade hollow ','glenora ','sonnenscheiner','shinshu mars','slyrs','glen kella','highwood','hollen','humbel ',' zürcher','nishinomiya','rugenbräu','glann ar mor','panimoravintola beer hunter\'s','us heit ','teerenpeli','bernheim','burgdorfer','chicken hill','cradle mountain','mosterei',' stadelmann','gasthof hirsch','hercynian',' hammerschmiede','lark ','samuel smith','telser ','belgian owl','willy macheiner','warenghem','stokerij de molenberg','hagen rühli','loch ewe ','meyer','zuidam ','vallei distilleerderij','bieri bauernhof','duvel moortgat','birkenhof','glen els','lüthy','macardo','mavela','locher','stokerij de onrust','triple eight ','ving&aring;rden lille gadeg&aring;rd','whisky castle','abhainn dearg',' carnish','james sedgwick','rothaus','walter seeger','monstein','braunstein',' schwab',' liebl','crianza','edgefield ','j et m lehmann','forty creek','graanstokerij','kümin weinbau','great southern','clear creek ','old raven','la rouget de l\'isle','southern grain','slijterij',' museum van kleef',' höhler','eigashima shuzo','catoctin creek ','des menhirs','eifel','kampen','fary lochan','haas','pradlo ','kilbeggan ','craft distillers','wannborga','rock town ','roughstock','southern coast','sperbers','langatun','thirteenth colony distilleries','a. smith bowman',' ziegler','altstadthof','big bottom ','box Destilleri',' high coast','steinhauser','mississippi river','dakota spirits','delaware phoenix ','diedenacker','drexler','few spirits','healeys','hven','braugasthof',' papiermühle','new holland','old hobart ','spreewald','smooth ambler spirits','sonnenbräu','stauning','surselva bräu',' gruel','avadis ','bertrand','vielanker brauhaus','weingut mö&szlig;lein','lebe &geniesse',' langenrohr','falken','oregon spirit ','waldviertler roggenhof','domaine des hautes glaces','senft','finch',' henrich','schlitzer korn','hillrock estate ','forschungs',' hohenheim','nyborg ','kinzig','radermacher','liber','z&#039;graggen','lost spirits ','corby spirit','meissener','monde shuzou','aare bier','old world spirits','john distilleries','mönchguter','preussische','qvänum mat','roser','edelbrandwein',' ewald rau','sons of liberty','still waters ','starward','stoaninger','stranahan\'s colorado','timboon railway shed ','wädi','brau','huus','copper fox ','whistling andy','widow jane ','wyoming','adnams','aichinger','alberta','hepp','cooperstown ','belgrove ','de monsieur balthazar','molen','heritage','english spirit ','joh. b. geuting','arcus','grythyttan','gute','longhorn ','marder ','märkische','mosswood distillers','mykulynetsky brovar','nestville ','nordisk br&aelig;nderi','old pogue','old sandhill','öufi brauerei','panimoravintola koulu','praskoveya',' druffel','reservoir ','rogner','stokerij sculte','spezialitätenbrauerei eckart','st. george spirits','edelobst',' höning','lakes','egnach','corsair','weidenauer','woodinville ','woodstone creek','t koelschip',' koelschip','sonoma county','radico khaitan','alpenwhisky','amador ','wave distil','uerige','hinricus noyte\'s spirituosen','békési manufaktura','caldera ','camp 1805','york brewery','charbay','whipper snapper ','wollbrink','dürr edelbranntweine','dry fly ','feisty spirits ','brunschwiler','gerhard büchner','glendalough ','glina whisky','r. jelìnek','rittmeister','guglhof','hellyers road ','etter','last mountain ','mück','okanagan spirits','kauzen bräu','thomas sippel','patrick breindl','puni','reisetbauer','scriptor','old gamundia whisky','stöfflbräu','steinwälder',' schraml','dolleruper','bull run','london distillery','the vogel','thomson whisky new zealand ltd','tom&#039;s foolery ','kiwi spirit','alte haus a. wecklein','alambik','wilderen','günter busch','anno 1940','laws whiskey house','ag&aacute;rdi p&aacute;linkafőzde','alley 6','alt enderle','archie rose','agder','nelson\'s green brier ','de bercloux','black dirt ','black gate ','stein','blackwater ','brenne','broad branch ','lake george','victoria distillers','cut spike ','bruckners erz bräu','bellerhof','IJsvogel','deheck','hamilton','burger','dietrich','dillon\'s','dingle','dirker','eaglesburn ','kalkwijck','cornelius pass roadhouse ','det norske','nordik','ergaster','eimverk ','blaum','gemenc','george washington\'s','gerlachus','seetal','authentic seacoast','the helsinki  ','horstman','tin shed  ','journeyman ','klein duimpje','z.kozuba i synowie','friedrich düll','kymsee','kyrö','donner peltier','gilbert holl','las vegas ','lobangernich','brûlerie du revermont','mgp','moutard',' lanz','new riff ','yeti ','gerhard wagner','kentucky peerless','pemberton ','pfanner','highglen ','rebecca creek ','bischof','alde gott','great lakes ','norrtelje','ralf hauer','schwane','saxa vord','spirit hound','vikre ','wakatsuru saburomaru ','the grove experience','number nine','west cork distillers','northoff','niederrhein','sauerländer','trolden ','valamo monastery ','birgitta',' birgitta rust',' piekfeine brände','castan','franz kostenzer','sasanokawa shuzo','zweiger','twin valley','black button ','wood hat spirits','brænderiet limfjorden','cleveland','copperworks','corowa','dà mhìle ','mountain laurel','drentsche schans','georges lacroix','preiser',' eiger','muller lemmer','psenner','grallet','dupic','to t&aring;rn bryggeri as','peloni','golan heights','sperling silver ','weingut etl','habbel\'s','ironroot republic ','gotland','henry farms',' prairie spirits','koval ','kemper','pirlot stokerij','keuris','kings county ','alpirsbacher','alpirsbacher klosterbräu','m&h',' milk & honey',' milk and honey','shene estate','mad river','mahrs bräu','tsunuki','mchenry ','missouri spirits','moon harbour','nagahama','north of 7 ','miyashita sake brewery','diesdorfer','peter affenzeller','popcorn sutton ','rabbit hole ','tweekoppige','säntisblick','neuenburg','shelter point ','fein simon\'s','enghaven','st. patrick\'s ','stark spirits ','starlight ','stone barn brandyworks','spreewood','dublin liberties','exeter',' the fat pig','matsui shuzo','asheville','tipperary boutique ','toronto  ','turv exloo ','yukon brewing ','kaltenthaler','virginia  ','small','brook','wieser','feiner kappler','workshops ','wright & brown  ','yellow rose ','sempione ','stadsbrouwerij de hemel','asaka','asw ','united  group','badmils black ','de biercée','bimber ','boldizar',' obstbrand','bosch edelbrand','braeckman ','brehmer',' knauer','arnsteiner','chattanooga','clonakilty ','conecuh ridge ','southern grace','gimli',' höck','dancing cows ','pennington','deerhammer',' ehringhausen','scissortail ',' spielberger','augustus rex','eau claire','thuisbrunner elch bräu','borchert','fannys bay ','fleurieu ','hessische spezialitätenbrennerei','fukano ','gammelstilla','mühle4','gölles','griffo ','acha','stonecutter','ironclad','isfjord','browar ciechan','harald keckeis','hart family brewers','helios ','la piautre','liberty call ','central city ','lucky bastard','cali ','geiger',' Imkerei','mcdowell\'s','fesslermill','mosgaard whisky','naguelann','nant ','new york distilling','old kempton ','svach','rabel','pearse lyons ','pelter ','pfau brennerei','cave de la crausaz','still 630','chankaska spirits','kuenz','franziska','graton ','ironbridge','j. rieger','steigmiller','lutz','sasse','sächsische','san diego ','haus hettig','savage & cooke','slane','smugglers\' notch ','st. kilian distillers','taconic ','h.clark ','tevsjö','lepelaar','baumgartner',' tiroler','tommyrotter ','the waters ','traverse city whiskey ','tullamore dew','nearest green ','virgil kaine lowcountry ','g. miclo','hafendestillerie','einbach','walsh whiskey','zeitzer whisky manufactur','aero whisky','anglesey','arbikie','bakery hill ','baltimore','ko ','wilhelm behr','hardenberg ','black bridge ','jeptha creed ','bluegrass','turin','preuschens','bows','brother justus','wharf ','chicken cock','churfirsten','cley ','coppersea ','obst dirk böckenhoff','detroit city ','distillery 291','krauss','east london','scheibel mühle','eschenbräu','farny','great northern distillery','forgan','alex clark','waldhorn klotz gbr','franken bräu','riedbach','guillon','kaikyo ','devil\'s distillery','biospirits','kartveli','joadja ','kanosuke ','tōsh ','new liberty','belmont farm ','krobār craft ','baker williams ','launceston','lindores','franzlahof',' hubertus vallendar','manly','the wild alps','kumesen','myken','nibelungengold','ninkasi','o.z. tyler','odd society','old line spirits','gyokusendo shuzo','penninger','khoday india','de graal','schmalwieser','zum lobmüller','du vercors','seven stills','signal hill spirits','eifel',' j.p.schütz','oxford artisan','spring bay ','lohn keiser','clydeside','lübbehusen','riverbourne ','top of the hill ','lexington','trebitsch old town ','schäffler bräu','two james','firestone','ugelris','mt. uncle ','spezialitäten weidhof','weingut dotzauer','westward','pittsburgh','wilderness trail ','bendt','wolf & oak ','brandhaus 7','czeglédi pálinkafőzde','10th street','adelaide hills','niigata ','anno','dr. clyde','backwoods  ','ballykeefe ','baronie','böckenhoff','bauhöfer',' ulmer','blackmoon','boplaas','kötztinger',' bärwurz quelle','bröderna bommen','burwood ','bus','chief\'s son ','circumstance ','cirka','coles ','leiper\'s fork ','cooper king','corra linn ','bronckhorst','killara ','dartmoor','august dinsing','safe house','three boys farm','drilling','the shed ','dueling barrels','bossche stokers','egg','farthofer',' feller','turabauer maass','fossey\'s ','ghost coast ','glen wyvis ','golden moon ','hanson of sonoma ','hierber','holweger','holyrood ','sas distilleries','irten\'ge',' gurten farmhouse ','jobst','weinhaus kilian','killowen ','knaplund','loburger brennereimanufaktur','lagg','last straw ','five points ','lonerider spirits','the black bottle ','d\'hautefeuille','luca mariano','z&aacute;meck&aacute; palìrna blatn&aacute;','pianta brand','greenbrier','spirits workshop','nonesuch ','nordmarkens','otter craft ','philadelphia ','r.m. rose','rochfort ','rose valley feinbrand','long island spirits','santan','sagamore spirit ','kindschi söhne ag','newport','short mountain ','sin gold','de paris','ouche nanon ','santamanía','skånska','spritfabriken','st. urban','connacht ','lambicool','still austin','tahwahkaro','moe ','tarnished truth','iron house ','borders','think destillers','northmaen','thy whisky ','vareler brauhaus','de laguiole','ulex schnäpse','pittermanns','van brunt stillhouse','vattudalen','armagnac veuve goudoulin','vulkan brauerei',' hack','waldkircher','weyermann destillerie','white peak ','yack creek','yerushalmi ','5nines','7k ','bodega abasolo','brain brew',' eureka','backwoods craft spirits','zweistein','bergslagens','republic restoratives','broken bones','brugse','cathead ','charlier','clara hof','copenhagen ','copper rebublic ','craft works','windecker dorfbrennerei','devils river','gasthof dinkel','einar\'s',' lippert','halber mond','frey ranch','furneaux','headlands','henstone','tamar valley ','ocean king','isarnhoe','puchas','la roche aux fées','starlaw','lawrenny ','loch brewery','lost republic','ludlow','mammoth','old carrick mill ','mb roland ','mourne dew ','ohishi ','j.w. kelly','erongo mountain','orma','osuzuyama','ragged branch','dobson\'s','castle & key','rieger',' hofmeister','rogue spirits',' stapf','eckerts','feuergraben','sall whisky ','alexander biselli','didier barbe','hard truth ','weinkellerei spielmann','spirit works ','stammheimer','adams ','vara','aisling','derwent','creag dearg ','thorn&aelig;s destilleri','union horse  ','uppsala destilleri','mühlenbrennerei','claeyssens de wambrechies','waterford ','watershed ','whiskey acres  ','wild river mountain ','venakki ','wyndberg','yserrain','aber falls','agitator','t.o.s','maison daucourt','drumlin ','wild brennerei','vienna craft ','inchdairnie','diwisa  willisau sa','hawkshead','american freedom ','klosterdistille machern','mühlhäuser','lautergold','chateau du breuil','moon distilling','mw&oacute;rveld  b.v.','top shelf international','die kleine','sakurao','sons of vancouver','evan william','stenger','tria prima','birkenhof','mccormick','stock','canadian mist','hoffman',' old commonwealth','old crow ','old comber','frankfort','ferintosh','kellerstrass ','lochindaal','green river ','mellwood ','burke\'s ','parkmore','glenfyne','o.f.c. stagg ','marrowbone lane','thomas street george roe ','stromness','black velvet ','gooderham','southern distilleries','corio','continental distillers','1000 hills','10th mountain','12.05','1769','18th street','2bar','3 badge','3 howls','45th parallel','52eighty ','66 gilead ','acre ','adirondack  ','aioi unibio','alaska ','albany ','alchemy ','all points west','allgäu',' günther','alte','altore','american fifth','andalusia','appalachian ','applewood','arbutus ','arcola ','arizona high spirits ','artist in residence','ascendant','astidama','auchnagie','axe and the oak ','az granata',' azgranata','bachgau','bad dog ','bainbridge','bandon ','bankhall','baoilleach ','barrel house ','basilico','basque moonshiners','batch 206 ','bay area','bear wallow ','belle isle','belmont ','benachie',' bennachie','bendistillery','bent','bergwelt','berkshire mountain','betz','bflo','bières michard','biolandhof köhler','black bear ','black canyon ','black draft ','black heron','black\'s','blackfish','blinking owl','blue monkey','blue ridge','blue sky ','blue spirits ','boann ','böckl','bogner','bolanachi','bone spirits','boone county jail ','böttchehof','bouck brothers ','branger',' bayer',' bühler','brasch',' friz',' hübner',' kramer',' lettner',' ludwig faber',' roman kraus',' ro&szlig;mann','falckenthal','chicago','collier',' mckeel','colorado gold ','copper run ','crooked water','cutler\'s','dachstein destillerie mandlberggut','dalaruan ','dallas distilleries','dambachler','dancing goat ','dancing pines ','dark corner ','dark horse ','death\'s door ','deception ','dehner ','denning\'s point ','ayutla','limtuaco','aldea','siegfried herzog','gö&szlig;wein','hirtner','parzmair','destylarnia piasecki','devine spirits','die klein rackelmann','cherry rocher','de la quintessence','des bughes','dreum','du castor','du pays d\'othe','du périgord','du risoux','du st. laurent','janot','theo preiss','krucefix','dixon&rsquo;s distilled spirits','do good ','doc porter\'s ','dogfish head ','domaine de bourjac','don michael','don quixote ','door county ','downslope ','doz de dauzanges','driftless glen','dry county ','dubh glas ','dundashill','durango','dyreh&oslash;j ving&aring;rd','eastside ','echlinville','gierer','egilse','eleven wells','elkins','ellensburg ','emperador','english spirit ','erismann','ezra cox ','fallstein',' demmel','familie franz lauritsch','fifth state ','fisselier','five & 20','flag hill ','flat rock spirits ','florida caribbean','florida farm','fogs\'s end ','foothills ','franklin county','franz stettner & sohn','freeland spirits','frongoch ','fugitives spirits','geistreich','gelephu ','georgia','ginebra san miguel','glacier ','glenfoyle','glenns creek ','goalong liquor','godet','golden distillery','goodridge','gourmet berner','grand traverse ','grandten ','granit','great northern ','great outback','great wagon road','greenbar ','griffin ranch','grumsiner','grüner baum','gulf coast','gutshof andres','hali\'imaile','hartfield','hartges','headframe','hiebl','high wire','highspire whiskey','hinrichsen\'s','höllberg','holy ','homberg','hood river','hotel tango','hounds tooth','immortal spirits','ingendael','iron smoke','iron wolf','isaiah morgan','isanti','5 artisan','ivy mountain','j. carver ','j. riley ','jersey spirits  ','jf strothman ','joe morgan\'s black diamond ','john emerald','jonasberg stokerij','josiah thedford','kaerilis','kentucky artisan ','kern & schweigert','kgb spirits','kinsip','klein fitzke','kleinhenz','kloster zinna','ko\'olau','koenig','kohler hofladen','kord ','kozuba','la alazana','lagler','lamas','lava bräu braumanufaktur','lechtaler haussegen','lee spirits','leopold bros','likörfabrik mikolasch','litchfield ','lo artisan ','lochhead','london distillers','los 2 compadres','lost state ','lou&acirc;pre','pottier','lynchburg ','lyon','maiden derry ','maison du vigneron','maison sivo','malahats','malibreiz','malt mill','manifest ','maraska','marillenhof','martes santo','matter spirits','mcclintock','meiers allgäuer','michelehof','micil ','middle west','mile high','minhas ','minsk grape wines factory','miscellaneous ','monkey hollow ','mont saint jean','morris of rutherglen','mosterei','mountain state ','murree brewery','myer farm','mystic farm','nahmias et fils','new deal ','new england ','noble elite','nordlicht','north shore ','nun\'s island ','o\'begley ','obst','korn  zaiser','off the clock','old dominick ','old elk','old forge ','old school','old sugar ','old tahoe ','ole smoky ','oola ','oppidan','orange county ','orcas island','ozark ','palìrna u zeleného stromu','palmetto ','panther ','parliament','peach street','penderyn ','peterseil','piedmont','pierde almas ','piet van gent','pocketful of stones','port chilkoot ','primushäusl','prince edward ','gols','prohibition distillery','proof artisan distillers','ransom','re:find','red bordner','red bull','red eagle ','reece\'s','restless spirits ','rich grain','robert meisner','rockfilter ','roseisle','royal brewhouse','royal oak ','ryan & wood','saint james spirits','salm bräu','sammerhof','san diego sunshine','santa fe spirits','schloss marienburg','schlossbrauerei autenried','seacrets','seattle ','second chance spirits','seppelbauer','seven brothers','seven three','shelter ','shirakawa','shot in the dark craft ','sibling ','sierra norte ','sikkim','silk city','silver trail ','sinnesfreuden neber hagemann','six & twenty ','skaalvenn ','skip rock distillers','sliabh liag ','snitching lady ','sonoma brothers','southern artisan spirits','southern  company','southern tier ','souwester spirits','spessarthof','spezialitäten assulzerhof','spirit of york ','spirits of french lick','split rock ','springbrook hollow farm','square one','st. petersburg ','stadler','standarad wormwood ','starkenberg','stilltheone','stillwater',' moylan','stratheden','studio ','sugarlands','sweet potato spirits','swhisky','swift ','syntax spirits','tahoe moonshine ','tanduay distillers','tatoosh','tattersall ','tawny corn','tekel','temperance ','the block','bondi','the cooper spirits','the family jones ','the liberty ','mclaren vale','mighty oak','original texas legend','splinter group','village brewer','thistle finch','thomas wilhelm','thumb butte ','thunder road ','tiger juice ','tirado ','tirril brewery','tobias schmid','top shelf distillers','tovuz','baltiya','towcester mill brewery','trail town still','treecraft','twenty third street ','twin creeks ','twin stills moonshine ','two doves','union maltwhisky do brasil','urban distilleries','valentine ','vapor ','venus spirits','viktor senn','vinn','virginia sweetwater ','vitis industries','waldbrand destillerie','wallner','wayne gretzky estate','weidmann & groh','weinbau zur krone','wein und likörfabrik h. a. wagner','west virginia','western reserve','western son ','weutz','wheat state ','whitmeyer\'s','wibblers','wijnhuis texel','willie\'s','winter park','wishkah river ','wondertucky','woody creek','wood&rsquo;s high mountain ','wylie howell','yahara bay','yalaha bootlegging ','zauser','zöchmeister','zogg mosterei ','  ag','&aelig;ppeltreow','suerlaenner',' volker theurer im gasthof lamm','brickway ','broadbent','broger','bulleit','bully boy','caiseal','cadushy ','carbon glacier ','cedar ridge','central standard ','ch ','chambers bay ',' steinlein',' roder','sheep dip','ardenistle','remy martin','boone county','hennessy','NULL','pennco','Brora','Camus','Old fitzgerald','stitzel','medley','George T. Stagg','courvoisier','NULL','bardstown','louis royer','NULL','jim beam',' booker noe','shinshu','NULL','miltonduff','NULL','NULL','lakes','bernheim','NULL','martell','shinzato','old grand-dad',' grandad','pulteney','NULL','kyoto','NULL','nc\'nean',' ncnean','NULL','NULL','dingle','NULL','tasmania',' sullivans cove','NULL','king car',' kavalan','NULL','miltonduff','charpentier','Miyagikyo','old taylor castle','Maker\'s Mark','NULL','NULL','NULL','pasquet','gwalia','seagram',' louisville','NULL','tanqueray','meukow','osumi','small concern','NULL','kyoto','aber falls','NULL','hellyers','NULL','NULL','seagram',' waterloo','NULL','NULL','NULL','NULL','NULL','NULL','NULL','NULL','myagikyo','port ellen',' fort ellen','arran',' lochranza','highland park','dufftown','dufftoen','glentauchers','yamazaki','speyside','drumguish','banff','brora','craigellachie','knockando','aberlour', '','glasgow ','girvan','port charlotte','glenlivet','glinlivet','dumbarton']

    # Request
    data = request.get_json()
    input = data.get('input', '')
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
