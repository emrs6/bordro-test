# Test tasarımı: sizin kısmınız

Bu klasördeki tablolar projenin **"İnsan"** test grubu. Raporda LLM'in testleriyle karşılaştırılacak olan bunlar. O yüzden değerleri ve beklenen sonuçları **siz** seçip **siz** hesaplıyorsunuz. Ben tablolarınızı birebir pytest koduna çeviriyorum, değerlere dokunmuyorum.

## Kurallar (deney dürüst kalsın diye)
- Tek kaynağınız `docs/gereksinimler.md` (R1–R21) ve `docs/Mevzuat_2026.md`.
- `tests/gelistirici/` klasörüne ve `bordro/` koduna **bakmayın**. Oradaki testleri ve kodu ben yazdım; görürseniz tasarımınız benimkine benzer ve karşılaştırma bozulur.
- Beklenen değeri hesap makinesiyle ve gereksinimlerdeki formüllerle **elle** hesaplayın. Programı çalıştırıp çıkan sonucu tabloya yazmayın, yoksa kodda bir hata varsa testiniz o hatayı "doğru" sanır.
- Emin olmadığınız bir satıra "?" koyun, birlikte bakarız.

## Sıra ve minimum (20 Kasım için)
1. **`sinir_degerleri.md`**: en az 10 satır. Lab 3'e yetecek olan bu; önce bunu doldurun.
2. `denklik_siniflari.md`: en az 6 satır
3. `karar_tablosu.md`: en az 8 kural
4. `durum_gecisi.md`: en az 5 geçiş

## Test edebileceğiniz fonksiyonlar (sadece adları ve ne döndürdükleri)
| Fonksiyon | Girdi | Ne döndürür |
|---|---|---|
| `bordro_hesapla(ocak_brut, zamlar, ikramiyeler)` | Ocak brüt, `[Zam(ay, oran)]`, `[Ikramiye(ay, tutar)]` | 12 ay; her ayda `toplam_brut, sgk_isci, issizlik, gv_matrahi, kumulatif_matrah, hesaplanan_gv, au_istisna, gelir_vergisi, damga, net, dilimler, baslangic_orani, dilim_degisti`; ayrıca yıllık toplamlar |
| Geçersiz girdi | aynı | Hata mesajı (R2–R7 tablosundaki metin) |
| `kumulatif_vergi(x)` | birikmiş matrah | T(x) (R14) |
| `oran(x)` | birikmiş matrah | dilim oranı (R18) |

Tabloda "fonksiyon" sütununa sadece adı yazmanız yeter, ör. `bordro_hesapla → Ocak net`.
