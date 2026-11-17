# Sınır değer analizi (Boundary Value Analysis)

## Kısa ders
Hatalar çoğunlukla sınırlarda olur. Programcı "kadar" yerine "altında" yazar (`<=` yerine `<`), bir kuruşluk fark gözden kaçar. Sınır değer analizi her sınır için **üç nokta** dener:
- sınırın hemen altı
- sınırın kendisi
- sınırın hemen üstü

"Hemen" paralarda 1 kuruş (0,01) demek.

**Örnek (bordro dışı, Lab 1'den):** "Kargo 2 kg'a **kadar** 30 TL, üstü 50 TL."

| R-no | Fonksiyon → çıktı | Girdi | Beklenen | Gerekçe |
|---|---|---|---|---|
| (kargo) | `shipping_fee` | 1.99 | 30 | sınırın altı |
| (kargo) | `shipping_fee` | 2 | 30 | sınırın kendisi: "kadar" dahil |
| (kargo) | `shipping_fee` | 2.01 | 50 | sınırın üstü |

Lab 1'deki gizli hata tam 2 kg'daydı; sadece ortadaki satır onu yakalıyordu.

## Bordroda sınır nerelerde? Gereksinimlerde şunlara bakın:
- **R2:** Ocak brütünün alt ve üst sınırı
- **R3, R4:** zam ayı ve zam oranının sınırları
- **R10:** SGK tavanı. İpucu: bir ayın toplam brütü (maaş + ikramiye) tavana denk gelecek şekilde ikramiye seçebilirsiniz.
- **R14 / R18:** vergi dilim sınırları. `oran(x)` ve `kumulatif_vergi(x)` ile doğrudan test edilebilir.
- **R16:** damga vergisinin sıfır olduğu yer (asgari ücret)

Her satır için beklenen değeri gereksinimdeki formülle elle hesaplayın. Geçersiz girdilerde beklenen, R2–R7 tablosundaki hata mesajıdır.

## Tablonuz (en az 10 satır)

| R-no | Fonksiyon → çıktı | Girdi | Beklenen | Gerekçe |
|---|---|---|---|---|
| R2 | `bordro_hesapla` → hata | Ocak brüt 33.029,99 TL | "Ocak brüt maaşı en az 33.030,00 TL olmalı" | alt sınırın 1 kuruş altı |
| R2 | `bordro_hesapla` → başarılı | Ocak brüt 33.030,00 TL | Ocak net 28.075,50 TL | tam alt sınır |
| R2 | `bordro_hesapla` → başarılı | Ocak brüt 33.030,01 TL | Ocak net 28.075,51 TL | alt sınırın 1 kuruş üstü |
| R2 | `bordro_hesapla` → başarılı | Ocak brüt 9.999.999,99 TL | Ocak net 6.324.307,72 TL | üst sınırın 1 kuruş altı |
| R2 | `bordro_hesapla` → başarılı | Ocak brüt 10.000.000,00 TL | Ocak net 6.324.307,73 TL | tam üst sınır |
| R2 | `bordro_hesapla` → hata | Ocak brüt 10.000.000,01 TL | "Ocak brüt maaşı en fazla 10.000.000,00 TL olabilir" | üst sınırın 1 kuruş üstü |
| R4 | `bordro_hesapla` → başarılı | Ocak brüt 33.030,00 TL, Şubat zammı %99,99 | Şubat brüt 66.056,70 TL | zam üst sınırının 0,01 puan altı |
| R4 | `bordro_hesapla` → başarılı | Ocak brüt 33.030,00 TL, Şubat zammı %100,00 | Şubat brüt 66.060,00 TL | tam zam üst sınırı |
| R4 | `bordro_hesapla` → hata | Ocak brüt 33.030,00 TL, Şubat zammı %100,01 | "Zam oranı 0'dan büyük ve en fazla 100 olmalı" | zam üst sınırının 0,01 puan üstü |
| R6 | `bordro_hesapla` → hata | Ocak brüt 33.030,00 TL, Ocak ikramiyesi 0,00 TL | "İkramiye tutarı 0'dan büyük olmalı" | ikramiye alt sınırında geçersiz değer |
