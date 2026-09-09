# Prioritized Supervision of Imported & Joint-Venture (JV) Drugs

## Objective
Identify which imported and joint-venture (JV) drugs require prioritized supervision from three risk perspectives:
1. **Inventory backlog** (over-stocking, frozen/scrapped stock, slow-moving inventory)
2. **Supply interruption** (zero qualified stock, quarantine holds, stale inbound/outbound, frozen/scrapped status)
3. **Quality issue risk** (near-expiry, expired, damaged, contamination, temperature/humidity excursions, storage/transport sensitivity, GSP non-certification)

## Methodology
- Joined `basic_drug_information` ↔ `inventory_management` (1:1) on `Drug ID` for all **264 imported/JV drugs** (125 Imported, 139 JV).
- Computed per-drug sub-scores (0–100) in Python (parsing of mixed-format discrepancy rates, date-staleness conversions, log-normalization of skewed quantities, and weighted combination are not cleanly expressible in SQLite):
  - **Backlog score** = 30% log-normalized stock-to-threshold ratio + 20% frozen + 15% scrapped + 35% days-since-last-outbound (capped at 365 d).
  - **Supply-interruption score** = 25% zero qualified + 15% frozen + 10% scrapped + 10% quarantine-held + 15% severe alert + 5% alert + 20% days-since-last-inbound (capped at 365 d).
  - **Quality-risk score** = 35% log-normalized quality-issue volume (near-expiry + expired + damaged + returned + contamination + excursions) + 10% refrigerated storage + 5% cold-chain transport + 15% GSP non-certification + 15% discrepancy rate + 20% temp/humidity excursions.
- **Overall priority = 0.35×Backlog + 0.30×Supply + 0.35×Quality**.

## Key Findings

### 1. System-wide backlog & quality pressure affect BOTH origins
- **Inventory backlog is endemic**: average total stock is **2.12× (Imported)** and **2.32× (JV)** the `Max Inventory Threshold`; ~99% of drugs of both origins carry quarantine-hold quantities.
- **Large fractions of stock are unusable**: avg. near-expiry quantity ≈ 1,200 units and avg. expired quantity ≈ 574–645 units per drug; the **quality-issue rate (defective/expired units ÷ total stock) is ~24.6% (Imported) and ~25.1% (JV)**.
- **~64–68% of drugs** are in Frozen/Scrapped status (64.0% Imported, 67.6% JV); 61.6–63.3% carry Alert/Severe inventory alerts.
- **Cold-chain/refrigerated exposure**: 49.6% Imported / 48.2% JV require cold-chain transport; 34.4% / 32.4% require refrigerated storage, raising quality risk if handled improperly.
- **GSP non-certification**: 48.0% of Imported (60/125) and 42.4% of JV (59/139) drugs are *not* GSP-certified.
- **Abnormal price fluctuations** (potential supply stress signal): 54.0% of Imported (67/124) and 48.2% of JV (67/139) drugs.

### 2. Critical-tier drugs (overall priority ≥ 60): 21 drugs — 9 Imported, 12 JV
Top 15 priority drugs (see `figure2_top15.png` and `figure4_heatmap.png`):

| Drug ID | Origin | Priority | Backlog | Supply | Quality |
|---|---|---|---|---|---|
| UhKF57059 | JV | 73.1 | 83.5 | 59.1 | 74.7 |
| CHih47021 | JV | 69.0 | 81.6 | 58.1 | 65.7 |
| HefB27775 | JV | 66.8 | 61.3 | 81.5 | 59.8 |
| nEhy59489 | Imported | 66.2 | 68.7 | 58.6 | 70.2 |
| HOeX41903 | JV | 65.5 | 80.5 | 58.5 | 56.5 |
| yPOK56280 | JV | 65.0 | 66.8 | 74.6 | 54.9 |
| uPIW68939 | Imported | 64.4 | 81.5 | 49.6 | 60.1 |
| pjeu02085 | JV | 64.2 | 79.1 | 43.3 | 67.2 |
| KUaK82776 | Imported | 63.9 | 56.5 | 77.7 | 59.6 |
| IPC09701 | JV | 63.6 | 63.4 | 49.7 | 75.7 |
| PAsyf73184 | JV | 62.7 | 60.5 | 61.5 | 66.0 |
| ciHyk53653 | Imported | 62.1 | 69.6 | 73.7 | 44.6 |
| oXZ18640 | Imported | 62.0 | 72.6 | 48.8 | 62.7 |
| XkGu08654 | Imported | 61.6 | 72.4 | 46.7 | 63.6 |
| ceaEl51255 | JV | 61.6 | 64.8 | 49.5 | 68.7 |

**Risk-profile of the critical tier**: 20/21 Frozen or Scrapped, 13/21 Severe or Alert inventory alerts, 15/21 quarantine-held, 15/21 GSP non-certified, 13/21 refrigerated storage, and 15/21 cold-chain transport — i.e., these drugs combine unusable status, cold-chain sensitivity, and weak certification simultaneously.

### 3. Acute supply-interruption (dual-risk) drugs — 13 drugs with zero qualified stock AND frozen/scrapped
These are effectively **unavailable to dispense** and carry large defective inventories, making them the highest supply-interruption priority (Imported: RiY49601? – see below; 4 Imported, 9 JV):

| Drug ID | Origin | Status | Qualified | Near-expiry | Expired | Contam. | Notes |
|---|---|---|---|---|---|---|---|
| RiY49601 | JV | Scrapped | 0 | 3,156 | **2,550** | 2 | largest expiry volume |
| PAsyf73184 | JV | Scrapped | 0 | 2,163 | **2,052** | 2 | GSP not certified |
| ciHyk53653 | Imported | Frozen | 0 | 3,912 | 1,769 | 4 | cold-chain |
| HefB27775 | JV | Frozen | 0 | 1,789 | 628 | 4 | Severe alert, GSP not certified |
| yPOK56280 | JV | Frozen | 0 | 972 | 491 | 3 | GSP not certified |
| KOIOq72539 | Imported | Scrapped | 0 | 1,092 | 68 | 3 | Severe alert |
| KUaK82776 | Imported | Scrapped | 0 | 636 | 60 | 1 | Severe alert, GSP not certified |

These drugs present a **simultaneous triple threat**: (a) large frozen/scrapped backlogs occupying warehouse capacity, (b) complete loss of dispensable supply, and (c) major expired/damaged volumes that must be scrapped — i.e., backlog is being converted into waste rather than demand.

### 4. Quality-risk concentration
The highest quality-risk drugs (e.g., TNVY60239 [81.6], ywC04617 [81.4], iVry08865 [78.3], IPC09701 [75.7]) are characterized by very high near-expiry + expired volumes combined with refrigerated storage and contamination/excursion records. For temperature-sensitive refrigerated drugs, supervision should focus on cold-chain integrity (storage + transport) and GSP certification status, since non-certified cold-chain handlers multiply excursion risk.

## Conclusions & Recommendations
1. **Immediate-priority (critical tier, 21 drugs)**: verify stock status resolution (defrost/re-certification vs. scrapping), quarantine disposition, and cold-chain handling for the top-ranked drugs; prioritize the 13 dual-risk (zero-qualified + frozen/scrapped) drugs for emergency re-supply because qualified stock is exhausted.
2. **Backlog supervision**: Imported/JV portfolios run at ~2.1–2.3× threshold with ~25% of stock already defective/expired — enforce expiry-alert workflows and stop further replenishment for drugs already >2× threshold with large near-expiry/expired balances (e.g., UhKF57059, CHih47021, uPIW68939).
3. **Supply-interruption supervision**: monitor zero-qualified + quarantine-held positions (severe-frozen combinations: 14 Imported / 20 JV with severe alert & frozen; 12/17 severe & scrapped) and trigger re-supply before qualified stock reaches zero.
4. **Quality supervision**: prioritize GSP non-certified refrigerated/cold-chain drugs (60 Imported / 59 JV non-certified) for storage-environment audits; correlate temp/humidity excursion records with defective volumes.

## Limitations
- The dataset reflects a single snapshot (inventory dates 2024-01…2024-12); "staleness" is measured against end of 2024, not the current date.
- `Inventory Discrepancy Rate` mixes percentage and decimal formats; parsed conservatively.
- Scoring weights are analyst-defined (equal-ish across the three mandated perspectives); sub-scores are robust to moderate weight changes but rankings shift slightly with large weight changes.
- One inventory record (`yqq47916`) has no matching basic-drug record and was excluded.
- Price-flag, ADR, and contraindication data exist but were used only as supplementary context, not in the scores.

## Figures
- `figure1_scores_by_origin.png` — risk sub-scores by origin (box/violin)
- `figure2_top15.png` — top-15 priority drugs by score
- `figure3_scatter.png` — backlog vs. quality risk (bubble = supply-interruption)
- `figure4_heatmap.png` — risk profile of top-15 drugs
- `figure5_distribution.png` — priority-score distributions by origin
- `figure6_indicators.png` — key risk-indicator comparison (Imported vs. JV)
- `priority_scores.csv` — full per-drug scoring output (264 drugs)