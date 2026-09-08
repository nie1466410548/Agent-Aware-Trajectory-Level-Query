import json, re
from collections import Counter, defaultdict

with open("/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/fad/agnews/query4/full-01/results/d0cece66a1b94506af0304f1b8c32850.json") as f:
    meta = json.load(f)
with open("/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/fad/agnews/query4/full-01/results/04981f2a93e845d28b18e5130ac0b946.json") as f:
    arts = json.load(f)

region = {r["article_id"]: r["region"] for r in meta}
print("meta rows:", len(meta), "articles:", len(arts))

# Weighted keyword lists for AG News classes
SPORTS = ["olympic","olympics","football","soccer","baseball","basketball","hockey","tennis","golf","nfl","nba","mlb","nhl",
"world cup","super bowl","quarterback","touchdown","inning","innings","homer","home run","playoff","playoffs","stadium",
"athlete","athletes","medal","medals","marathon","boxing","heavyweight","tournament","grand slam","yankees","red sox","lakers",
"premiership","serie a","formula one","formula 1","grand prix","nascar","cricket","rugby","wicket","goalkeeper","striker",
"midfielder","championship","tour de france","swimming","sprinter","gymnastics","fifa","uefa","athens 2004","olympic games",
"coach","roster","goal","goals","match","races","race","cyclist","cycling","skier","skiing","snowboard","skating","athletics",
"finals","semifinal","quarterfinal","knockout","pitcher","batter","hitter","slam","birdie","bogey","par","tee","lap",
"olympia","paralympic","seeded","unseeded","wimbledon","us open","french open","australian open","ryder cup","masters",
"world series","stanley cup","soccer","league","club","clubs","transfer","referee","penalty","kickoff","halftime","doping"]

BUSINESS = ["stock","stocks","shares","share price","wall street","nasdaq","dow jones","nyse","profit","profits","earnings",
"revenue","revenues","quarterly","quarter","gdp","economy","economic","inflation","interest rate","interest rates",
"federal reserve","fed ","oil price","oil prices","crude","opec","merger","acquisition","takeover","buyout","bankruptcy",
"layoffs","layoff","jobless","unemployment","ipo","dividend","investor","investors","investment","bond","bonds","treasury",
"currency","trade deficit","retail","retailer","sales","analyst","analysts","upgrade","downgrade","hedge fund","net income",
"fiscal","outlook","index","indices","market","markets","yen","euro","dollar","bank","banks","banking","loan","loans",
"credit","debt","mortgage","insurance","insurer","airline profit","stock market","bull","bear","rally in","fell sharply",
"rose sharply","percent","billion","million","fund","funds","pension","tariff","import","imports","export","exports",
"trade","wto","imf","world bank","chief executive","ceo","cfo","chairman","shareholder","shareholders","buy ","bought",
"sell","sells","sold","deal","deals","bid","bids","takeover","daimler","chrysler","ford","general motors","gm ","toyota",
"profits rose","profits fell","loss","losses","earnings report","guidance","forecast","forecasts","profit warning"]

SCITECH = ["microsoft","windows","linux","apple","macintosh","mac ","google","yahoo","ebay","internet","web","website",
"online","software","hardware","computer","computers"," pc","chip","chips","intel","amd","ibm","hewlett","hp ","dell",
"sun microsystems","oracle","sap ","cisco","nokia","motorola","sony","samsung","technology","technologies","broadband",
"wifi","wi-fi","wireless","spam","virus","viruses","hacker","hackers","encryption","open source","java","blog","blogs",
"blogging","e-mail","email","voip","cell phone","mobile phone","digital","dvd","itunes","ipod","xbox","playstation",
"video game","video games","game console","nasa","space","spacecraft","satellite","satellites","mars","shuttle","astronaut",
"astronauts","telescope","asteroid","comet","scientist","scientists","researchers","study finds","climate change","dna",
"gene","genes","genome","stem cell","stem cells","bird flu","vaccine","cancer","fda","robot","robots","physics","universe",
"fossil","evolution","global warming","titan","huygens","space station","iss ","genetic","cloning","disease","virus",
"hiv","aids","sars","flu","drug","drugs","cancer","medical","health study","brain","species","ocean","tundra","forest",
"ecosystem","biodiversity","astronomy","galaxy","solar","lunar","orbit","probe","rover","shuttle","boeing","airbus",
"browser","browsers","firefox","mozilla","netscape","search engine","antivirus","firewall","broadband","telecom",
"telecommunications","phone","phones","cellular","3g","hdtv","plasma","lcd","camera","cameras","mp3","download","downloads",
"piracy","file-sharing","file sharing","peer-to-peer","p2p","hack","security flaw","vulnerability","patch","service pack",
"spyware","adware","phishing","identity theft","e-commerce","dot-com","silicon valley","nanotechnology","biotech"]

WORLD = ["iraq","iraqi","baghdad","afghanistan","kabul","taliban","bush","kerry","president","presidential","election",
"elections","vote","votes","voters","poll","polls","government","minister","ministers","parliament","senate","senator",
"congress","white house","pentagon","troops","soldiers","army","military","war","killed","killing","bomb","bombs","bombing",
"blast","attack","attacks","militant","militants","rebels","rebel","hostage","terror","terrorist","terrorism","qaeda",
"insurgent","insurgents","police","arrest","arrested","trial","court","judge","sentenced","prison","united nations","u.n.",
" treaty","summit","diplomat","diplomatic","embassy","sanctions","nuclear","iran","iranian","north korea","pyongyang",
"seoul","china","chinese","beijing","japan","japanese","tokyo","russia","russian","moscow","putin","israel","israeli",
"palestinian","gaza","sharon","arafat","india","indian","pakistan","pakistani","kashmir","sri lanka","tsunami","earthquake",
"flood","floods","hurricane","storm","darfur","sudan","haiti","venezuela","chavez","castro","cuba","mexico","mexican",
"colombia","chile","argentina","brazil","brazilian","egypt","syria","syrian","lebanon","jordan","turkey","turkish","saudi",
"kuwait","yemen","libya","kenya","nigeria","zimbabwe","mugabe","south africa","france","french","germany","german",
"britain","british","london","paris","berlin","nato","ukraine","georgia","chechnya","chechen","indonesia","indonesian",
"philippines","thailand","vietnam","myanmar","australia","australian","canada","canadian","annan","blair","chirac",
"schroeder","shiite","sunni","kurd","kurds","falluja","najaf","basra","mosul","karzai","musharraf","powell","rumsfeld",
"cheney","campaign","republican","democrat","democratic","gop","convention","relief","humanitarian","refugee","refugees",
"ceasefire","truce","peace talks","protest","protests","rally","demonstration","opposition","lawmaker","lawmakers",
"candidate","candidates","ballot","referendum","constitution","human rights","massacre","genocide","ethnic","sectarian",
"border","immigration","asylum","visa","spy","espionage","missile","missiles","weapons","arms","wmd","iaea","envoy",
"ambassador","prime minister","foreign minister","defense minister","killed in","death toll","died","dead","victims",
"suicide bomber","car bomb","roadside bomb","gunmen","guerrillas","toll","injured","wounded","explosion","blasts",
"state department","diplomacy","clinton","edwards","vice president","governor","mayor","cabinet","spokesman","officials",
"authorities","security forces","cease-fire","insurgency","occupation","regime","aid workers","red cross","reconstruction"]

def score(text, kws):
    s = 0
    for kw in kws:
        if kw in text:
            s += 1
    return s

preds = {}
cls_counter = Counter()
samples = defaultdict(list)
for a in arts:
    aid = a["article_id"]
    title = (a.get("title") or "").lower()
    desc = (a.get("description") or "").lower()
    text = title + " " + desc
    t3 = (title + " ") * 3  # title weighted triple
    full = t3 + text
    s_sp = score(full, SPORTS)
    s_bu = score(full, BUSINESS)
    s_st = score(full, SCITECH)
    s_wo = score(full, WORLD)
    scores = {"Sports": s_sp, "Business": s_bu, "Sci/Tech": s_st, "World": s_wo}
    # small tie-break preference order: Sports > Sci/Tech > Business > World (World as catch-all when zero signal)
    best = max(scores.items(), key=lambda kv: kv[1])
    if best[1] == 0:
        cls = "World"
    else:
        # among ties, prefer non-World, then World
        mx = best[1]
        tied = [k for k, v in scores.items() if v == mx]
        if len(tied) == 1:
            cls = tied[0]
        else:
            for pref in ["Sports", "Sci/Tech", "Business", "World"]:
                if pref in tied:
                    cls = pref
                    break
    preds[aid] = cls
    cls_counter[cls] += 1
    if len(samples[cls]) < 8:
        samples[cls].append((aid, a.get("title")))

print("Class distribution:", dict(cls_counter))
for c in ["World", "Sports", "Business", "Sci/Tech"]:
    print(c, "samples:")
    for s in samples[c]:
        print("   ", s)

# Region counts among predicted World
world_region = Counter()
for a in arts:
    if preds[a["article_id"]] == "World":
        world_region[region[a["article_id"]]] += 1

print("\nWorld-category (predicted) 2015 counts by region:")
for r, n in world_region.most_common():
    print(f"  {r}: {n}")

# Reference: overall 2015 counts
overall = Counter(region.values())
print("\nOverall 2015 counts by region:")
for r, n in overall.most_common():
    print(f"  {r}: {n}")

with open("predictions.json", "w") as f:
    json.dump({str(k): v for k, v in preds.items()}, f)
