# `kurallar.py`: hoca sorarsa

## `Zam` ve `Ikramiye`
İki küçük `@dataclass`, yani sadece veri taşıyan kutular: `Zam(ay=7, oran=30)` "Temmuz'dan itibaren %30 zam" demek.

## `girdileri_dogrula(...)`: "Geçersiz girdide ne oluyor?"
Kuralları **sırayla** kontrol eder; ilk bozuk kuralda Türkçe mesajlı bir `ValueError` fırlatır ve hesap hiç yapılmaz.

| Kontrol | Gereksinim | Neden bu sırada |
|---|---|---|
| Tüm tutarlar en fazla 2 ondalık | R7 | 33.030,001 gibi bir değer sınır kontrolünü yanıltmasın diye önce bu |
| Ocak brüt ≥ 33.030,00 ve ≤ 10.000.000,00 | R2 | Asgari ücretin altında maaş olamaz |
| Zam ayı 2–12, oran (0, 100] | R3, R4 | Ocak maaşı zaten girdinin kendisi, Ocak'a zam anlamsız |
| Aynı aya iki zam yok | R5 | "Temmuz'da %10 mu %5 mi?" belirsizliğini önler |
| İkramiye ayı 1–12, tutar > 0 | R3, R6 | |

`_iki_ondalikli_mi(x)`: Sayıyı 2 basamağa yuvarlayınca değişmiyorsa en fazla 2 ondalığı vardır.

## `aylik_maaslar(ocak_brut, zamlar)`: "Zam nasıl uygulanıyor?"
- Önce zamlardan bir sözlük kurar: `{7: 30, 10: 10}`.
- Ocak'tan Aralık'a yürür. Zam ayına gelince `maas = kurus(maas × (1 + oran/100))` uygular; maaş o aydan sonra yeni değerle devam eder.
- **Bileşik:** Ekim zammı, Ocak maaşına değil Temmuz'da zamlanmış maaşa uygulanır.
- **Yuvarlama:** 33.030,01 × 1,30 = 42.939,013 → 42.939,01. Sonraki zam bu yuvarlanmış değerden hesaplanır (R8).

## `aylik_ikramiyeler(ikramiyeler)`
12 sıfırlık bir liste kurar, her ikramiyeyi kendi ayına ekler. Aynı aya iki ikramiye girilirse toplanır (R5). Liste 0'dan başladığı için Ocak `[0]`, Haziran `[5]`.
