"""
Module 5 lab, Hour 1 companion: a probability-of-default model three ways.

Data: UCI Machine Learning Repository dataset 350, "Default of Credit Card Clients".
Yeh, I. C., and Lien, C. H. (2009), Expert Systems with Applications 36(2), 2473-2480.
30,000 real credit-card customers of a bank in Taiwan, April to September 2005, with the
default outcome for the following month. The file is public. Nothing in it is simulated.

What it does, in order:
  1. Build six plain features a credit analyst would recognise.
  2. Split 70/30, stratified, seed 42. The models never see the 9,000 test rows.
  3. Fit a logistic regression, a depth-3 decision tree and a 200-tree XGBoost.
  4. Print the logistic coefficients on the raw scale, so a reader can recompute one PD by hand.
  5. Score all three on the test rows: AUC, Gini and KS.
  6. Walk one test customer through the logistic equation term by term.
"""
import os
import sys
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import roc_auc_score

LOCAL = os.path.expanduser("~/files/pd-model-workbook/default of credit card clients.xls")
URL = ("https://archive.ics.uci.edu/static/public/350/default+of+credit+card+clients.zip")
RS = 42

if os.path.exists(LOCAL):
    df = pd.read_excel(LOCAL, header=1)
else:
    import io, zipfile, urllib.request
    z = zipfile.ZipFile(io.BytesIO(urllib.request.urlopen(URL).read()))
    name = [n for n in z.namelist() if n.endswith(".xls")][0]
    df = pd.read_excel(io.BytesIO(z.read(name)), header=1)
df = df.rename(columns={"default payment next month": "DEFAULT"})

df["UTILIZATION"] = (df["BILL_AMT1"] / df["LIMIT_BAL"]).clip(0, 2).round(4)
df["PAY_RATIO"] = (df["PAY_AMT1"] / df["BILL_AMT1"].where(df["BILL_AMT1"] > 0, np.nan)).clip(0, 2)
df["PAY_RATIO"] = df["PAY_RATIO"].fillna(0).round(4)
FEATS = ["LIMIT_BAL", "AGE", "PAY_0", "PAY_2", "UTILIZATION", "PAY_RATIO"]
X, y = df[FEATS], df["DEFAULT"]
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.30, random_state=RS, stratify=y)

# logistic regression, fitted on standardised inputs then converted back to the raw scale
m, s = Xtr.mean(), Xtr.std(ddof=0)
lr = LogisticRegression(max_iter=2000, random_state=RS).fit((Xtr - m) / s, ytr)
coef = lr.coef_[0] / s.values
intercept = float(lr.intercept_[0] - (lr.coef_[0] * m.values / s.values).sum())
p_lr = 1 / (1 + np.exp(-(intercept + Xte.values @ coef)))
assert np.allclose(p_lr, lr.predict_proba((Xte - m) / s)[:, 1], atol=1e-9)

dt = DecisionTreeClassifier(max_depth=3, min_samples_leaf=200, random_state=RS).fit(Xtr, ytr)
p_dt = dt.predict_proba(Xte)[:, 1]
try:
    from xgboost import XGBClassifier
    xgb = XGBClassifier(n_estimators=200, max_depth=3, learning_rate=0.1, subsample=0.9,
                        colsample_bytree=0.9, eval_metric="logloss", random_state=RS).fit(Xtr, ytr)
    p_xgb = xgb.predict_proba(Xte)[:, 1]
except ImportError:
    p_xgb = None


def ks(yt, p):
    o = np.argsort(-p)
    yt = np.asarray(yt)[o]
    return float(np.max(np.cumsum(yt) / yt.sum() - np.cumsum(1 - yt) / (1 - yt).sum()))


print("=" * 66)
print("PD MODEL THREE WAYS | UCI dataset 350, 30,000 real credit-card customers")
print("=" * 66)
print(f"Rows: {len(df):,} total, {len(Xtr):,} train, {len(Xte):,} test. "
      f"Default rate {y.mean():.2%}.")
print()
print("--- Logistic regression, raw-scale coefficients ---")
print(f"{'intercept':12s} {intercept:+.6f}")
for f, c in zip(FEATS, coef):
    print(f"{f:12s} {c:+.6f}")
print()
print("--- Test-set ranking power (9,000 unseen customers) ---")
print(f"{'model':22s} {'AUC':>7s} {'Gini':>7s} {'KS':>7s}")
for name, p in [("Logistic regression", p_lr), ("Decision tree", p_dt), ("XGBoost", p_xgb)]:
    if p is None:
        print(f"{name:22s}   (xgboost not installed)")
        continue
    a = roc_auc_score(yte, p)
    print(f"{name:22s} {a:7.4f} {2*a-1:7.4f} {ks(yte, p):7.4f}")
print()

# one customer, term by term
i = 0
row = Xte.iloc[i]
print(f"--- One test customer, ID {df.loc[Xte.index[i], 'ID']}, term by term ---")
score = intercept
print(f"{'intercept':12s} {'':>12s} {'':>12s} {intercept:+10.4f}")
for f, c in zip(FEATS, coef):
    contrib = c * row[f]
    score += contrib
    print(f"{f:12s} {row[f]:12.4f} x {c:+12.6f} = {contrib:+10.4f}")
pd_hat = 1 / (1 + np.exp(-score))
print(f"{'score':12s} {'':>12s} {'':>12s} {score:+10.4f}")
print(f"PD = 1 / (1 + e^(-score)) = {pd_hat:.4f}   actually defaulted: {int(yte.iloc[i])}")
