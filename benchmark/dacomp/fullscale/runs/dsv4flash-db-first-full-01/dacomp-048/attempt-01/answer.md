# Starting Salary & Benefits Analysis for Vocational School Graduates

## Data Scope
The analysis is based on job postings in the database that explicitly require **"Vocational school or above"** education (`Education Requirement = 'Vocational school or above'`). This is the most direct representation of positions open to vocational school graduates.

- **Total qualifying postings:** 9,073
- **Postings with salary data:** 7,936 (3 records with impossible values such as "4-5 yuan/month" were removed, leaving **7,933** for analysis)
- **Postings with benefits data:** 8,055
- Salary was parsed from the "Salary Range" field into a monthly minimum and maximum, and a midpoint = (min+max)/2 was used as the primary measure.

---

## 1. Starting Salary Distribution

![Salary Distribution](salary_distribution.png)

**Key statistics (monthly, yuan):**

| Measure | Value |
|---|---|
| Mean midpoint | **~6,190** |
| Median midpoint | **5,500** |
| Mean lower bound (starting pay) | ~4,816 |
| Mean upper bound | ~7,566 |
| P5 / P25 / P50 / P75 / P90 / P95 | 3,500 / 4,500 / 5,500 / 7,000 / 9,000 / 11,500 |

**Salary bands (by midpoint):**

| Band (yuan/month) | % of postings |
|---|---|
| < 3,000 | 1.3% |
| 3,000–4,000 | 9.7% |
| 4,000–5,000 | 22.6% |
| 5,000–6,000 | 21.5% |
| 6,000–7,000 | 16.1% |
| 7,000–8,000 | 11.8% |
| 8,000–10,000 | 9.0% |
| 10,000–15,000 | 5.6% |
| > 15,000 | 2.4% |

**Interpretation:** The typical starting salary for vocational school graduates is concentrated in the **4,000–7,000 yuan/month** range (≈60% of postings). About 17% of postings offer 8,000+ yuan/month, usually in sales/commission and skilled-technical roles.

---

## 2. Benefits Distribution

![Benefits Distribution](benefits_distribution.png)

Among the 7,933 analyzed postings (percentages relative to postings with salary data):

| Benefit | Postings | % |
|---|---|---|
| Five Social Insurances (五险) | 6,169 | 77.8% |
| Paid Annual Leave | 4,252 | 53.6% |
| Holiday Benefits | 4,175 | 52.6% |
| Performance Bonus | 3,609 | 45.5% |
| Full Attendance Bonus | 2,906 | 36.6% |
| Housing Provident Fund | 2,287 | 28.8% |
| Employee Travel | 2,256 | 28.4% |
| Professional Training | 2,130 | 26.9% |
| Overtime Pay | 2,023 | 25.5% |
| Meal Allowance | 1,851 | 23.3% |
| Commercial Insurance | 1,840 | 23.2% |
| Double Pay at Year End | 1,706 | 21.5% |
| Work Uniform | 1,696 | 21.4% |
| Housing/Accommodation | 1,315 | 16.6% |
| Meals Provided | 1,297 | 16.4% |
| Communication Allowance | 1,108 | 14.0% |
| High-Temperature Allowance | 956 | 12.1% |
| Year-End Bonus | 559 | 7.0% |
| Flexible Working Hours | 528 | 6.7% |
| Free Shuttle Bus | 474 | 6.0% |
| Medical Checkups | 31 | 0.4% |

**Interpretation:** Social insurance is nearly universal (78%), and roughly half of postings add paid annual leave, holiday benefits, or a performance bonus. Statutory/standard protections (insurances, leave) are common, whereas premium perks (year-end bonus, flexible hours, medical checkups) are rare.

---

## 3. Which Qualities Significantly Increase Starting Salary?

![Salary Factors](salary_factors.png)

### 3.1 Work Experience — strongest and most significant factor
- **ANOVA across experience groups:** F = 77.8, p ≈ 9×10⁻¹³⁹
- **Pearson correlation** between required years of experience and salary: **r = 0.345, p < 10⁻¹⁰⁹** (Spearman ρ = 0.369)

| Experience Requirement | n | Mean Salary (yuan) | Δ vs "No limit" |
|---|---|---|---|
| Fresh graduates | 155 | 5,162 | −744 |
| No limit | 4,031 | 5,906 | — |
| 1+ year | 1,581 | 5,723 | −184 |
| 2+ years | 1,037 | 6,389 | +483 |
| 3+ years | 800 | 7,372 | +1,466 |
| 4+ years | 34 | 8,559 | +2,652 |
| 5+ years | 243 | 8,755 | +2,849 |
| 6+ years | 9 | 12,328 | +6,422 |
| 8+ years | 19 | 11,000 | +5,094 |

Pairwise t-tests: 2+ yrs vs no-limit p<0.0001; 5+ yrs vs no-limit p<0.0001; fresh-grads vs no-limit p<0.0001. **Every additional year of experience is associated with a large, statistically significant salary premium.** Higher-paying roles also skew to sales (sales manager, sales representative, telemarketing) and skilled technical work (mold design, electrician, production manager).

### 3.2 Foreign Language (English fluency)
- Jobs requiring **"Proficiency in English required"** (fluent English): mean **8,657** yuan vs 6,186 for all other postings (t = 2.77, **p = 0.011**), but this is a small group (n = 23).
- General "English" mentions are not significant (mean ≈ 6,207, p = 0.93), indicating that only a *demonstrated strong* English skill is associated with a premium.

### 3.3 Company Type
- ANOVA across company types: F = 18.4, **p ≈ 4×10⁻¹⁵**
- **Listed companies: 6,812** (t-test vs private, p = 0.04)
- Private joint-stock: 6,346; Private: 6,310; Foreign (EU/US): 5,915
- Lower: Taiwanese/Hong Kong capital 5,517; public institutions 5,405; foreign (Japanese etc.) 5,369; **State-owned enterprises lowest at 5,120**

### 3.4 Industry
High-paying industries (mean, primary tag, n≥20): intermediary services 11,143; insurance 9,931; home furnishing/interior design 8,061; construction & engineering 7,969; beauty/health 7,799; IT/data services 7,620–6,976; finance/securities 7,375; automotive 6,886.
Low-paying: **Hotels/tourism 4,066**, property management 4,962–5,274, food/catering 5,073, medical equipment 5,246.

### 3.5 Location (within the Xiamen labor market)
- City center / main urban listings pay more: "Siming District" 7,202; general "Xiamen" 6,577; Huli 6,207.
- Outer districts pay less: Tong'an 5,612, Xiang'an 5,614, Haicang 5,914.

### 3.6 Gender requirement (descriptive)
- No gender requirement: 6,223; female-specific: 6,007; male-specific: 5,003 (female vs male t-test p<0.0001). Male-specific postings are relatively few (n=57) and concentrated in lower-paid manual roles.

### 3.7 Benefits that co-occur with higher salaries (correlational, not causal)
![Benefit Salary Impact](benefit_salary_impact.png)

| Benefit | Δ Salary vs postings without it | p-value |
|---|---|---|
| Flexible Working Hours | **+1,480** | <0.0001 |
| Year-End Bonus | **+895** | <0.0001 |
| Communication Allowance | **+833** | <0.0001 |
| Performance Bonus | **+816** | <0.0001 |
| Professional Training | +599 | <0.0001 |
| Employee Travel | +591 | <0.0001 |
| Holiday Benefits | +285 | <0.0001 |
| Paid Annual Leave | +235 | 0.0001 |
| Full Attendance Bonus | +232 | 0.0003 |
| Five Social Insurances | +186 | 0.0095 |
| Overtime Pay | −244 | 0.0002 |
| Meals/Housing Provided | −196 to −333 | <0.02 |

Premiums are found with flexible hours, bonuses, allowances, training, and travel — typical of white-collar/sales/professional positions. In contrast, factory-type roles that provide meals, accommodation, or overtime pay pay less. These are **associations**; the benefits themselves do not cause higher salaries but signal the job tier.

---

## Conclusion

1. **Starting salary distribution:** Vocational school graduates typically start at **4,000–7,000 yuan/month** (median ~5,500; mean ~6,190), with roughly 17% of postings offering 8,000+ and only ~1% below 3,000.
2. **Benefits distribution:** Five social insurances (78%), paid annual leave (54%), and holiday benefits (53%) are the most common; premium benefits (year-end bonus, flexible hours, medical checkups) are rare (<7%).
3. **Qualities that significantly raise starting salary:**
   - **Work experience** is by far the strongest lever (3+ years ≈ +1,470 yuan; 5+ years ≈ +2,850 yuan vs no-limit; r = 0.35, p < 10⁻¹⁰⁹).
   - **Strong English proficiency** (not merely any English mention).
   - **Working for listed companies** and in high-paying industries (insurance, intermediary services, IT, construction, finance, automotive).
   - **Working in central urban locations** (Siming district / central Xiamen).
   - **Sales / skilled-technical roles** (sales, mold design, electricians, production management) are the highest-paying job families.
   - Flexible hours, performance/year-end bonuses, and communication allowances appear in higher-paying jobs (correlational signal).

## Limitations
- Analysis covers postings explicitly listing "Vocational school or above"; vocational graduates could also take jobs labeled "No limit", "High school", or "Junior high school" which were excluded.
- Salary parsing assumed the "low–high /month" format; commission-based structures used the listed headline range.
- Benefits are free text; keyword matching may miss rare synonyms or unusual phrasings.
- Benefit–salary and factor–salary relationships are observational (associations), not causal; small subgroups (e.g., 6+ years experience, fluent English, n < 25) should be interpreted cautiously.
