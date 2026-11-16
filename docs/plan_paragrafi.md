# Proje plan paragrafı

- **Son tarih:** 30 Ekim 2026 23:59, Google Form (kaçırıldı; form kapandı)
- **Gönderim:** 1 Kasım 2026 17:42, e-posta ile; emre.sulun@bilgiedu.net → ekrem.erol@bilgi.edu.tr
- **Konu satırı:** "CMPE 411 - Late submission of project plan paragraph (Emre Sülün, 124200077)"
- **Hocanın cevabı (1 Kasım 2026, 23:16):** Geç plan kabul edilmiyor. Bu yalnızca Milestones puanını etkiliyor; onaylı kendi konuyla (OWN) devam edilebilir.

## Gönderilen paragraf

I will write a Turkish payroll calculator in Python that computes the monthly gross-to-net salary for 2026 (SGK and unemployment premiums with the SGK ceiling, cumulative income tax brackets for wage income, the minimum wage tax exemption and stamp tax), with raises and bonuses entered as rules, and a small web page that shows the result for each month of the year. I will test it at three levels: unit tests with pytest for the calculation rules, API tests for a FastAPI endpoint, and end-to-end tests with Playwright on the web page. I will design the tests with boundary value analysis (tax bracket limits, the SGK ceiling, the minimum wage), equivalence partitioning (valid and invalid inputs), a decision table (bonus, ceiling, bracket change, exemption period) and state transition (moving through tax brackets during the year). As the AI element (option A), I will ask an LLM to generate tests from the written rules, review every expected value against the official 2026 parameters, and compare the generated suite with my own tests using coverage, mutation testing (mutmut) and versions of the code with planted defects, including an experiment where the LLM also sees the code.
