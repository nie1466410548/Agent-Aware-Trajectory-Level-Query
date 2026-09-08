import json, re
rows = json.load(open("/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/fad/crmarenapro/query2/full-01/results/924d3b9c6f46427da202e73452570e67.json"))
targets = ["EcoPCB Creator","PulseSim Pro","CircuitSync Pro"]
for r in rows:
    if r["id"] in ("#ka0Wt000000EnwvIAC","ka0Wt000000EnvJIAS","ka0Wt000000Ens5IAC","ka0Wt000000Eq0MIAS","#ka0Wt000000EpSUIA0"):
        txt = r.get("faq_answer__c") or ""
        print("="*70)
        print(r["id"], "|", r["title"], "| len:", len(txt))
        for t in targets:
            if t.lower() in txt.lower():
                for m in re.finditer(re.escape(t), txt, re.I):
                    s=max(0,m.start()-150); e=min(len(txt),m.end()+200)
                    print("  ...", txt[s:e].replace("\n"," "), "...")
