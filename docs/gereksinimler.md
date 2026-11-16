# Requirements: Turkish payroll calculator (2026)

This document is the specification. Every test, written by a person or by an LLM, takes its expected values from these rules only. The official sources of the 2026 values are listed in `docs/Mevzuat_2026.md`.

Scope: private sector, a standard employee (not retired, no disability deduction, no incentives), calendar year 2026, 12 months.

## Inputs

- **R1.** The input is: the January gross salary (TL), a list of raises `(month, percent)` and a list of bonuses `(month, amount TL)`.
- **R2.** The January gross salary must be at least 33,030.00 TL (the 2026 gross minimum wage) and at most 10,000,000.00 TL. Otherwise the input is rejected.
- **R3.** A raise month must be a whole number from 2 to 12 (no raise in January). A bonus month must be a whole number from 1 to 12. Otherwise the input is rejected.
- **R4.** A raise percent must be greater than 0 and at most 100. Otherwise the input is rejected.
- **R5.** Two raises in the same month are rejected. Two or more bonuses in the same month are allowed and are added together.
- **R6.** A bonus amount must be greater than 0. Otherwise the input is rejected.
- **R7.** All amounts and percents may have at most 2 decimal places. Otherwise the input is rejected.

When an input is rejected, no result is produced and the user sees a Turkish error message:

| Rule | Message |
|---|---|
| R2 (too low) | `Ocak brüt maaşı en az 33.030,00 TL olmalı` |
| R2 (too high) | `Ocak brüt maaşı en fazla 10.000.000,00 TL olabilir` |
| R3 (raise) | `Zam ayı 2 ile 12 arasında olmalı` |
| R3 (bonus) | `İkramiye ayı 1 ile 12 arasında olmalı` |
| R4 | `Zam oranı 0'dan büyük ve en fazla 100 olmalı` |
| R5 | `Aynı aya birden fazla zam girilemez` |
| R6 | `İkramiye tutarı 0'dan büyük olmalı` |
| R7 | `Tutarlar en fazla 2 ondalık basamak içerebilir` |

## Monthly salary

- **R8.** The salary of a month is the salary of the previous month, increased by the raise of that month if there is one. Raises are applied in month order and compound: after each raise the salary is rounded to kuruş (see R20). Example: January 33,030.01; July +30% gives 42,939.01 from July; October +10% gives 47,232.91 from October.
- **R9.** The total gross of a month is that month's salary plus that month's bonuses.

## Monthly deductions (m = 1 … 12, computed in order)

- **R10.** SGK base = the month's total gross, but at most 297,270.00 TL (the 2026 SGK ceiling). The part above the ceiling is not subject to SGK and is not carried to later months.
- **R11.** SGK employee premium = 14% of the SGK base. Unemployment insurance employee premium = 1% of the SGK base.
- **R12.** Income tax base of the month = total gross − SGK employee premium − unemployment premium.
- **R13.** The cumulative income tax base after month m is the sum of the monthly income tax bases from January to month m (it starts from 0 in January).
- **R14.** Income tax is computed with the 2026 **wage income** tariff T(x) applied to the cumulative base:

  | Cumulative base x | Tax T(x) |
  |---|---|
  | up to 190,000 | 15% of x |
  | 190,000 – 400,000 | 28,500 + 20% of the part above 190,000 |
  | 400,000 – 1,500,000 | 70,500 + 27% of the part above 400,000 |
  | 1,500,000 – 5,300,000 | 367,500 + 35% of the part above 1,500,000 |
  | above 5,300,000 | 1,697,500 + 40% of the part above 5,300,000 |

  The calculated income tax of month m = T(cumulative base after m) − T(cumulative base after m−1).
- **R15.** Minimum wage income tax exemption of month m = T(28,075.50 × m) − T(28,075.50 × (m−1)). (28,075.50 is the monthly income tax base of the minimum wage.) The income tax actually deducted = calculated income tax − exemption, but never below 0.
- **R16.** Stamp tax = 0.759% (binde 7,59) of the month's total gross, minus the minimum wage stamp tax exemption of 250.70 TL, but never below 0.
- **R17.** Net pay = total gross − SGK employee premium − unemployment premium − income tax deducted − stamp tax.

## Tax bracket information

- **R18.** A limit belongs to the lower bracket: a cumulative base of exactly 190,000.00 is in the 15% bracket, 190,000.01 is in the 20% bracket. The same holds for 400,000, 1,500,000 and 5,300,000.
- **R19.** For each month the result also shows:
  - **brackets**: the tax rates (in increasing order) that this month's base passes through, i.e. the rates with a positive part in the interval (cumulative base after m−1, cumulative base after m]. Example: from 168,453.00 to 196,528.50 gives [15, 20].
  - **starting rate**: the rate of the bracket that contains the cumulative base after m−1 (15 in January).
  - **bracket changed**: true when the highest rate in *brackets* is greater than the starting rate. This can be true in January too.

## Rounding

- **R20.** Every amount (salary after a raise, SGK premium, unemployment premium, calculated income tax, exemption, stamp tax before the 250.70 deduction) is rounded to kuruş (2 decimal places), halves rounded up (0.005 → 0.01). The cumulative base is the sum of the rounded monthly bases.

## Yearly totals

- **R21.** The result also shows yearly totals: total gross, total net, total income tax deducted, and total SGK (SGK employee premium + unemployment premium).
