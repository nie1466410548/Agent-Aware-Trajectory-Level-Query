import pandas as pd
import numpy as np
import re
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

df_kw = pd.read_csv('/work/df_kw.csv')
df_kw['is_problem'] = df_kw['is_problem'].astype(int)

# Fig 5: Word lift chart
words_vocab = ["analytics","best","business","buy","cheap","cloud","compare","consulting","course",
"delivery","digital","discount","enterprise","free","management","marketing","mobile","new","online",
"premium","price","professional","quality","review","sale","service","software","solution","support",
"top","training","warranty"]
def tokens(text):
    return set(re.findall(r'[a-z]+', str(text).lower()))
df_kw['tok'] = df_kw['keyword_text'].apply(tokens)

rows_list = []
for grp in [0, 1]:
    sub = df_kw[df_kw['is_problem'] == grp]
    tot = sub['clicks'].sum()
    for w in words_vocab:
        wc = sub[sub['tok'].apply(lambda t: w in t)]['clicks'].sum()
        rows_list.append({'group': grp, 'word': w, 'share': 100.0*wc/tot})
wd = pd.DataFrame(rows_list)
wide = wd.pivot(index='word', columns='group', values='share').reset_index()
wide.columns = ['word','non_prob','prob']
wide['lift'] = wide['prob'] / wide['non_prob']
wide = wide.sort_values('lift')

fig, ax = plt.subplots(figsize=(7,9))
colors = np.where(wide['lift']>=1.1, '#C44E52', np.where(wide['lift']<=0.9, '#4C72B0', '#9AA7B1'))
ax.barh(wide['word'], wide['lift'], color=colors)
ax.axvline(1.0, color='grey', ls='--', lw=1)
ax.set_xlabel('Click-share lift (problem / normal)')
ax.set_title('Keyword word click-share lift in problem vs normal ad groups\n(red=over-indexed in problem groups)')
plt.tight_layout(); plt.savefig('/work/fig5_words.png'); plt.close()

# Fig 6: Economics comparison
df_all = pd.read_csv('/work/df_all.csv')
df_all['is_problem'] = df_all['is_problem'].astype(int)
result = db.query("SELECT ad_group_id, SUM(conversions_value) AS conv_value FROM google_ads__ad_group_report GROUP BY ad_group_id")
e = result['executions'][0]; rows = db.rows(result)
df_extra = pd.DataFrame(rows, columns=e['columns'])
df_all = df_all.merge(df_extra, on='ad_group_id', how='left')
df_all['cpa'] = df_all['spend'] / df_all['conversions'].replace(0, np.nan)
df_all['roas'] = df_all['conv_value'] / df_all['spend'].replace(0, np.nan)
df_all['Group'] = np.where(df_all['is_problem']==1, 'Problem', 'Normal')

fig, axes = plt.subplots(1, 2, figsize=(9,4))
sns.boxplot(data=df_all, x='Group', y='cpa', ax=axes[0], hue='Group', legend=False, palette=['#4C72B0','#C44E52'])
axes[0].set_ylim(0, 250); axes[0].set_title('Cost per Acquisition (spend/conversion)'); axes[0].set_ylabel('CPA')
sns.boxplot(data=df_all, x='Group', y='roas', ax=axes[1], hue='Group', legend=False, palette=['#4C72B0','#C44E52'])
axes[1].set_ylim(0, 8); axes[1].set_title('Return on Ad Spend (conv value/spend)'); axes[1].set_ylabel('ROAS')
plt.tight_layout(); plt.savefig('/work/fig6_econ.png'); plt.close()
print("Fig5, Fig6 saved.")