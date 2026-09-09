import numpy as np, pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

df = pd.read_csv('work/sheet1_full.csv')

def ols_simple(y, X):
    Xmat = np.asarray(X, dtype=float)
    yv = np.asarray(y, dtype=float)
    n, k = Xmat.shape
    XtX_inv = np.linalg.pinv(Xmat.T @ Xmat)
    beta = XtX_inv @ Xmat.T @ yv
    return beta

def base_design(df):
    d = pd.DataFrame(index=df.index)
    d['Mental health score'] = df['Mental health score']
    d['Daily study time'] = df['Daily study time']
    d['Social media usage time'] = df['Social media usage time']
    d['Attendance rate'] = df['Attendance rate']
    d['Sleep duration'] = df['Sleep duration']
    d['Exercise frequency'] = df['Exercise frequency']
    d['Diet_Good'] = (df['Diet quality']=='Good').astype(int)
    d['Diet_Poor'] = (df['Diet quality']=='Poor').astype(int)
    d['Part_time_Yes'] = (df['Part-time job']=='Yes').astype(int)
    d['Internet_Good'] = (df['Internet quality']=='Good').astype(int)
    d['Internet_Poor'] = (df['Internet quality']=='Poor').astype(int)
    d['Parent_Bachelor'] = (df["Parents' education level"]=='Bachelor').astype(int)
    d['Parent_Master'] = (df["Parents' education level"]=='Master').astype(int)
    d['Parent_Missing'] = (df["Parents' education level"].isnull()).astype(int)
    return d

base = base_design(df)
y = df['Exam score'].values
base_cols = list(base.columns)
base_mat = np.column_stack([np.ones(len(df)), base])
m_base = ols_simple(y, base_mat)
beta_base = dict(zip(['Intercept']+base_cols, m_base))
means = {c: np.mean(base[c]) for c in base_cols}

# Fit interaction model for Attendance
X_att = base.copy()
X_att['MHxAtt'] = df['Mental health score'] * df['Attendance rate']
X_att_mat = np.column_stack([np.ones(len(df)), X_att])
beta_att = dict(zip(['Intercept']+list(X_att.columns), ols_simple(y, X_att_mat)))

# Fit interaction model for Social media
X_sm = base.copy()
X_sm['MHxSM'] = df['Mental health score'] * df['Social media usage time']
X_sm_mat = np.column_stack([np.ones(len(df)), X_sm])
beta_sm = dict(zip(['Intercept']+list(X_sm.columns), ols_simple(y, X_sm_mat)))

print("Betas for att model:", {k: round(v,4) for k,v in beta_att.items()})
print("Betas for sm model:", {k: round(v,4) for k,v in beta_sm.items()})

mh_grid = np.linspace(1, 10, 50)
fig, axes = plt.subplots(1, 2, figsize=(14, 5.5))

# Panel A: attendance interaction
att_levels = {'Low (60%)': 60, 'Average (83%)': 83, 'High (100%)': 100}
ax = axes[0]
for lab, att in att_levels.items():
    pred = (beta_att['Intercept'] 
            + beta_att['Mental health score']*mh_grid 
            + beta_att['Attendance rate']*att 
            + beta_att['MHxAtt']*mh_grid*att)
    for c in means:
        if c in ['Mental health score', 'Attendance rate']:
            continue
        pred += beta_att[c]*means[c]
    ax.plot(mh_grid, pred, lw=2.2, label=lab)
ax.set_xlabel('Mental health score', fontsize=12)
ax.set_ylabel('Predicted Exam score', fontsize=11)
ax.set_title('A: Mental health × Attendance rate', fontsize=12, fontweight='bold')
ax.legend(title='Attendance', fontsize=9)
ax.set_ylim(45, 100)

# Panel B: social media interaction
sm_levels = {'Low (0h)': 0, 'Average (2.6h)': 2.6, 'High (5h)': 5, 'Very high (8h)': 8}
ax = axes[1]
for lab, sm in sm_levels.items():
    pred = (beta_sm['Intercept'] 
            + beta_sm['Mental health score']*mh_grid 
            + beta_sm['Social media usage time']*sm 
            + beta_sm['MHxSM']*mh_grid*sm)
    for c in means:
        if c in ['Mental health score', 'Social media usage time']:
            continue
        pred += beta_sm[c]*means[c]
    ax.plot(mh_grid, pred, lw=2.2, label=lab)
ax.set_xlabel('Mental health score', fontsize=12)
ax.set_ylabel('Predicted Exam score', fontsize=11)
ax.set_title('B: Mental health × Social media usage time', fontsize=12, fontweight='bold')
ax.legend(title='Social media', fontsize=9)
ax.set_ylim(45, 100)

plt.tight_layout()
plt.savefig('work/fig2_interactions.png', dpi=150)
plt.close()
print("Figure 2 saved")

# Marginal MH slopes
print("\nMH marginal effect (dExam/dMH) at moderator levels:")
for lab, att in att_levels.items():
    s = beta_att['Mental health score'] + beta_att['MHxAtt']*att
    print(f"  Attendance {lab}: slope = {s:.3f}")
print()
for lab, sm in sm_levels.items():
    s = beta_sm['Mental health score'] + beta_sm['MHxSM']*sm
    print(f"  SM {lab}: slope = {s:.3f}")
print()

# Quantify the interaction effect sizes
att_diff = beta_att['MHxAtt'] * (100 - 60)
print(f"MH effect difference: 60% vs 100% attendance = {att_diff:.3f} exam points per MH unit")
sm_diff = beta_sm['MHxSM'] * (8 - 0)
print(f"MH effect difference: 0h vs 8h social media = {sm_diff:.3f} exam points per MH unit")