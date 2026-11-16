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
| | | | | |
| | | | | |
| | | | | |
| | | | | |
| | | | | |
| | | | | |
| | | | | |
| | | | | |
| | | | | |
| | | | | |
