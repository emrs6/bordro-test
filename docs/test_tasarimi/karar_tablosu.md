# Karar tablosu (Decision Table)

## Kısa ders
Sonuç birden fazla koşulun **birleşimine** bağlıysa, koşulların her kombinasyonunu bir "kural" olarak yazarız. Böylece hiçbir kombinasyon unutulmaz.

**Örnek (Week 5 slaytından):** "STUDENT10 kuponu %10 indirim: sadece doğrulanmış öğrenci + sepet ≥ 200 TL + başka kupon yok."

| Kural | Öğrenci? | Sepet ≥ 200? | Başka kupon? | Sonuç |
|---|---|---|---|---|
| K1 | Hayır | – | – | Reddedilir |
| K2 | Evet | Hayır | – | Reddedilir |
| K3 | Evet | Evet | Evet | Reddedilir |
| K4 | Evet | Evet | Hayır | %10 indirim |

"–" önemsiz demek.

## Bordro için koşullar (tasarım belgesi §7.3)
Bir **ayın** sonucunu şu dört koşul belirler:
1. Bu ay ikramiye var mı? (R9)
2. Bu ayın toplam brütü SGK tavanını aşıyor mu? (R10)
3. Bu ay dilim değişiyor mu? (R19)
4. Asgari ücret istisnası dönemi: Ocak–Haziran / Temmuz / Ağustos–Aralık (R15)

Her kural için bir senaryo kurun (Ocak brüt + zam/ikramiye + hangi ay) ve o ayın beklenen değerlerini elle hesaplayın: `sgk_isci`, `gelir_vergisi`, `dilim_degisti` vb. Bazı kombinasyonlar imkânsız olabilir; o satıra "imkânsız" yazıp nedenini not edin. Bu da raporda değerlidir.

## Tablonuz (en az 8 kural)

| Kural | İkramiye? | Tavan aşılıyor? | Dilim değişiyor? | İstisna dönemi | Senaryo (girdi + ay) | Beklenen | Gerekçe |
|---|---|---|---|---|---|---|---|
| K1 | | | | | | | |
| K2 | | | | | | | |
| K3 | | | | | | | |
| K4 | | | | | | | |
| K5 | | | | | | | |
| K6 | | | | | | | |
| K7 | | | | | | | |
| K8 | | | | | | | |
