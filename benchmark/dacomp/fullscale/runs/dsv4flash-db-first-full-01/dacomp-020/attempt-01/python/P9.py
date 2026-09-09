import numpy as np, pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy import stats

df = pd.read_csv('work/sheet1_full.csv')

# Recompute the full interaction model for Attendance and Social media
# Model: exam ~ all controls + MH:Att + MH:SM (jointly)
def ols_simple(y, X):
    X = np.asarray(X, dtype=float)
    y = np.asarray(y, dtype=float)
    n, k = X.shape
    XtX_inv = np.linalg.pinv(X.T @ X)
    beta = XtX_inv @ X.T @ y
    yhat = X @ beta
    rss = (y-yhat) @ (y-yhat)
    r2 = 1 - rss/np.sum((y-y.mean())**2)
    return dict(beta=beta, r2=r2, yhat=yhat)

# Base controls
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

# Interaction model with both significant interactions
X = base.copy()
X['MHxAttendance'] = df['Mental health score'] * df['Attendance rate']
X['MHxSocialMedia'] = df['Mental health score'] * df['Social media usage time']
Xmat = np.column_stack([np.ones(len(df)), X])
m = ols_simple(y, Xmat)
names = ['Intercept'] + list(X.columns)
beta = dict(zip(names, m['beta']))
print("Joint interaction model coefficients:")
for k_, v_ in beta.items():
    print(f"{k_:25s} {v_:.4f}")

# Predicted exam = f(MH) at different levels of attendance / social media, holding other covariates at means
base_cols = [c for c in X.columns if not c.startswith('MHx')]
means = {c: np.mean(X[c]) for c in base_cols}

att_levels = {'Low attendance (60%)': 60, 'Average (83%)': 83, 'High (100%)': 100}
sm_levels = {'Low SM (0h)': 0, 'Average (2.6h)': 2.6, 'High (5h)': 5, 'Very high (8h)': 8}

fig, axes = plt.subplots(1, 2, figsize=(14, 5.5))
mh_grid = np.linspace(1, 10, 50)

ax = axes[0]
for lab, att in att_levels.items():
    pred = beta['Intercept'] + beta['Mental health score']*mh_grid + beta['Attendance rate']*att + \
           beta['MHxAttendance']*mh_grid*att
    # add means of other controls
    for c in base_cols:
        if c in ['Mental health score', 'Attendance rate', 'Social media usage time']:
            continue
        pred += beta[c]*means[c]
    ax.plot(mh_grid, pred, lw=2.2, label=lab)
ax.set_xlabel('Mental health score', fontsize=12)
ax.set_ylabel('Predicted Exam score (other covariates at mean)', fontsize=11)
ax.set_title('A: MH × Attendance rate interaction', fontsize=12, fontweight='bold')
ax.legend(fontsize=9)
ax.set_ylim(40, 100)

ax = axes[1]
for lab, sm in sm_levels.items():
    pred = beta['Intercept'] + beta['Mental health score']*mh_grid + beta['Social media usage time']*sm + \
           beta['MHxSocialMedia']*mh_grid*sm
    for c in base_cols:
        if c in ['Mental health score', 'Attendance rate', 'Social media usage time']:
            continue
        pred += beta[c]*means[c]
    ax.plot(mh_grid, pred, lw=2.2, label=lab)
ax.set_xlabel('Mental health score', fontsize=12)
ax.set_ylabel('Predicted Exam score (other covariates at mean)', fontsize=11)
ax.set_title('B: MH × Social media usage time interaction', fontsize=12, fontweight='bold')
ax.legend(fontsize=9)
ax.set_ylim(40, 100)

plt.tight_layout()
plt.savefig('work/fig2_interactions.png', dpi=150)
plt.close()
print("Figure 2 saved")

# Quantify the MH slope at different moderator levels
print("\nMH marginal effect (dExam/dMH) at moderator levels:")
slope_att = beta['Mental health score'] + beta['MHxAttendance']*np.array([60, 83, 100])
for lab, att in att_levels.items():
    print(f"  {lab}: slope = {beta['Mental health score'] + beta['MHxAttendance']*att:.3f}")
print()
slope_sm = beta['Mental health score'] + beta['MHxSocialMedia']*np.array([0, 2.6, 5, 8])
for lab, sm in sm_levels.items():
    print(f"  {lab}: slope = {beta['Mental health score'] + beta['MHxSocialMedia']*sm:.3f}")
