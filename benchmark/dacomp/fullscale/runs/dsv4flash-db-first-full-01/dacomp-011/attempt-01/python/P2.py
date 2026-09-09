import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

rows = db.query("SELECT * FROM sheet1")
df = db.frame(rows)

# Ensure column name is right
col = "Parents' education level"
print(df[col].value_counts(dropna=False))
print(df[col].isnull().sum(), "nulls")

# ============ Analysis 1: Parents' education level vs exam score ============
# Kruskal-Wallis test across parent edu groups (excluding null)
groups = [df.loc[df[col]==g, 'Exam score'].values for g in ['High School','Bachelor','Master']]
kw = stats.kruskal(*groups)
print(f"\nKruskal-Wallis across parent edu groups (HS, Bachelor, Master): H={kw.statistic:.3f}, p={kw.pvalue:.4f}")

# ANOVA
f_stat, p_val = stats.f_oneway(*groups)
print(f"ANOVA: F={f_stat:.3f}, p={p_val:.4f}")

# Pairwise Mann-Whitney
from itertools import combinations
edu_levels = ['High School','Bachelor','Master']
for a,b in combinations(edu_levels, 2):
    u, p = stats.mannwhitneyu(df.loc[df[col]==a,'Exam score'], df.loc[df[col]==b,'Exam score'])
    print(f"MWU {a} vs {b}: p={p:.4f}")

# Effect size (eta squared)
all_scores = np.concatenate(groups)
grand_mean = all_scores.mean()
ss_between = sum(len(g)*(np.mean(g)-grand_mean)**2 for g in groups)
ss_total = sum(((g-grand_mean)**2).sum() for g in groups)
eta2 = ss_between/ss_total
print(f"Eta-squared for parent education: {eta2:.4f}")

# Mean difference between Bachelor and Master
b_mean = df.loc[df[col]=='Bachelor','Exam score'].mean()
m_mean = df.loc[df[col]=='Master','Exam score'].mean()
hs_mean = df.loc[df[col]=='High School','Exam score'].mean()
print(f"Mean exam: HS={hs_mean:.2f}, Bachelor={b_mean:.2f}, Master={m_mean:.2f}")
print(f"Diff Bachelor vs Master: {b_mean-m_mean:.2f} points")