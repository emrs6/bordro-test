# Sayfa (`static/index.html`, `app.js`, `style.css`): hoca sorarsa

## Yapı
- **`index.html`:** İskelet. Solda girdiler (Ocak brüt, zam satırları, ikramiye satırları, Hesapla), sağda seçili ayın sonucu, altta yıllık grafik. Zam ve ikramiye satırları `<template>` etiketinden kopyalanarak eklenir.
- **`style.css`:** Görünüm. Renkler `:root` değişkenlerinde: net yeşil, SGK kırmızı, gelir vergisi turuncu, damga mor, ikramiye sarı. Sistem karanlık moddaysa koyu renklere geçer.
- **`app.js`:** Davranış. Framework yok, düz JavaScript.

## `app.js` fonksiyonları
| Fonksiyon | Ne yapar |
|---|---|
| `turkceSayi("50.000,50")` | `"50000.50"` döner. Nokta binlik ayırıcı, virgül ondalık. Sayı değilse "Geçersiz sayı" hatası. Sayıyı **metin** olarak API'ye yollar, böylece JavaScript'in kayan nokta hatası araya girmez. |
| `satirEkle(...)` | "+ Zam ekle" / "+ İkramiye ekle"ye basınca yeni satır. Zam ay listesi Şubat'tan başlar (R3). |
| `satirlariOku(...)` | Satırları okur; **boş bırakılan satırı yok sayar**. |
| `hesapla(...)` | Formu okur, `POST /api/hesapla` çağırır. Hata gelirse (422) sunucunun Türkçe mesajını gösterir. |
| `hataGoster(mesaj)` | Hata kutusunu gösterir ve eski sonucu gizler; yoksa eski sonuç yeni girdiye aitmiş gibi görünürdü. |
| `ayGoster(ay)` | Seçili ayın net maaşını, renkli çubuğu, dilim uyarısını, kesinti tablosunu ve yıllık toplamları çizer. |
| `dilimUyarisi(ay)` | `dilim_degisti` ise "Bu ay %15 diliminden %20 dilimine geçtiniz." metni; birden fazla dilim atlandıysa ara oranlar "(%15 → %20 → %27)". |
| `grafikCiz()` | 12 sütun. Yükseklik net maaşla orantılı; ikramiyeden kalan net sarı (brüt içindeki payı oranında, yaklaşık). Dilim değişen ayın çerçevesi turuncu. Sütuna tıklayınca o ay seçilir. |

## Test için işaretler
Uçtan uca testler elemanları **görünen adlarıyla** bulur: "Ocak brüt maaşı" etiketi, "Hesapla" butonu. Ayrıca `data-testid` işaretleri var: `net-maas`, `dilim-uyarisi`, `hata-mesaji`, `ay-sutunu-1…12`, `yillik-net`. CSS sınıfı ya da sayfa yapısı değişse de testler kırılmaz; Week 5'teki "iyi locator" konusu bu.
