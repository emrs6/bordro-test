# `api.py`: hoca sorarsa

## Ne işe yarıyor?
Hesap motoru (`bordro/`) saf Python. `api.py` onu web'e açar: tarayıcıdaki sayfa `POST /api/hesapla` adresine JSON gönderir, cevap olarak 12 ayın bordrosunu JSON olarak alır. Çatı olarak **FastAPI** kullanılıyor.

## İstek ve cevap
```json
// İstek
{"ocak_brut": "50000", "zamlar": [{"ay": 7, "oran": "30"}], "ikramiyeler": [{"ay": 6, "tutar": "50000"}]}
// Cevap (kısaltılmış)
{"aylar": [{"ay": 1, "net": "40207.53", "dilimler": [15], "dilim_degisti": false, ...}, ...],
 "yillik": {"toplam_net": "...", ...}}
```

## Parça parça
- **`HesaplaIstek`, `ZamIstek`, `IkramiyeIstek` (pydantic modelleri):** Gelen JSON'un şeklini tanımlar. Bir alan eksikse (ör. `ocak_brut` yok) FastAPI otomatik olarak **422** döner; bizim kodumuz hiç çalışmaz.
- **`sayi(x)`:** Sayıyı `Decimal(str(x))` ile okur. JSON'dan `33030.1` gibi bir ondalıklı sayı gelirse `str` önce onu "33030.1" metnine çevirir; `Decimal` da tam o değeri alır. Doğrudan `Decimal(33030.1)` yazsaydık 33030.09999999999854... gibi bir değer çıkardı.
- **`json_uyumlu(...)`:** `Decimal` JSON'a doğrudan yazılamaz. Her tutarı 2 ondalıklı metne çevirir ("33030" → "33030.00"); listeleri ve sözlükleri içine kadar dolaşır.
- **`dogrulama_hatasi` (exception handler):** Hesap motoru kurallara uymayan girdide Türkçe mesajlı `ValueError` fırlatıyordu. Bu fonksiyon onu yakalayıp **422 + `{"detail": "<mesaj>"}`** cevabına çevirir. Sayfa da bu mesajı kullanıcıya gösterecek.
- **`hesapla(...)`:** İsteği motorun beklediği tiplere (`Decimal`, `Zam`, `Ikramiye`) çevirir, `bordro_hesapla`'yı çağırır, sonucu JSON'a uygun hale getirir.
- **`anasayfa()` ve `/static`:** Tarayıcıda `http://127.0.0.1:8000` açılınca sayfayı (`static/index.html`) gönderir.

## Çalıştırma
```
.venv\Scripts\uvicorn api:app --reload
```
Sonra tarayıcıda http://127.0.0.1:8000 ve otomatik dokümantasyon için http://127.0.0.1:8000/docs.

## Testler (`tests/api/test_api.py`)
API seviyesindeki altyapı testleri: geçerli istek, 50.000 TL'nin neti, asgari altı → 422 + mesaj, eksik alan → 422, ondalıklı sayı tam okunuyor mu, tutarlar 2 ondalıklı mı, ana sayfa HTML dönüyor mu.
