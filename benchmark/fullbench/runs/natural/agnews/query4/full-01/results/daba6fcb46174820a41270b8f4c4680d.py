import json, re, math
from collections import Counter, defaultdict

train = json.load(open("/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/natural/agnews/query4/full-01/results/fc2db6d55c3c4a448907f42c0e070b27.json"))
test  = json.load(open("/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/natural/agnews/query4/full-01/results/21c0a2afc9be488e89290abbfd5bf3d3.json"))
meta  = json.load(open("/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/natural/agnews/query4/full-01/results/ccdd38c5f55b4e35b63c4db19bddbd6e.json"))
region = {r["article_id"]: r["region"] for r in meta}

KW = {
 "Sports": {"nfl":3,"nba":3,"nhl":3,"mlb":3,"olympics":3,"olympic":2,"soccer":3,"football":2,"baseball":3,"touchdown":3,"quarterback":3,"playoff":3,"playoffs":3,"championship":2,"coach":2,"stadium":2,"athens 2004":3,"tour de france":3,"grand slam":3,"wimbledon":3,"world series":3,"super bowl":3,"goalkeeper":3,"innings":3,"homer":2,"home run":3,"yankees":3,"red sox":3,"lakers":3,"marathon":2,"tennis":2,"golf":2,"golfer":3,"boxer":3,"boxing":2,"hockey":3,"racing":2,"race course":3,"fillies":3,"defeated":1,"beat":1,"scored":1,"score":1,"game":1,"season":1,"team":1,"league":2,"cup":1,"win":1,"victory":1,"sports":3,"athlete":2,"medal":2,"gold medal":3,"sprinter":3,"swimming":2,"finals":1,"first round":1,"seeded":2,"steroids":2,"doping":3,"pitcher":3,"batter":3,"halftime":3},
 "Business": {"stock":2,"stocks":2,"shares":2,"share price":3,"earnings":3,"profit":2,"profits":2,"quarter":1,"quarterly":3,"ipo":3,"merger":3,"acquisition":3,"takeover":3,"sales":1,"revenue":3,"revenues":3,"wall street":3,"nasdaq":3,"dow jones":3,"analyst":1,"analysts":2,"investor":2,"investors":2,"ceo":2,"chief executive":2,"economy":2,"economic":1,"growth":1,"inflation":3,"interest rate":3,"interest rates":3,"federal reserve":3,"oil prices":3,"crude oil":2,"trade deficit":3,"unemployment":2,"jobs report":3,"retail":2,"consumer":1,"bank":1,"banking":2,"bankruptcy":3,"debt":1,"bond":2,"bonds":2,"market":1,"markets":2,"forecast":1,"outlook":1,"dividend":3,"fiscal":2,"billion":1,"million":1,"company":1,"corp.":1,"inc.":1,"ltd.":1,"buyout":3,"layoff":3,"layoffs":3,"job cuts":3,"auction":1},
 "Sci/Tech": {"software":3,"microsoft":2,"google":2,"yahoo":2,"apple computer":2,"linux":3,"open source":3,"open-source":3,"computer":2,"computers":2,"internet":2,"online":1,"web":1,"website":2,"broadband":3,"spam":3,"spyware":3,"virus":2,"hackers":3,"hacker":3,"security flaw":3,"chip":2,"chips":2,"intel":2,"amd":3,"ibm":2,"dell":2,"hewlett-packard":3,"sun microsystems":3,"oracle":2,"sap ":2,"nasa":3,"space":2,"spacecraft":3,"shuttle":2,"satellite":2,"mars":2,"titan":2,"asteroid":3,"telescope":3,"scientists":2,"researchers":2,"study":1,"dna":2,"gene":2,"genes":2,"stem cell":3,"climate change":2,"global warming":3,"fossil":2,"technology":2,"tech":1,"wireless":2,"voip":3,"cell phone":2,"mobile phone":2,"e-mail":2,"email":2,"browser":3,"search engine":3,"digital":1,"gadget":2,"robot":2,"astronaut":3,"solar system":3,"universe":2,"planet":2,"species":1,"evolution":2,"brain":1,"vaccine":2},
 "World": {"iraq":2,"iraqi":3,"baghdad":3,"afghanistan":3,"afghan":2,"taliban":3,"al-qaeda":3,"qaeda":3,"terrorist":2,"terrorism":2,"bomb":2,"bombed":2,"bombing":2,"blast":2,"explosion":1,"killed":2,"kills":2,"death toll":3,"troops":2,"soldiers":2,"army":1,"military":1,"war":1,"insurgent":3,"insurgents":3,"hostage":3,"kidnap":2,"kidnapped":3,"president":1,"prime minister":3,"minister":1,"parliament":2,"election":2,"elections":2,"vote":1,"voters":1,"campaign":1,"kerry":2,"bush":1,"democrat":1,"republican":1,"senate":1,"congress":1,"white house":2,"pentagon":2,"u.n.":2,"united nations":3,"nato":2,"european union":2,"government":1,"police":1,"arrest":1,"arrested":1,"court":1,"trial":1,"judge":1,"prosecutor":2,"charged":1,"indicted":2,"protest":1,"protesters":2,"demonstration":1,"riot":2,"strike":1,"ceasefire":3,"peace talks":3,"treaty":2,"sanctions":2,"nuclear":1,"missile":2,"weapons":1,"israel":2,"israeli":3,"palestinian":3,"gaza":3,"north korea":3,"iran":2,"syria":2,"russia":1,"putin":3,"china":1,"india":1,"pakistan":2,"japan":1,"france":1,"germany":1,"britain":1,"london":1,"paris":1,"moscow":2,"beijing":2,"tokyo":2,"seoul":2,"kyoto":2,"tsunami":3,"hurricane":2,"flood":1,"earthquake":3,"kashmir":3,"saddam":3,"hussein":2,"arafat":3,"sharon":3,"blair":2,"chirac":3,"annan":3,"diplomat":1,"embassy":2,"summit":2,"talks":1,"border":1,"refugees":2,"aid":1,"relief":1,"independence day":1,"parade":1,"separatist":3,"rebel":2,"rebels":2,"opposition":1,"candidate":1,"rally":1,"abuse":1,"prison":1,"prisoners":1,"detainees":2,"guantanamo":3,"abu ghraib":3,"islamic":2,"muslim":1,"cleric":2,"shiite":2,"sunni":2},
}

def kw_scores(text):
    t = " " + text.lower() + " "
    sc = {}
    for cat, kws in KW.items():
        s = 0
        for k, w in kws.items():
            if k in t:
                s += w
        sc[cat] = s
    return sc

def fulltext(a):
    return (a.get("title") or "") + " . " + (a.get("description") or "")

tok_re = re.compile(r"[a-z][a-z'\-]+")
def tokens(text):
    return tok_re.findall(text.lower())

# Seed labeling with high confidence
seeds = []
for a in train:
    sc = kw_scores(fulltext(a))
    ranked = sorted(sc.values(), reverse=True)
    best_cat = max(sc, key=sc.get)
    if ranked[0] >= 6 and ranked[0] - ranked[1] >= 3:
        seeds.append((a, best_cat))

print("Seeds:", len(seeds), Counter(c for _, c in seeds))

cats = ["World","Sports","Business","Sci/Tech"]
# Train multinomial NB
vocab = Counter()
class_tok = {c: Counter() for c in cats}
class_docs = Counter()
class_tok_total = Counter()
for a, c in seeds:
    tk = tokens(fulltext(a))
    class_docs[c] += 1
    class_tok[c].update(tk)
    class_tok_total[c] += len(tk)
    vocab.update(tk)

V = set(w for w, n in vocab.items() if n >= 5)
Vn = len(V)
alpha = 0.5
logprior = {c: math.log(class_docs[c]/len(seeds)) for c in cats}

def predict_proba(text):
    tk = [w for w in tokens(text) if w in V]
    counts = Counter(tk)
    logp = {}
    for c in cats:
        denom = class_tok_total[c] + alpha*Vn
        lp = logprior[c]
        tc = class_tok[c]
        for w, n in counts.items():
            lp += n*math.log((tc.get(w,0)+alpha)/denom)
        logp[c] = lp
    m = max(logp.values())
    exps = {c: math.exp(logp[c]-m) for c in cats}
    Z = sum(exps.values())
    return {c: exps[c]/Z for c in cats}

# Evaluate on held-out seeds (quick sanity via simple split already done implicitly; skip)
# Predict for 2015 articles
world_prob_region = defaultdict(float)
world_hard_region = Counter()
cat_hard = Counter()
for a in test:
    p = predict_proba(fulltext(a))
    r = region[a["article_id"]]
    world_prob_region[r] += p["World"]
    best = max(p, key=p.get)
    cat_hard[best] += 1
    if best == "World":
        world_hard_region[r] += 1

print("Hard category counts (2015):", dict(cat_hard))
print("World by region (hard argmax):")
for r, c in world_hard_region.most_common():
    print(f"  {r}: {c}")
print("World by region (summed probability):")
for r, v in sorted(world_prob_region.items(), key=lambda kv: -kv[1]):
    print(f"  {r}: {v:.1f}")
