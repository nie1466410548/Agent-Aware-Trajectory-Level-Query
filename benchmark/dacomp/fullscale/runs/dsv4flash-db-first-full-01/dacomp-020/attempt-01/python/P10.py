import numpy as np, pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

df = pd.read_csv('work/sheet1_full.csv')

def ols_simple(y, X):
    X = np.asarray(X, dtype=float)
    y = np.asarray(y, dtype=float)
    XtX_inv = np.linalg.pinv(X.T @ X)
    beta = XtX_inv @ X.T @ y
    yhat = X @ beta
    rss = (y-yhat) @ (y-yhat)
    r2 = 1 - rss/np.sum((y-y.mean())**2)
    return dict(beta=beta, r2=r2, yhat=yhat)

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
base_mat = np.column_stack([np.ones(len(df)), base])
m_base = ols_simple(y, base_mat)
names_base = ['Intercept'] + list(base.columns)
beta_base = dict(zip(names_base, m_base['beta']))
means = {c: np.mean(base[c]) for c in base.columns}

# Single interaction models
def fit_int(var, dval):
    X = base.copy()
    X[f'MHx{var}'] = df['Mental health score'] * dval
    Xmat = np.column_stack([np.ones(len(df)), X])
    m = ols_simple(y, Xmat)
    names = ['Intercept'] + list(X.columns)
    return dict(zip(names, m['beta']))

beta_att = fit_int('Attendance rate', df['Attendance rate'])
beta_sm = fit_int('Social media usage time', df['Social media usage time'])

mh_grid = np.linspace(1, 10, 50)
fig, axes = plt.subplots(1, 2, figsize=(14, 5.5))

# Panel A: attendance interaction (SM held at mean)
att_levels = {'Low (60%)': 60, 'Average (83%)': 83, 'High (100%)': 100}
ax = axes[0]
for lab, att in att_levels.items():
    pred = (beta_att['Intercept'] 
            + beta_att['Mental health score']*mh_grid 
            + beta_att['Attendance rate']*att 
            + beta_att['MHxAttendance']*mh_grid*att)
    for c in means:
        if c in ['Mental health score', 'Attendance rate']:
            continue
        pred += beta_att[c]*means[c]
    ax.plot(mh_grid, pred, lw=2.2, label=lab)
ax.set_xlabel('Mental health score', fontsize=12)
ax.set_ylabel('Predicted Exam score (other covariates at mean)', fontsize=11)
ax.set_title('A: Mental health × Attendance rate', fontsize=12, fontweight='bold')
ax.legend(title='Attendance', fontsize=9)
ax.set_ylim(45, 100)

# Panel B: social media interaction (attendance held at mean)
sm_levels = {'Low (0h)': 0, 'Average (2.6h)': 2.6, 'High (5h)': 5, 'Very high (8h)': 8}
ax = axes[1]
for lab, sm in sm_levels.items():
    pred = (beta_sm['Intercept'] 
            + beta_sm['Mental health score']*mh_grid 
            + beta_sm['Social media usage time']*sm 
            + beta_sm['MHxSocialMedia']*mh_grid*sm)
    for c in means:
        if c in ['Mental health score', 'Social media usage time']:
            continue
        pred += beta_sm[c]*means[c]
    ax.plot(mh_grid, pred, lw=2.2, label=lab)
ax.set_xlabel('Mental health score', fontsize=12)
ax.set_ylabel('Predicted Exam score (other covariates at mean)', fontsize=11)
ax.set_title('B: Mental health × Social media usage time', fontsize=12, fontweight='bold')
ax.legend(title='Social media', fontsize=9)
ax.set_ylim(45, 100)

plt.tight_layout()
plt.savefig('work/fig2_interactions.png', dpi=150)
plt.close()
print("Figure 2 saved (corrected)")

# Marginal MH slopes at moderator levels
print("\nMH marginal effect (dExam/dMH, per 1 MH point) at moderator levels:")
for lab, att in att_levels.items():
    s = beta_att['Mental health score'] + beta_att['MHxAttendance']*att
    print(f"  Attendance {lab}: slope = {s:.3f}")
print()
for lab, sm in sm_levels.items():
    s = beta_sm['Mental health score'] + beta_sm['MHxSocialMedia']*sm
    print(f"  SM {lab}: slope = {s:.3f}")
print()
# Difference in MH effect between high and low attendance
att_diff = (beta_att['MHxAttendance']*(100-60))
print(f"MH effect difference between 60% and 100% attendance: {att_diff:.3f} exam points per MH unit")
sm_diff = (beta_sm['MHxSocialMedia']*(8-0))
print(f"MH effect difference between 0h and 8h social media: {sm_diff:.3f} exam points per MH unit")
