# `parametreler.py`, `para.py`, `tarife.py`: hoca sorarsa

## parametreler.py: "Rakamlar nereden geliyor?"
2026'nın resmî rakamlarının hepsi burada; başka hiçbir dosyada elle yazılmış bir sayı yok. Her satırın yanında kaynağı yazar (GİB tarifesi, SGK prim tablosu, Damga Vergisi Kanunu). Gelecek yıl rakamlar değişirse sadece bu dosya değişir.

Tarife bir liste: `(üst sınır, oran)`. Son dilimin üst sınırı yok, `None`.

## para.py: "Neden `float` değil de `Decimal`?"
`float` ikili sistemde tutulduğu için 0,1 gibi sayıları tam gösteremez (`0.1 + 0.2 = 0.30000000000000004`). Parada bu, kuruş hatası demek. `Decimal` onluk sistemde tam hesap yapar.

`kurus()` tutarı 2 basamağa yuvarlar; yarımlar yukarı gider (`ROUND_HALF_UP`): 4.211,325 → 4.211,33.

## tarife.py

### `kumulatif_vergi(matrah)`: T(x)
Dilimleri sırayla dolaşır. Matrah bu dilimin içindeyse "önceki dilimlerin vergisi + bu dilimdeki kısmın vergisi" döner. Değilse dilimin tamamının vergisini ekleyip sonraki dilime geçer.

Örnek: T(196.528,50) = 190.000 × %15 + 6.528,50 × %20 = 28.500 + 1.305,70 = 29.805,70.

### `oran(matrah)`: "Bu matrah hangi dilimde?"
`matrah <= ust_sinir` karşılaştırması yüzünden tam 190.000 hâlâ %15 dilimindedir (R18). Tarife metni de "190.000 TL'ye **kadar** %15" diyor. Burada `<` yazmak klasik bir sınır hatası olur. Lab 1'deki 2 kg hatasının aynısı.

### `dilimler(onceki, simdiki)`: "Bu ay hangi oranlardan geçtim?"
Bu ayın matrah aralığı (önceki birikmiş, şimdiki birikmiş]. Her dilim için şuna bakar: aralığın bu dilimin içinde kalan bir parçası var mı?
- `dilim_ust = min(simdiki, ust_sinir)`: aralığın bu dilimdeki üst ucu
- `dilim_ust > max(onceki, alt_sinir)`: parçanın uzunluğu sıfırdan büyükse bu oran listeye girer

Örnek: 168.453 → 196.528,50 aralığı hem %15'e hem %20'ye değiyor → `[15, 20]`. 161.924,50 → 190.000 aralığı ise tam sınırda bitiyor, %20'ye hiç girmiyor → `[15]`.

## Testler (`tests/gelistirici/test_tarife.py`)
GİB tarifesinin kendi verdiği sabit tutarları (28.500, 70.500, 367.500, 1.697.500) ve sınır noktalarını kontrol eder. Bunlar geliştirici testleri; asıl test tasarımını (sınır değer tabloları) siz yapacaksınız.
