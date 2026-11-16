# `hesap.py`: hoca sorarsa

## `AySonucu` ve `YilSonucu`
Bir ayın bordrosundaki her satır `AySonucu`'nda bir alan: maaş, ikramiye, SGK, vergi, net... `YilSonucu` 12 ayı ve yıllık toplamları tutar.

## `ay_hesapla(ay, maas, ikramiye, onceki_kumulatif)`: bir ayın bordrosu
Gerçek bir bordro kâğıdındaki satırlarla aynı sıra:

| Satır | Kod | Gereksinim |
|---|---|---|
| Toplam brüt | `maas + ikramiye` | R9 |
| SGK matrahı | `min(toplam_brut, SGK_TAVAN)`: tavanın üstü SGK'ya girmez | R10 |
| SGK %14, işsizlik %1 | `kurus(sgk_matrahi × oran)` | R11 |
| GV matrahı | brüt − SGK − işsizlik | R12 |
| Birikmiş matrah | önceki birikmiş + bu ayın matrahı | R13 |
| Hesaplanan GV | `T(birikmiş şimdi) − T(birikmiş önce)` | R14 |
| Asgari ücret istisnası | asgari ücretli birinin bu ay ödeyeceği vergi | R15 |
| Kesilen GV | `max(0, hesaplanan − istisna)` | R15 |
| Damga | `max(0, brüt × binde 7,59 − 250,70)` | R16 |
| Net | brüt − tüm kesintiler | R17 |
| Dilim bilgisi | `tarife.dilimler(...)`, `tarife.oran(...)`, değişti mi? | R19 |

**"Vergi neden T(şimdi) − T(önce)?"** Türkiye'de vergi yıllık birikimle hesaplanır. Ocak'tan bu aya kadar toplam ödenmesi gereken vergiden, geçen aya kadar ödenmiş olanı çıkarınca bu ayın vergisi kalır. Birikim bir dilim sınırını geçtiği ay maaşın bir kısmı %15, kalanı %20 ile vergilenir; bu formül bunu kendiliğinden yapar.

**"İstisna neden her ay farklı?"** Asgari ücretlinin birikmiş matrahı da Temmuz'da 190.000'i geçer. Bu yüzden istisna Ocak–Haziran 4.211,33, Temmuz 4.537,75, Ağustos–Aralık 5.615,10 olur. `asgari_ucret_istisnasi(ay)` bunu aynı T formülüyle hesaplar.

## `bordro_hesapla(ocak_brut, zamlar, ikramiyeler)`: ana fonksiyon
1. Girdileri doğrular (`girdileri_dogrula`); bozuksa hata, hesap yok.
2. 12 ayın maaşını ve ikramiyesini çıkarır.
3. Ocak'tan Aralık'a `ay_hesapla`'yı çağırır; her ayın birikmiş matrahı bir sonraki aya aktarılır.
4. Yıllık toplamları hesaplar.

## Kontrol (`tests/gelistirici/test_hesap.py`)
- **Asgari ücretli bir yıl:** Her ay net 28.075,50 TL çıkmalı; bu, resmî olarak açıklanan net asgari ücret. Kod resmî rakamla birebir aynı sonucu veriyor.
- **50.000 TL brüt, Ocak:** Net 40.207,53 TL. Elle hesap: SGK 7.000 + işsizlik 500, vergi 6.375 − 4.211,33 = 2.163,67, damga 379,50 − 250,70 = 128,80.
