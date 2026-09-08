# 失败、解析覆盖和审计

**进度：108/108 次运行已结束。全量运行已结束。**

验证失败是原始验证器结果，保留错误轨迹，不以重新作答提高通过率。未完成任务不等同失败。

- DEPS_DEV_V1/query2 / fad：Missing project name: sveltejs/svelte
- GITHUB_REPOS/query1 / fad：No value in LLM output rounds to 0.33
- GITHUB_REPOS/query2 / fad：No fuzzy match found for 'swiftandroid/swift' within 3-character distance

审计待核对 GITHUB_REPOS/query4 / fad：
```json
{
  "kind": "non_adapter_bash_review",
  "index": 20,
  "command": "grep -o '\"repo_name\": \"[^\"]*torvalds[^\"]*\"' /data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/fad/GITHUB_REPOS/query4/full-01/results/58d575041f3a4c948b61cef08b746e68.json | head; echo \"---\"; grep -c 'torvalds/linux' /data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/fad/GITHUB_REPOS/query4/full-01/results/58d575041f3a4c948b61cef08b746e68.json"
}
```
- PANCANCER_ATLAS/query1 / fad：Missing histology type: 9382/3

审计待核对 PANCANCER_ATLAS/query2 / fad：
```json
{
  "kind": "non_adapter_bash_review",
  "index": 10,
  "command": "grep -io '\"column_name\": \"[^\"]*\"' /data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/fad/PANCANCER_ATLAS/query2/full-01/results/818a166389ea4751a69f268b63961875.json | grep -i -E 'vital|status|acronym|type|barcode|cancer|description'"
}
```

审计待核对 PANCANCER_ATLAS/query3 / fad：
```json
{
  "kind": "non_adapter_bash_review",
  "index": 12,
  "command": "grep -oiE '\"column_name\": \"[^\"]*(gender|sex|acronym|type|cancer|bcr|barcode)[^\"]*\"' /data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/fad/PANCANCER_ATLAS/query3/full-01/results/4f09a0227ea741b085dd6092706f5c61.json | sort -u"
}
```

审计待核对 PANCANCER_ATLAS/query3 / fad：
```json
{
  "kind": "non_adapter_bash_review",
  "index": 14,
  "command": "python3 -c \"\nimport json\nrows=json.load(open('/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/fad/PANCANCER_ATLAS/query3/full-01/results/4f09a0227ea741b085dd6092706f5c61.json'))\nprint(len(rows))\nprint([r['column_name'] for r in rows])\n\""
}
```
- PATENTS/query1 / fad：Missing CPC code: A22B
- PATENTS/query3 / fad：No match for: BLOOM ENERGY CORP + PROCESSES OR MEANS, e.g. BATTERIES, FOR THE DIRECT CONVERSION OF CHEMICAL ENERGY INTO ELECTRICAL ENERGY

审计待核对 agnews/query1 / fad：
```json
{
  "kind": "non_adapter_bash_review",
  "index": 38,
  "command": "/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/bookreview/.venv/bin/python -c \"\nimport json\ndata = json.load(open('/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/fad/agnews/query1/full-01/results/f6ab9504fb754fc6a941262d5a730059.json'))\nfor d in data:\n    print(d['article_id'], d['desc_len'], '|', d['title'])\n\""
}
```

审计待核对 agnews/query1 / fad：
```json
{
  "kind": "non_adapter_bash_review",
  "index": 48,
  "command": "/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/bookreview/.venv/bin/python -c \"\nimport json\ndata = json.load(open('/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/fad/agnews/query1/full-01/results/4598ab18d5df4b238ac4856d1b289391.json'))\nfor d in data:\n    print(d['article_id'], d['desc_len'], '|', d['title'])\n\""
}
```

审计待核对 agnews/query1 / fad：
```json
{
  "kind": "non_adapter_bash_review",
  "index": 74,
  "command": "/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/bookreview/.venv/bin/python -c \"\nimport json\ndata = json.load(open('/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/fad/agnews/query1/full-01/results/80df329b4afa456e92ef38fb304379cb.json'))\nfor d in data:\n    if d['article_id'] == 69413:\n        print('title:', d['title'])\n        print('len:', len(d['description']))\n\""
}
```
- agnews/query2 / fad：No answer submitted
- agnews/query3 / fad：Ground truth numeric value '336.6363636363636' (tol=0.01) not found in LLM output: Answer: approximately 41.82 business articles per year (460 total over 11 years, 2010-2020).

Method: Business articles were identified from the MongoDB articles collection as those whose title or description contains the word "business" (case-insensitive; 4018 articles matched). These were joined with the SQLite article_metadata table filtered to region = 'Europe' and publication dates from 2010-01-01 to 2020-12-31.

Per-year counts in Europe:
2010: 45, 2011: 44, 2012: 35, 2013: 46, 2014: 40, 2015: 34, 2016: 44, 2017: 41, 2018: 41, 2019: 46, 2020: 44

Total = 460; Average = 460 / 11 ≈ 41.82 articles per year.
- agnews/query4 / fad：No answer submitted

审计待核对 agnews/query4 / fad：
```json
{
  "kind": "non_adapter_bash_review",
  "index": 48,
  "command": "cat > analysis.py <<'PYEOF'\nimport json, re\nfrom collections import Counter\n\nRES = \"/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/fad/agnews/query4/full-01/results/\"\nwith open(RES + \"0398bda632db421094f2e5cd8159b5d6.json\") as f:\n    meta = json.load(f)\nwith open(RES + \"1eccd19d29af435aa0907404de634b24.json\") as f:\n    arts = json.load(f)\n\nregion_of = {r[\"article_id\"]: r[\"region\"] for r in meta}\n\nKW = {}\nKW[\"World\"] = ('iraq iraqi iraqis baghdad fallujah najaf iran iranian iranians tehran afghanistan afghan afghans kabul karzai allawi pakistan pakistani islamabad india indian kashmir china chinese beijing japan japanese tokyo korea korean pyongyang seoul taiwan taiwanese russia russian moscow putin britain british london blair france french paris chirac germany german berlin italy italian rome spain spanish madrid europe european nato israel israeli israelis palestinian palestinians gaza sharon arafat syria syrian lebanon lebanese beirut egypt egyptian cairo turkey turkish ankara saudi riyadh kuwait jordan yemen sudan sudanese darfur africa african nigeria nigerian kenya zimbabwe libya libyan morocco tunisia algeria ghana ghanaian liberia somalia rwanda congo uganda ethiopia eritrea namibia angola zambia tanzania mozambique senegal mali niger chad cameroon malawi '\n 'united nations annan security council taliban al qaeda al-qaeda qaeda bin laden terror terrorism terrorist terrorists insurgent insurgents militant militants hostage hostages bomb bombs bombing bombings blast blasts killed kills killing killings dead deaths died attack attacks attacker troop troops soldier soldiers army war rebel rebels ceasefire truce peace envoy diplomat diplomats diplomatic embassy '\n 'election elections elect vote votes voting voter voters ballot polls parliament parliamentary president presidential premier prime minister minister ministers government opposition congress congressional senate senator white house washington bush kerry cheney edwards campaign campaigns candidate candidates democrat democratic republican republicans gop administration court trial judge charged charges guilty verdict sentence sentenced prison jail police arrested arrest probe investigation scandal nuclear weapon weapons sanctions talks '\n 'pope vatican church hurricane charley ivan storm earthquake tsunami flood floods flooding aid relief refugee refugees human rights protest protests protesters rally demonstration coup violence clash clashes assassination assassinated mexico mexican venezuela venezuelan chavez colombia colombian haiti haitian cuba cuban castro ukraine ukrainian chechnya chechen indonesia indonesian malaysia philippines philippine thailand thai vietnam vietnamese myanmar nepal bangladesh sri lanka australia australian howard canada canadian chile argentina brazil brazilian peru serbia serbian kosovo bosnia bosnian croatia albania macedonia romania bulgaria hungary poland polish czech austria austrian swiss switzerland sweden swedish norway norwegian denmark danish finland finnish netherlands dutch belgium belgian brussels portugal portuguese lisbon greece greek ireland irish dublin iceland estonia latvia lithuania slovenia slovakia moldova armenia azerbaijan kazakhstan uzbekistan mongolia cambodia laos mideast middle east gulf emirates qatar bahrain oman ')\nKW[\"Sports\"] = ('sport sports sporting football baseball basketball hockey soccer tennis golf golfer nfl nba mlb nhl ncaa olympic olympics olympian game games coach coaches coached coaching quarterback touchdown touchdowns playoff playoffs championship championships league leagues season seasons preseason postseason team teams teammate player players score scores scored scoring win wins winner winning victory victories loss losses lost beat beats beating defeat defeats defeated match matches tournament tournaments inning innings homer homers yankees mets phillies braves marlins astros cardinals cubs dodgers giants padres angels athletics twins orioles royals tigers indians mariners rangers brewers pirates reds nationals expos diamondbacks rockies lakers celtics knicks nets pistons pacers bulls heat magic wizards hornets hawks bucks raptors sixers cavaliers spurs mavericks rockets grizzlies jazz nuggets timberwolves sonics warriors clippers kings suns sharks bruins sabres flyers penguins devils islanders canadiens canucks oilers flames avalanche stars blues predators wild coyotes ducks thrashers hurricanes panthers lightning capitals patriots cowboys eagles jets redskins packers bears vikings lions buccaneers falcons saints rams seahawks chargers raiders broncos chiefs dolphins bills ravens bengals browns steelers texans colts jaguars titans '\n 'stadium arena race racing racer nascar ferrari mclaren boxing boxer bout medal medals medalist athlete athletes athletic athletics sprint sprinter marathon swimmer swimming gymnastics gymnast skater skating ski skiing skier snowboard roster draft drafted trade traded catcher pitcher pitchers pitching batter batters batting hitter hitters hitting slugger fielder outfielder infielder shortstop baseman goalie goaltender goalkeeper defenseman referee umpire atp wta wimbledon masters augusta armstrong athens doping steroid steroids suspension suspended injury injured injuries shutout overtime preseason scrimmage mvp clubhouse beckham zidane ronaldo barcelona manchester arsenal chelsea liverpool juventus davenport williams serena venus sharapova henin clijsters federer agassi roddick hewitt safin woods mickelson schumacher barrichello montoya earnhardt olympiad paralympic red sox white sox maple leafs blue jackets mighty ducks grand prix formula one formula 1 world cup super bowl world series stanley cup final four march madness us open u.s. open french open australian open tour de france tiger woods michael schumacher jeff gordon premier league champions league uefa fifa hat trick all-star all star ')\nKW[\"Business\"] = ('business businesses economy economic economies stock stocks share shares shareholder shareholders market markets dow nasdaq profit profits profitable earnings revenue revenues sale sales quarter quarterly company companies corp corporation corporations ceo cfo chairman executive executives merger mergers acquisition acquisitions acquire acquired buyout takeover ipo investor investors investment investments investing bank banks banking banker bankers citigroup hsbc barclays wachovia fed greenspan inflation deflation dollar dollars euro euros yen currency currencies forex oil crude barrel barrels opec gasoline fuel prices price pricing retail retailer retailers retailing store stores shop shops shopping consumer consumers walmart wal-mart target kmart sears costco gap nordstrom macys saks kroger safeway albertsons airline airlines airways boeing airbus jetblue southwest qantas lufthansa jobs jobless unemployment layoffs layoff hiring hires workers union unions trade tariffs tariff imports exports import export gdp growth recession slowdown recovery forecast forecasts analyst analysts bonds bond treasury treasuries yield yields mortgage mortgages housing insurance insurer insurers pension pensions bankruptcy bankrupt dividend dividends buyback outlook guidance downgrade downgraded upgrade upgraded billion million trillion nyse amex ftse cac dax nikkei index indices futures commodities commodity gold silver copper wheat corn soybeans coffee cotton equities equity portfolio sec accounting accountant auditors auditor fraud enron worldcom tyco adelphia parmalat halliburton exxon exxonmobil mobil chevron bp shell ford gm daimlerchrysler chrysler toyota honda nissan volkswagen bmw hyundai ge siemens philips sony matsushita samsung nokia motorola ericsson lucent alcatel nortel pfizer merck lilly unilever nestle coke pepsi pepsico mcdonalds starbucks disney viacom comcast directv verizon bellsouth vodafone telefonica alitalia fiat santander mizuho oecd imf nafta advertising ads media newspaper newspapers circulation publishing publisher publishers gannett mcclatchy lottery casino casinos gambling hotel hotels marriott hilton hyatt tourism travel cruise restaurant restaurants apparel clothing fashion nike adidas reebok avon revlon whirlpool maytag caterpillar deere cummins paccar raytheon honeywell textron bombardier embraer ups fedex dhl railroad csx truckers trucking ryder '\n 'wall street dow jones s&p standard & poor first quarter second quarter third quarter fourth quarter interest rate interest rates federal reserve exchange rate oil prices crude oil gas prices consumer spending consumer confidence home depot best buy circuit city toys r us j.c. penney whole foods british airways air france job cuts labor market trade deficit trade gap gross domestic product stock market stock exchange market value market cap earnings per share net income net profit net loss operating income profit warning profit-taking credit rating new york stock exchange venture capital private equity hedge fund mutual fund mutual funds securities and exchange ernst & young martha stewart chapter 10-year general motors general electric procter & gamble coca-cola burger king time warner at&t deutsche telekom france telecom bt group credit lyonnais bnp paribas societe generale bank of japan european central bank bank of england world bank world trade organization free trade news corp knight ridder new york times washington post wall street journal usa today warner music universal music las vegas box office ')\nKW[\"Sci/Tech\"] = ('technology technologies tech software hardware computer computers computing laptop laptops notebook notebooks desktop desktops server servers internet web website websites webpage online offline broadband dsl isp isps msn google yahoo ebay amazon mac macintosh imac ipod itunes microsoft windows xp vista longhorn office word excel powerpoint outlook explorer netscape mozilla firefox opera safari browser browsers linux redhat suse novell mandrake debian opensource gnu gpl apache ibm intel amd athlon opteron pentium centrino chip chips chipset microprocessor processor processors semiconductor semiconductors dell compaq gateway oracle sap siebel peoplesoft veritas symantec mcafee cisco juniper qualcomm rim blackberry palm palmsource handspring pda pdas cellphone cellphones handset handsets sms wireless wi-fi wifi wimax bluetooth gsm cdma gprs canon nikon olympus kodak mp3 napster kazaa filesharing piracy pirated copyright copyrights riaa drm spam spammers spamming email virus viruses worm worms trojan hacker hackers hacking vulnerability vulnerabilities patch patches firewall encryption decrypt phishing spyware adware blog blogs blogger bloggers blogging weblog weblogs rss podcast podcasting voip skype im chat myspace friendster flickr database databases storage memory ram lcd plasma hdtv dvr tivo videogame videogames playstation ps2 xbox gamecube nintendo gaming gamer gamers '\n 'world wide web service provider america online apple computer mac os open source sun microsystems bea systems trend micro computer associates cisco systems lg electronics research in motion cell phone cell phones mobile phone mobile phones text messaging text message digital camera digital cameras digital music mp3 player mp3 players file sharing peer to peer junk e-mail junk email electronic mail computer virus trojan horse security flaw security hole software update security update pop-up search engine search engines web search google search voice over ip internet phone instant messaging instant message chat room chat rooms social network social networking data storage hard drive hard drives disk drive flash memory usb drive flat panel digital tv digital television video game video games game console electronic arts computer game computer games halo doom half-life grand theft auto world of warcraft sims everquest final fantasy silicon valley '\n 'nasa space shuttle shuttles columbia discovery atlantis endeavour iss astronaut astronauts cosmonaut cosmonauts rocket rockets launch launches launched satellite satellites spacecraft probe probes mars rover rovers cassini huygens titan saturn jupiter venus mercury planet planets asteroid asteroids comet comets telescope telescopes hubble observatory astronomy astronomer astronomers galaxy galaxies universe supernova rutan science sciences scientist scientists scientific research researcher researchers study studies journal lab labs laboratory laboratories experiment experiments nobel physics physicist physicists chemistry chemist biologist biologists biology biotech biotechnology genetic genetics gene genes genome genomic genomics dna rna cloning clone clones cloned embryo embryos embryonic species evolution darwin fossil fossils dinosaur dinosaurs archaeology archaeologists greenhouse co2 emissions kyoto environment environmental epa pollution ecosystem ecosystems endangered extinction biodiversity cancer cancers tumor tumors leukemia lymphoma melanoma disease diseases diabetes obesity stroke strokes alzheimer parkinson aids hiv flu influenza vaccine vaccines vaccination drug drugs medicine medicines medical fda approval patient patients doctor doctors physicians hospital hospitals surgeon surgeons surgery transplant health healthcare depression antidepressant antidepressants vioxx celebrex bextra arthritis cholesterol statin statins lipitor hypertension therapy therapies treatment treatments treated cure neuron neurons brain sleep diet diets dieting smoking smokers tobacco cigarette cigarettes nicotine drinkers drinking alcohol vitamin vitamins supplement supplements antioxidant antioxidants caffeine cells protein proteins molecule molecules molecular atomic atoms particle particles quantum nanotech nanotechnology nanoscale robot robots robotic robotics '\n 'space shuttle international space station space station space launch mars rover space telescope solar system big bang black hole light years ansari x prize stem cell stem cells gene therapy human genome natural selection climate change global warming carbon dioxide air pollution water pollution national geographic breast cancer prostate cancer lung cancer heart disease heart attack multiple sclerosis bird flu avian flu clinical trial clinical trials food and drug administration side effects health care mental health blood pressure weight loss secondhand smoke red wine green tea physical activity cell lines particle physics artificial intelligence computer science press release study finds study suggests researchers found researchers say scientists say scientists have new research according to the study ')\n\nPAT = {}\nfor cls, s in KW.items():\n    words = [w for w in s.split('  ') ]\n    # split on spaces but keep multiword phrases: rebuild list manually\n    terms = s.split()\n    # rebuild multiword: use known multiword list embedded - simpler: split by single spaces, but multiword terms got split.\n    PAT[cls] = None\n\n# Instead: define term lists with pipe separators for phrases\ndef build(s):\n    terms = [t.strip() for t in s.replace('  ', ' |').split('|')]\n    out = []\n    for grp in terms:\n        for t in grp.split(' | '):\n            pass\n    return None\n\n# Simpler robust approach: terms separated by spaces, multi-word phrases joined with underscore\ndef munge(s):\n    return s\n\nPYEOF\necho \"draft - will rewrite cleanly\""
}
```
- crmarenapro/query12 / fad：Found agent IDs ['005Wt000003NEa3IAG'], but expected '005Wt000003NDEBIA4'
- 已核对 crmarenapro/query12 / fad / 消息 1：已核对：仅在当前指定目录执行 pwd/ls，无数据库访问或外部内容读取。 [代码](../runs/fad/crmarenapro/query12/full-01/audit/shell-message-1.sh)
- crmarenapro/query13 / fad：Found agent IDs ['005Wt000003NHw5IAG'], but expected '005Wt000003NIXCIA4'
- crmarenapro/query2 / fad：Found knowledge article IDs ['ka0Wt000000Ens5IAC'], but expected 'ka0Wt000000Eq0MIAS'
- 已核对 crmarenapro/query2 / fad / 消息 9：人工逐段核对：仅以 json/re 读取本运行已有 results 文件、筛选和打印文本；未直接访问数据库或外部答案。属于 Python 工具协议偏离。 [代码](../runs/fad/crmarenapro/query2/full-01/audit/direct-python-message-9.py)
- 已核对 crmarenapro/query2 / fad / 消息 11：人工逐段核对：仅以 json/re 读取本运行已有 results 文件、筛选和打印文本；未直接访问数据库或外部答案。属于 Python 工具协议偏离。 [代码](../runs/fad/crmarenapro/query2/full-01/audit/direct-python-message-11.py)
- 已核对 crmarenapro/query2 / fad / 消息 21：人工逐段核对：仅以 json/re 读取本运行已有 results 文件、筛选和打印文本；未直接访问数据库或外部答案。属于 Python 工具协议偏离。 [代码](../runs/fad/crmarenapro/query2/full-01/audit/direct-python-message-21.py)
- 已核对 crmarenapro/query2 / fad / 消息 23：人工逐段核对：仅以 json/re 读取本运行已有 results 文件、筛选和打印文本；未直接访问数据库或外部答案。属于 Python 工具协议偏离。 [代码](../runs/fad/crmarenapro/query2/full-01/audit/direct-python-message-23.py)
- 已核对 crmarenapro/query2 / fad / 消息 25：人工逐段核对：仅以 json/re 读取本运行已有 results 文件、筛选和打印文本；未直接访问数据库或外部答案。属于 Python 工具协议偏离。 [代码](../runs/fad/crmarenapro/query2/full-01/audit/direct-python-message-25.py)
- crmarenapro/query7 / fad：Found knowledge article IDs ['ka0Wt000000EpSUIA0'], but expected 'ka0Wt000000EoD3IAK'
- 已核对 crmarenapro/query7 / fad / 消息 31：人工核对：grep 仅检查本运行已有查询结果中的 ID。未访问外部数据或数据库。 [代码](../runs/fad/crmarenapro/query7/full-01/audit/shell-message-31.sh)
- 已核对 crmarenapro/query7 / fad / 消息 85：人工核对：直接 Python 仅读取本运行结果并筛选/打印；SQL 未绕过适配器。属于 Python 协议偏离；消息 103 另对输出排序。 [代码](../runs/fad/crmarenapro/query7/full-01/audit/direct-python-message-85.py)
- 已核对 crmarenapro/query7 / fad / 消息 87：人工核对：直接 Python 仅读取本运行结果并筛选/打印；SQL 未绕过适配器。属于 Python 协议偏离；消息 103 另对输出排序。 [代码](../runs/fad/crmarenapro/query7/full-01/audit/direct-python-message-87.py)
- 已核对 crmarenapro/query7 / fad / 消息 103：人工核对：直接 Python 仅读取本运行结果并筛选/打印；SQL 未绕过适配器。属于 Python 协议偏离；消息 103 另对输出排序。 [代码](../runs/fad/crmarenapro/query7/full-01/audit/direct-python-message-103.py)
- googlelocal/query2 / fad：No score found after name: Elite Massage
- googlelocal/query4 / fad：Number 19 not found near Encino Dermatology & Laser
- music_brainz_20k/query1 / fad：Ground truth '1059.46' not found in LLM output: Apple Music made a total of $601.44 USD in revenue from Beyoncé's song "Get Me Bodied" in Canada.

Methodology:
1. In the tracks database, I found 3 track records matching Beyoncé's "Get Me Bodied" (track_ids 4233, 12954, 15158), all from the "Sexxxplicit R&B, Volume 25" release (2007) but from different sources.
2. In the sales database, filtering for these track_ids with country = 'Canada' and store = 'Apple Music' returned 2 sale records:
   - track_id 4233: 354 units, $377.62
   - track_id 12954: 210 units, $223.82
   (track_id 15158 had no Apple Music sales in Canada.)
3. Total revenue = $377.62 + $223.82 = $601.44 USD (564 units total).

Answer: $601.44 USD

- music_brainz_20k/query3 / fad：No fuzzy match (Zo gaat het leven aan je voor) found in The song that generated the highest total revenue in USD across all stores and countries is:

"Systemisch bled" by Stüngö
- Track ID: 14719
- Album: "Um wos gehts'n?" (2009)
- Total revenue: $2,522.82 USD
- Total units sold: 2,109 (across 5 sale records spanning multiple stores/countries)

Method: Summed revenue_usd from the sales table (DuckDB) grouped by track_id, then joined the top result to the tracks table (SQLite) for the title/artist. The runner-up was "011-I'll Tell You" by The BGeau Brummels (track_id 5124) at $2,503.19, about $19.63 less. A robustness check aggregating by title+artist across duplicate track records did not reveal any legitimately duplicated song that would surpass this total (the only larger groupings were artifacts of null/placeholder titles from different unrelated tracks), confirming the per-track answer.. Best score: 0.03
- stockindex/query2 / fad：Target 'IXIC' not stated as primary answer (not in first 200 chars).
- stockmarket/query4 / fad：Name not found within 5 edits: 'Argo Group International Holdings, Ltd', closest: 'er-toledo international, inc. (' (distance=19)

审计待核对 yelp/query7 / fad：
```json
{
  "kind": "non_adapter_bash_review",
  "index": 48,
  "command": "/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/bookreview/.venv/bin/python -c \"\nimport json\nd=json.load(open('/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/fad/yelp/query7/full-01/results/a3683be94f2e4dfa9c8b9fe7f6f0259a.json'))\nprint(d['stdout'])\" | tail -55"
}
```
- DEPS_DEV_V1/query1 / natural：Missing or mis-versioned above-cutoff package: @dmrvos/infrajs>0.0.6>typescript 2.6.2
- DEPS_DEV_V1/query2 / natural：Missing project name: sveltejs/svelte

审计待核对 DEPS_DEV_V1/query2 / natural：
```json
{
  "kind": "non_adapter_bash_review",
  "index": 19,
  "command": "python3 - <<'EOF'\nnames = [l.strip() for l in open(\"project_names.txt\") if l.strip()]\nnames.append(\"reactjs-ui/reactjs-pull-refresh\")\nnames.append(\"sfundomhlungu/-dot.product-createlib\")\nnames = sorted(set(names))\ninlist = \", \".join(\"'%s'\" % n.replace(\"'\", \"''\") for n in names)\nsql = (\"SELECT Name, Version, ProjectName FROM project_packageversion \"\n       \"WHERE System='NPM' AND ProjectType='GITHUB' AND ProjectName IN (%s);\" % inlist)\nopen(\"q8.sql\", \"w\").write(sql)\nprint(len(names), \"names\")\nEOF"
}
```

审计待核对 DEPS_DEV_V1/query2 / natural：
```json
{
  "kind": "non_adapter_bash_review",
  "index": 23,
  "command": "python3 - <<'EOF'\nimport json\nrows = json.load(open(\"/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/natural/DEPS_DEV_V1/query2/full-01/results/add329c0d8af4331841ebf4ed8df7442.json\"))\nnames = sorted({r[\"Name\"] for r in rows})\ninlist = \", \".join(\"'%s'\" % n.replace(\"'\", \"''\") for n in names)\nsql = (\"SELECT Name, Version, Licenses, VersionInfo FROM packageinfo \"\n       \"WHERE System='NPM' AND Licenses LIKE '%\\\"MIT\\\"%' \"\n       \"AND VersionInfo LIKE '%\\\"IsRelease\\\": true%' AND Name IN (%s);\" % inlist)\nopen(\"q9.sql\", \"w\").write(sql)\nprint(len(names), \"distinct names\")\nEOF"
}
```

审计待核对 DEPS_DEV_V1/query2 / natural：
```json
{
  "kind": "non_adapter_bash_review",
  "index": 25,
  "command": "python3 - <<'EOF'\nimport json\nrows = json.load(open(\"/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/natural/DEPS_DEV_V1/query2/full-01/results/add329c0d8af4331841ebf4ed8df7442.json\"))\nnames = sorted({r[\"Name\"] for r in rows})\ninlist = \", \".join(\"'\" + n.replace(\"'\", \"''\") + \"'\" for n in names)\nsql = (\"SELECT Name, Version, Licenses, VersionInfo FROM packageinfo \"\n       \"WHERE System='NPM' AND Licenses LIKE '%\\\"MIT\\\"%' \"\n       \"AND VersionInfo LIKE '%\\\"IsRelease\\\": true%' AND Name IN (\" + inlist + \");\")\nopen(\"q9.sql\", \"w\").write(sql)\nprint(len(names), \"distinct names\")\nEOF"
}
```
- GITHUB_REPOS/query1 / natural：No value in LLM output rounds to 0.33

审计待核对 GITHUB_REPOS/query1 / natural：
```json
{
  "kind": "non_adapter_bash_review",
  "index": 14,
  "command": "cd /data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/natural/GITHUB_REPOS/query1/full-01 2>/dev/null || true; /data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/bookreview/.venv/bin/python - <<'EOF'\nimport json\nrows = json.load(open('/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/natural/GITHUB_REPOS/query1/full-01/results/665c02b536b54d818800744da2ca9027.json'))\nrepos = sorted(set(r['sample_repo_name'] for r in rows))\nprint(len(repos))\nsql = \"SELECT repo_name, language_description FROM languages WHERE repo_name IN (%s);\" % \",\".join(\"'%s'\" % r.replace(\"'\",\"''\") for r in repos)\nopen('q7.sql','w').write(sql)\nprint(\"written\")\nEOF"
}
```
- GITHUB_REPOS/query4 / natural：Could not match: 'tensorflow/tensorflow'
- PANCANCER_ATLAS/query1 / natural：Missing histology type: 9382/3

审计待核对 PANCANCER_ATLAS/query1 / natural：
```json
{
  "kind": "non_adapter_bash_review",
  "index": 13,
  "command": "pwd && ls"
}
```

审计待核对 PANCANCER_ATLAS/query3 / natural：
```json
{
  "kind": "non_adapter_bash_review",
  "index": 4,
  "command": "cat \"/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/natural/PANCANCER_ATLAS/query3/full-01/results/cf7b5bb373cd4969a61abb83c7929698.json\" | /data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/bookreview/.venv/bin/python -c \"import json,sys; d=json.load(sys.stdin); [print(r['column_name']) for r in d]\""
}
```
- PATENTS/query1 / natural：Missing CPC code: A22B

审计待核对 PATENTS/query1 / natural：
```json
{
  "kind": "non_adapter_bash_review",
  "index": 22,
  "command": "{ echo \"WITH p AS (SELECT rowid AS rid, CASE\"; for y in $(seq 1976 2024); do echo \"WHEN filing_date LIKE '%$y%' THEN $y\"; done; echo \"END AS yr, cpc FROM publicationinfo),\"; echo \"e AS (SELECT DISTINCT p.rid AS rid, p.yr AS yr, substr(json_extract(j.value,'\\$.code'),1,4) AS sub FROM p, json_each(p.cpc) AS j WHERE p.yr IS NOT NULL)\"; echo \"SELECT sub, yr, COUNT(*) AS cnt FROM e GROUP BY sub, yr ORDER BY sub, yr;\"; } > query.sql && head -5 query.sql && tail -3 query.sql"
}
```

审计待核对 PATENTS/query1 / natural：
```json
{
  "kind": "non_adapter_bash_review",
  "index": 32,
  "command": "cp answer_codes.txt final.txt && cat final.txt | tr '\\n' ' ' | head -c 2000; echo; wc -l final.txt"
}
```
- PATENTS/query2 / natural：Name fuzzy match failed for 'BAKING; EDIBLE DOUGHS' (best match: 'henrankedallgroups', distance=12)
- PATENTS/query3 / natural：No match for: BLOOM ENERGY CORP + PROCESSES OR MEANS, e.g. BATTERIES, FOR THE DIRECT CONVERSION OF CHEMICAL ENERGY INTO ELECTRICAL ENERGY
- agnews/query2 / natural：Ground truth '0.14414414414414414' (tol=0.0001) not found in LLM output: ANSWER: 24/111 ≈ 0.216 (about 21.6%, roughly one-fifth) of Amy Jones's articles belong to the Science/Technology category.

METHOD:
1. Looked up author "Amy Jones" in metadata_database.authors -> author_id = 218.
2. Queried metadata_database.article_metadata for her articles -> 111 articles (all her authored articles).
3. Retrieved the title and description of each of the 111 articles from articles_database.articles.
4. Neither database stores an explicit category field, so each article was assigned to its AG News-style category (World / Sports / Business / Sci-Tech) from its title and description. 24 articles were classified as Science/Technology (space/NASA, science research, software/internet, telecom/wireless, and tech-industry stories).

RESULT: 24 Science/Technology articles out of 111 total = 0.2162 (~21.6%).

The 24 Science/Technology articles:
- 192: GameBoy mini-games win prize
- 2844: Students Win $100,000 in National Team Science Competition
- 2987: Energy from waves - teenager wins science award
- 15473: In Iraq, a Quest to Rebuild One More Broken Edifice: Science
- 17491: UPDATE: Intel lowers Q3 revenue estimates
- 22354: Space Probe Fails to Deploy Its Parachute and Crashes
- 24495: Shuttle repair price tag soars
- 25960: Microsoft settles with UK phone maker
- 35882: EMC Unveils E-mail Storage For Microsoft Exchange
- 41616: TechBrief: Vodafone seeks new frontiers
- 46531: Ex-Astronaut Casts Doubt on Space Tourism
- 64102: Texas Instruments Posts Higher 3Q Profits
- 73025: FCC Approves Merger, Wireless Giant Created
- 89666: Vote Fraud Theories, Spread by Blogs, Are Quickly Buried
- 91822: AMCC to Lay Off 150
- 92992: Revealed: why the fear factor runs with the pack
- 105804: HP to launch 'virus-throttling' software
- 106908: XM CEO Sees Satellite Radio on Cell Phones
- 108586: EBay Adds 'Want It Now' Feature
- 109601: Chinese Firm To Buy IBM's PC Business For $1.75 Billion
- 112770: Paypal and Apple iTunes link-up
- 116698: US mobile groups confirm merger
- 119651: Bush Ordering Better Ocean Oversight
- 126655: Log on to be a satellite spy

LIMITATION: The databases contain no explicit category column, so the classification is content-based; a few borderline tech-business stories could shift the count slightly, but the fraction is approximately 0.22 (about one-fifth, close to the expected 25% share of Sci/Tech in the corpus).

审计待核对 agnews/query2 / natural：
```json
{
  "kind": "non_adapter_bash_review",
  "index": 9,
  "command": "cat > mq2.json <<'EOF'\n{\"operation\":\"count_documents\",\"collection\":\"articles\",\"filter\":{}}\nEOF\ncat > mq3.json <<'EOF'\n{\"operation\":\"find\",\"collection\":\"articles\",\"filter\":{\"article_id\":{\"$in\":[29998,29999,30000,30001,59998,59999,60000,60001,89998,89999,90000,90001,119998,119999,120000]}},\"projection\":{\"article_id\":1,\"title\":1,\"_id\":0},\"sort\":[[\"article_id\",1]]}\nEOF\nP=/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/bookreview/.venv/bin/python\nT=/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/tools/tool.py\n$P $T query-db articles_database --mongo-file mq2.json\n$P $T query-db articles_database --mongo-file mq3.json"
}
```

审计待核对 agnews/query2 / natural：
```json
{
  "kind": "non_adapter_bash_review",
  "index": 11,
  "command": "P=/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/bookreview/.venv/bin/python\nT=/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/tools/tool.py\n$P $T query-db metadata_database --sql \"SELECT DISTINCT region FROM article_metadata\""
}
```

审计待核对 agnews/query2 / natural：
```json
{
  "kind": "non_adapter_bash_review",
  "index": 13,
  "command": "P=/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/bookreview/.venv/bin/python\nT=/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/tools/tool.py\n$P $T query-db metadata_database --sql \"SELECT article_id FROM article_metadata WHERE author_id = 218 ORDER BY article_id\""
}
```

审计待核对 agnews/query2 / natural：
```json
{
  "kind": "non_adapter_bash_review",
  "index": 15,
  "command": "P=/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/bookreview/.venv/bin/python\nT=/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/tools/tool.py\nIDS=$(python3 -c \"import json;print(json.dumps([r['article_id'] for r in json.load(open('/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/natural/agnews/query2/full-01/results/ad24b5ee8713478a912aad3e601f250f.json'))]))\")\nprintf '{\"operation\":\"find\",\"collection\":\"articles\",\"filter\":{\"article_id\":{\"$in\":%s}},\"projection\":{\"article_id\":1,\"title\":1,\"description\":1,\"_id\":0},\"sort\":[[\"article_id\",1]]}' \"$IDS\" > mq4.json\n$P $T query-db articles_database --mongo-file mq4.json"
}
```

审计待核对 agnews/query2 / natural：
```json
{
  "kind": "non_adapter_bash_review",
  "index": 17,
  "command": "python3 -c \"\nimport json\nrows=json.load(open('/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/natural/agnews/query2/full-01/results/a65f87c00fe640a4a0b83eeee60e8edb.json'))\nfor r in rows:\n    print(r['article_id'],'|',r['title'],'|',r['description'][:180].replace(chr(10),' '))\n    print('---')\n\" > articles_111.txt\nwc -l articles_111.txt"
}
```
- agnews/query3 / natural：Ground truth numeric value '336.6363636363636' (tol=0.01) not found in LLM output: The average number of business articles published per year in Europe from 2010 to 2020 (inclusive) is approximately 41.82 articles per year.

Method:
- "Business articles" were identified from the articles collection (MongoDB) as articles whose title or description contains the word "business" (case-insensitive), yielding 4,018 articles.
- From article_metadata (SQLite), articles with region = 'Europe' and publication_date between 2010-01-01 and 2020-12-31 were selected.
- Joining the two on article_id gave yearly counts:
  2010: 45, 2011: 44, 2012: 35, 2013: 46, 2014: 40, 2015: 34, 2016: 44, 2017: 41, 2018: 41, 2019: 46, 2020: 44
- Total = 460 business articles over 11 years; average = 460 / 11 ≈ 41.82 per year.
- 已核对 crmarenapro/query10 / natural / 消息 1：已核对：进入旧 pilot 根目录列目录；属于目录协议偏离。实际 SQL 与答案由 v2 绑定到本任务，无日志错位。 [代码](../runs/natural/crmarenapro/query10/full-01/audit/shell-message-1.sh)
- crmarenapro/query12 / natural：Found agent IDs ['005Wt000003NJgAIAW'], but expected '005Wt000003NDEBIA4'
- 已核对 crmarenapro/query12 / natural / 消息 1：已核对：只在旧 pilot 根目录执行 ls/pwd，未读其他任务内容；记录目录协议偏离。 [代码](../runs/natural/crmarenapro/query12/full-01/audit/shell-message-1.sh)
- crmarenapro/query13 / natural：Found agent IDs ['005Wt000003NHw5IAG'], but expected '005Wt000003NIXCIA4'

审计待核对 crmarenapro/query13 / natural：
```json
{
  "kind": "non_adapter_bash_review",
  "index": 1,
  "command": "cd /data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/bookreview && ls 2>/dev/null | head; pwd"
}
```
- 已核对 crmarenapro/query2 / natural / 消息 4：人工逐段核对：仅以 json/re 读取本运行已有 results 文件、筛选和打印文本；未直接访问数据库或外部答案。属于 Python 工具协议偏离。 [代码](../runs/natural/crmarenapro/query2/full-01/audit/direct-python-message-4.py)
- 已核对 crmarenapro/query2 / natural / 消息 6：人工逐段核对：仅以 json/re 读取本运行已有 results 文件、筛选和打印文本；未直接访问数据库或外部答案。属于 Python 工具协议偏离。 [代码](../runs/natural/crmarenapro/query2/full-01/audit/direct-python-message-6.py)

审计待核对 crmarenapro/query7 / natural：
```json
{
  "kind": "non_adapter_bash_review",
  "index": 22,
  "command": "/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/bookreview/.venv/bin/python -c \"\nimport json\nrows = json.load(open('/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/natural/crmarenapro/query7/full-01/results/ca182fc6c1c348d0aa44b2b8835ef933.json'))\nfor r in rows:\n    t = r['title'].strip()\n    print(r['id'], '|', t)\n\" | grep -iE \"policy|polic|return|refund|warrant|discount|pricing|offer|support|upgrade|escalat|SLA|terms|guideline\" "
}
```

审计待核对 crmarenapro/query7 / natural：
```json
{
  "kind": "non_adapter_bash_review",
  "index": 34,
  "command": "/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/bookreview/.venv/bin/python -c \"\nimport json\nrows = json.load(open('/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/natural/crmarenapro/query7/full-01/results/ca182fc6c1c348d0aa44b2b8835ef933.json'))\nfor r in rows:\n    print(r['id'], '|', r['title'].strip())\n\""
}
```
- googlelocal/query2 / natural：No score found after name: Elite Massage

审计待核对 googlelocal/query4 / natural：
```json
{
  "kind": "non_adapter_bash_review",
  "index": 1,
  "command": "cd /data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/bookreview 2>/dev/null; pwd; ls"
}
```

审计待核对 googlelocal/query4 / natural：
```json
{
  "kind": "non_adapter_bash_review",
  "index": 7,
  "command": "PY=/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/bookreview/.venv/bin/python; T=/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/tools/tool.py; $PY $T query-db review_database --sql-file runs_tmp/schema.sql; $PY $T query-db review_database --sql-file runs_tmp/sample.sql"
}
```
- music_brainz_20k/query1 / natural：Ground truth '1059.46' not found in LLM output: Apple Music made **$601.44 USD** in revenue from Beyoncé's song "Get Me Bodied" in Canada.

Method:
- Found 3 matching track records in tracks_database (track_id 4233, 12954, 15158 — all "Get Me Bodied" by Beyoncé, from different sources).
- Summed sales in sales_database for those track IDs where country = 'Canada' and store = 'Apple Music'.
- Result: 564 units sold, total revenue = $601.44 USD.

- music_brainz_20k/query3 / natural：No fuzzy match (Zo gaat het leven aan je voor) found in The song that generated the highest total revenue in USD across all stores and countries is:

**"Emerge (Dexter remix)" by Fischerspooner — total revenue: $6,665.02**

How this was determined:
1. Aggregated all sales in the sales_database by track_id (SUM of revenue_usd over all stores and countries).
2. Joined with the tracks_database, which contains duplicate records of the same song from 5 different sources (with source-specific formatting: "Artist - Title" in source 2, "NNN-Title" track-number prefixes in source 4, "Title - Album" / "Title (Album)" suffixes in sources 3 and 1, plus occasional typos).
3. After canonicalizing titles/artists and clustering duplicate records of the same song, "Emerge (Dexter remix)" by Fischerspooner appears as 5 track records (track_ids 4895, 6988, 10166, 10606, 17167), one from each source, with revenues of $1,610.46 + $1,762.80 + $850.61 + $672.12 + $1,769.03 = $6,665.02.

Verification: the runner-up songs are "Pret à tout (feat. K-Rlos)" by La Swija ($6,097.66) and "Diamonds in the Mine" by Leonard Cohen ($6,017.10). The cluster for the winning song was verified to contain exactly the 5 source duplicates (the similarly named "Emerge (Dave Clarke remix)" is a different remix and was correctly excluded). A cross-artist fuzzy check confirmed no additional duplicates would change the top ranking.

Note: if duplicates are not consolidated, the top single track record is "Systemisch bled" by Stüngö ($2,522.82), but at the song level (deduplicating across sources), "Emerge (Dexter remix)" by Fischerspooner is the clear #1.. Best score: 0.01
- stockindex/query2 / natural：Target 'IXIC' not stated as primary answer (not in first 200 chars).
- stockmarket/query3 / natural：No number found near name: Apex Global Brands Inc
- yelp/query2 / natural：No occurrence of 3.7 near PA/Pennsylvania.

审计待核对 yelp/query4 / natural：
```json
{
  "kind": "non_adapter_bash_review",
  "index": 1,
  "command": "cd /data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/bookreview 2>/dev/null || pwd; ls"
}
```

审计待核对 yelp/query4 / natural：
```json
{
  "kind": "non_adapter_bash_review",
  "index": 25,
  "command": "/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/bookreview/.venv/bin/python -c \"\nimport json\nd = json.load(open('/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/natural/yelp/query4/full-01/results/26e9529c623b4c1f95aafba509b44831.json'))\nprint(d['stdout'])\n\" > /tmp/parse_out.txt; wc -l /tmp/parse_out.txt; head -80 /tmp/parse_out.txt"
}
```

审计待核对 yelp/query4 / natural：
```json
{
  "kind": "non_adapter_bash_review",
  "index": 27,
  "command": "tail -30 /tmp/parse_out.txt"
}
```

审计待核对 yelp/query4 / natural：
```json
{
  "kind": "non_adapter_bash_review",
  "index": 33,
  "command": "/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/bookreview/.venv/bin/python -c \"\nimport json\nd = json.load(open('/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/natural/yelp/query4/full-01/results/378c56c0e1f6429983b361f60c98f049.json'))\nprint(d['stdout'])\n\""
}
```

## 扩展工具参数检查

检查 108 次已结束运行的 1852 条 assistant 消息及 134 个 Python 脚本。匹配路径/库名只是待核对线索，不是泄漏证明。

[全部线索](provenance-review.json) · [人工核对记录](provenance-decisions.json)
- crmarenapro/query10 / natural / 消息 1：人工核对：在旧 pilot 根目录及其新建 work 子目录列目录、写 SQL/答案并调用 fullbench 工具；未见读取其他任务答案。v2 环境绑定将实际 SQL/结果/答案保存在正确任务，故保留并标注目录协议偏离。
- crmarenapro/query10 / natural / 消息 3：人工核对：在旧 pilot 根目录及其新建 work 子目录列目录、写 SQL/答案并调用 fullbench 工具；未见读取其他任务答案。v2 环境绑定将实际 SQL/结果/答案保存在正确任务，故保留并标注目录协议偏离。
- crmarenapro/query10 / natural / 消息 5：人工核对：在旧 pilot 根目录及其新建 work 子目录列目录、写 SQL/答案并调用 fullbench 工具；未见读取其他任务答案。v2 环境绑定将实际 SQL/结果/答案保存在正确任务，故保留并标注目录协议偏离。
- crmarenapro/query10 / natural / 消息 7：人工核对：在旧 pilot 根目录及其新建 work 子目录列目录、写 SQL/答案并调用 fullbench 工具；未见读取其他任务答案。v2 环境绑定将实际 SQL/结果/答案保存在正确任务，故保留并标注目录协议偏离。
- crmarenapro/query10 / natural / 消息 7：人工核对：在旧 pilot 根目录及其新建 work 子目录列目录、写 SQL/答案并调用 fullbench 工具；未见读取其他任务答案。v2 环境绑定将实际 SQL/结果/答案保存在正确任务，故保留并标注目录协议偏离。
- crmarenapro/query10 / natural / 消息 10：人工核对：在旧 pilot 根目录及其新建 work 子目录列目录、写 SQL/答案并调用 fullbench 工具；未见读取其他任务答案。v2 环境绑定将实际 SQL/结果/答案保存在正确任务，故保留并标注目录协议偏离。
- crmarenapro/query10 / natural / 消息 12：人工核对：在旧 pilot 根目录及其新建 work 子目录列目录、写 SQL/答案并调用 fullbench 工具；未见读取其他任务答案。v2 环境绑定将实际 SQL/结果/答案保存在正确任务，故保留并标注目录协议偏离。
- crmarenapro/query10 / natural / 消息 14：人工核对：在旧 pilot 根目录及其新建 work 子目录列目录、写 SQL/答案并调用 fullbench 工具；未见读取其他任务答案。v2 环境绑定将实际 SQL/结果/答案保存在正确任务，故保留并标注目录协议偏离。
- crmarenapro/query10 / natural / 消息 16：人工核对：在旧 pilot 根目录及其新建 work 子目录列目录、写 SQL/答案并调用 fullbench 工具；未见读取其他任务答案。v2 环境绑定将实际 SQL/结果/答案保存在正确任务，故保留并标注目录协议偏离。
- crmarenapro/query10 / natural / 消息 18：人工核对：在旧 pilot 根目录及其新建 work 子目录列目录、写 SQL/答案并调用 fullbench 工具；未见读取其他任务答案。v2 环境绑定将实际 SQL/结果/答案保存在正确任务，故保留并标注目录协议偏离。
- crmarenapro/query10 / natural / 消息 18：人工核对：在旧 pilot 根目录及其新建 work 子目录列目录、写 SQL/答案并调用 fullbench 工具；未见读取其他任务答案。v2 环境绑定将实际 SQL/结果/答案保存在正确任务，故保留并标注目录协议偏离。
- crmarenapro/query10 / natural / 消息 21：人工核对：在旧 pilot 根目录及其新建 work 子目录列目录、写 SQL/答案并调用 fullbench 工具；未见读取其他任务答案。v2 环境绑定将实际 SQL/结果/答案保存在正确任务，故保留并标注目录协议偏离。
- crmarenapro/query10 / natural / 消息 23：人工核对：在旧 pilot 根目录及其新建 work 子目录列目录、写 SQL/答案并调用 fullbench 工具；未见读取其他任务答案。v2 环境绑定将实际 SQL/结果/答案保存在正确任务，故保留并标注目录协议偏离。
- crmarenapro/query12 / natural / 消息 1：人工核对：只进入旧 pilot 根目录执行 ls/pwd，未读其他任务内容；保留目录协议偏离。
- crmarenapro/query13 / natural / 消息 1：人工核对该命令仅进入旧 pilot 目录执行 ls/head 和 pwd，未读取文件内容；保留并标注目录协议偏离。此结论仅针对该命令。
- googlelocal/query4 / natural / 消息 1：人工核对：在旧 pilot 根目录及其新建 work 子目录列目录、写 SQL/答案并调用 fullbench 工具；未见读取其他任务答案。v2 环境绑定将实际 SQL/结果/答案保存在正确任务，故保留并标注目录协议偏离。
- yelp/query4 / natural / 消息 1：待人工核对：path_outside_assigned_run_review

## 记录故障：natural-crmarenapro-query7

异常尝试已排除主统计并归档；恢复运行已结束，主报告引用恢复轨迹。
[事件记录](incidents/natural-crmarenapro-query7.json)

v2 适配器将记录目录及任务身份绑定到启动环境，防止改变当前目录后日志错位；早期 v1 运行保留，版本差异需与结果一同解释。
