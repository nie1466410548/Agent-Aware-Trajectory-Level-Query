import json
projects = json.load(open("projects.json"))
for p in projects:
    if p["project"] in ("lrembacz/vue-dragndrop.", "rrdelaney/reason", "wizards-lab/routing"):
        print(p["project"], "forks=", p["forks"], "|", p["text"][:130])
