# 2026 bordro parametreleri: testlerin "doğru cevap" kaynağı

Toplanma tarihi: 21 Ekim 2026. Kapsam: özel sektör, standart çalışan (emekli, engelli veya teşvikli değil).

## 1. Gelir vergisi tarifesi (GVK md. 103, 2026, ücret gelirleri)
Kaynak: GİB, "Gelir Vergisi Tarifesi 2026" (332 Seri No'lu GV Genel Tebliği, RG 31.12.2025 / 33124 5. Mükerrer)
https://cdn.gib.gov.tr/api/gibportal-file/file/getFileResources?objectKey=arsiv%2Fyardim-kaynaklar%2Fyararli-bilgiler%2Fgelir-vergisi-tarifeleri%2Fgelir-vergisi-tarifesi-2026.pdf

| Kümülatif matrah (ücret) | Oran | Önceki dilimlerin sabit vergisi |
|---|---|---|
| 0 – 190.000 | %15 | 0 |
| 190.000 – 400.000 | %20 | 28.500 |
| 400.000 – 1.500.000 | %27 | 70.500 |
| 1.500.000 – 5.300.000 | %35 | 367.500 |
| 5.300.000 üzeri | %40 | 1.697.500 |

Not: Ücret dışı gelirlerde 3. dilim 1.000.000'da biter. **Biz ücret tarifesini kullanıyoruz.**
Kontrol: 70.500 + 1.100.000×0,27 = 367.500 ✓ · 367.500 + 3.800.000×0,35 = 1.697.500 ✓

## 2. Asgari ücret ve SGK sınırları (2026, tüm yıl; Temmuz'da ara zam yok)
Kaynak: SGK, "Prime Esas Kazanç Miktarları" (özel sektör, 1/1/2026–31/12/2026)
https://www.sgk.gov.tr/Content/Post/2e0c9e1a-2cfe-4456-af10-49d3de0c58ba/Prime-Esas-Kazanc-Miktarlari-2026-01-14-10-35-39

| Parametre | Tutar |
|---|---|
| Brüt asgari ücret = SGK alt sınır (aylık) | 33.030,00 TL |
| SGK üst sınır / tavan (aylık, alt sınırın 9 katı) | 297.270,00 TL |
| Günlük alt / üst | 1.101,00 / 9.909,00 TL |

## 3. Kesinti oranları (çalışan payı)
| Kesinti | Oran | Dayanak |
|---|---|---|
| SGK işçi payı | %14 (%9 malullük-yaşlılık-ölüm + %5 genel sağlık) | 5510 s. Kanun |
| İşsizlik sigortası işçi payı | %1 | 4447 s. Kanun |
| Damga vergisi | binde 7,59 (brüt üzerinden) | 488 s. DVK, (1) sayılı tablo |

## 4. Asgari ücret istisnası (GVK md. 23/18 ve DVK, 7349 s. Kanun ile, 2022'den beri)
- Gelir vergisi: Asgari ücrete düşen gelir vergisi kadar istisna uygulanır. Tutar, asgari ücretin kümülatif matrahı üzerinden her ay ayrı hesaplanır.
- Damga vergisi: Brüt asgari ücretin damga vergisi kadar istisna uygulanır: 33.030 × 0,00759 = **250,70 TL/ay**.

Kendi hesabım (ikincil kaynaklardaki tutarlarla birebir aynı çıktı):
- Asgari ücret GV matrahı = 33.030 − %15 SGK+işsizlik (4.954,50) = 28.075,50 TL
- Ocak–Haziran: 28.075,50 × %15 = **4.211,33 TL**
- Temmuz (kümülatif 168.453 → 196.528,50, dilim geçişi): 21.547 × %15 + 6.528,50 × %20 = **4.537,75 TL**
- Ağustos–Aralık: 28.075,50 × %20 = **5.615,10 TL**
- Net asgari ücret = 33.030 − 4.954,50 = **28.075,50 TL** ✓ (resmî açıklanan net)

## Kapsam dışı (şimdilik)
- Devreden SGK matrahı (tavanı aşan ikramiyenin sonraki 2 aya devri)
- Engellilik indirimi, emekli (SGDP) çalışan, teşvikler, BES, yemek/yol istisnaları, kamu sektörü
- 2026 dışındaki yıllar

## İkincil kaynaklar (çapraz kontrol için)
- https://www.alomaliye.com/2025/12/31/2026-yili-vergi-dilimleri/
- https://www.muhasebetr.com/bordro-parametreleri
- https://www.alomaliye.com/asgari-ucret/
