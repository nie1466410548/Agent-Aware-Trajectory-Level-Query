import pandas as pd
import numpy as np
import re

df_ag = pd.read_csv('/work/df_ag.csv')
df_kw = pd.read_csv('/work/df_kw.csv')

# ---- Keyword word frequency analysis (clicks-weighted) ----
words_vocab = ["analytics","best","business","buy","cheap","cloud","compare","consulting","course",
"delivery","digital","discount","enterprise","free","management","marketing","mobile","new","online",
"premium","price","professional","quality","review","sale","service","software","solution","support",
"top","training","warranty"]

# Intent categorization
transactional = {"buy","cheap","price","discount","sale","delivery","warranty","purchase","order"}
informational = {"best","compare","review","free","top","new","online","quality","professional","course","training","consulting"}
brandish = {"analytics","business","cloud","digital","enterprise","management","marketing","mobile","premium","service","software","solution","support"}

def tokens(text):
    return set(re.findall(r'[a-z]+', str(text).lower()))

df_kw['tok'] = df_kw['keyword_text'].apply(tokens)

# Clicks-weighted word share in problem vs non-problem keyword rows
rows_list = []
for grp in [0, 1]:
    sub = df_kw[df_kw['is_problem'] == grp]
    tot_clicks = sub['clicks'].sum()
    for w in words_vocab:
        wc = sub[sub['tok'].apply(lambda t: w in t)]['clicks'].sum()
        rows_list.append({'group': 'problem' if grp else 'non-problem', 'word': w, 'clicks_share_pct': 100.0*wc/tot_clicks})
word_df = pd.DataFrame(rows_list)
wide = word_df.pivot(index='word', columns='group', values='clicks_share_pct').reset_index()
wide['lift'] = wide['problem'] / wide['non-problem']
wide = wide.sort_values('lift', ascending=False)
print("=== Word clicks-share lift (problem / non-problem) ===")
print(wide.round(2).to_string())

# Intent composition
for grp, label in [(1,'problem'), (0,'non-problem')]:
    sub = df_kw[df_kw['is_problem']==grp]
    tot = sub['clicks'].sum()
    tr = sub[sub['tok'].apply(lambda t: len(t & transactional)>0)]['clicks'].sum()
    inf = sub[sub['tok'].apply(lambda t: len(t & informational)>0 and len(t & transactional)==0)]['clicks'].sum()
    print(f"{label}: transactional-word click share={100*tr/tot:.1f}%, informational-only click share={100*inf/tot:.1f}%")