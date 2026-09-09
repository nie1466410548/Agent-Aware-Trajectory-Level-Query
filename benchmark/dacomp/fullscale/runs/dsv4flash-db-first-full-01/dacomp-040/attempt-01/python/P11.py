# Final summary computations
import numpy as np

# Higher education rates by gender (already computed, recompute precisely)
# 2000
f_higher_2000 = 11664728 + 4941964 + 266681
m_higher_2000 = 17320758 + 9208762 + 617252
fpop2000, mp2000 = 563230615, 593469678
# 2010
f_higher_2010 = 31740144 + 20408710 + 1787334
m_higher_2010 = 36870375 + 25217083 + 2351251
fpop2010, mp2010 = 609267735, 633278387
# 2020
f_higher_2020 = 53575442 + 46519060 + 4766905 + 503329
m_higher_2020 = 58727560 + 47637012 + 4721323 + 774020
fpop2020, mp2020 = 643666350, 671681215

for yr, (mh, fh, mp, fp) in [(2000,(m_higher_2000,f_higher_2000,mp2000,fpop2000)),
                             (2010,(m_higher_2010,f_higher_2010,mp2010,fpop2010)),
                             (2020,(m_higher_2020,f_higher_2020,mp2020,fpop2020))]:
    print(f"{yr}: Male higher edu rate = {100*mh/mp:.2f}%, Female higher edu rate = {100*fh/fp:.2f}%")
    print(f"      Male higher = {mh:,}, Female higher = {fh:,}")

# Regional population shares (6+)
pops = [(2000, 276608948, 154912145, 725179200),
        (2010, 384147858, 248689641, 609708623),
        (2020, 538489518, 301375243, 475482804)]
for yr, u, t, r in pops:
    tot = u+t+r
    print(f"{yr}: urban/city share = {100*u/tot:.1f}%, town = {100*t/tot:.1f}%, rural/village = {100*r/tot:.1f}%")

# Key growth multiples
print("\nNo schooling (6+):", 89629436+20767295, "->", 62136405, "->", 41543985)
print("Higher education total: 2000 =", 28985486+14150726+883933, 
      "; 2010 =", 68610519+45625793+4138585,
      "; 2020 =", 112303002+94156072+9488228+1277349)
print("Undergraduate+ growth 2000->2020:", (94156072+9488228+1277349)/(14150726+883933))
print("Higher education growth 2000->2020:", (112303002+94156072+9488228+1277349)/(28985486+14150726+883933))
print("Never attended decline 2000->2020:", 1-41543985/89629436)

# Postgraduate in 2020 vs 2000
print("Postgrad 2000:", 883933, "2020:", 9488228+1277349, "growth:", (9488228+1277349)/883933)

# Young cohort 20-24 higher education rates
print("\n20-24 higher edu rate: 2000=8.6%, 2010=25.3%, 2020=51.9%")
# Master's + doctoral female share 2020
print("Master's female share 2020: 50.2%; Doctoral female share 2020: 39.4%")
print("Female undergrad share 2020: 49.4% vs 2000: 34.9%")