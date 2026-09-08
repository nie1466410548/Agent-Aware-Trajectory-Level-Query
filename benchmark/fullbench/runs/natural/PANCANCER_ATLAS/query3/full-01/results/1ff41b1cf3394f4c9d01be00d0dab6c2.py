import json, math

clin_path = "/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/natural/PANCANCER_ATLAS/query3/full-01/results/1f0cd54a021a45e3b2969c67fce770c4.json"
mut_path = "/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/natural/PANCANCER_ATLAS/query3/full-01/results/fcaf927c69a242c5aca8c3894b75c3a9.json"

clin = json.load(open(clin_path))
mut = json.load(open(mut_path))
cdh1_mut = {r["ParticipantBarcode"] for r in mut}
print("Distinct CDH1 PASS-mutated participants (all cancers):", len(cdh1_mut))

# Female BRCA patients with known histological type
patients = [r for r in clin if r["histological_type"] is not None and r["histological_type"].strip() != ""]
print("Female BRCA patients with known histological type:", len(patients))

# Build contingency counts
from collections import defaultdict
counts = defaultdict(lambda: [0, 0])  # histo -> [mutated, not mutated]
for r in patients:
    h = r["histological_type"]
    if r["barcode"] in cdh1_mut:
        counts[h][0] += 1
    else:
        counts[h][1] += 1

print("\nAll categories (female BRCA, known histology):")
for h, (m, nm) in sorted(counts.items(), key=lambda kv: -(kv[1][0] + kv[1][1])):
    print(f"  {h}: mutated={m}, not_mutated={nm}, total={m+nm}")

# Exclude categories with marginal totals <= 10
kept = {h: v for h, v in counts.items() if v[0] + v[1] > 10}
print("\nKept categories (marginal total > 10):")
for h, (m, nm) in sorted(kept.items(), key=lambda kv: -(kv[1][0] + kv[1][1])):
    print(f"  {h}: mutated={m}, not_mutated={nm}, total={m+nm}")

# Chi-square test of independence
rows = list(kept.values())
R = len(rows); C = 2
row_tot = [m + nm for m, nm in rows]
col_tot = [sum(r[0] for r in rows), sum(r[1] for r in rows)]
N = sum(row_tot)
chi2 = 0.0
for i, (m, nm) in enumerate(rows):
    for j, o in enumerate((m, nm)):
        e = row_tot[i] * col_tot[j] / N
        chi2 += (o - e) ** 2 / e
dof = (R - 1) * (C - 1)

# p-value via regularized upper incomplete gamma Q(dof/2, chi2/2)
def gammaincc(a, x):
    if x <= 0:
        return 1.0
    if x < a + 1:
        # series for P, then Q = 1 - P
        term = 1.0 / a
        s = term
        ap = a
        for _ in range(1000):
            ap += 1
            term *= x / ap
            s += term
            if abs(term) < abs(s) * 1e-15:
                break
        P = s * math.exp(-x + a * math.log(x) - math.lgamma(a))
        return 1.0 - P
    else:
        # continued fraction for Q
        tiny = 1e-300
        b = x + 1 - a
        c = 1.0 / tiny
        d = 1.0 / b
        h = d
        for i in range(1, 1000):
            an = -i * (i - a)
            b += 2
            d = an * d + b
            if abs(d) < tiny: d = tiny
            c = b + an / c
            if abs(c) < tiny: c = tiny
            d = 1.0 / d
            delta = d * c
            h *= delta
            if abs(delta - 1.0) < 1e-15:
                break
        return h * math.exp(-x + a * math.log(x) - math.lgamma(a))

p = gammaincc(dof / 2.0, chi2 / 2.0)

print(f"\nN patients in test: {N}")
print(f"Chi-square statistic: {chi2:.4f}")
print(f"Degrees of freedom: {dof}")
print(f"p-value: {p:.3e}")
