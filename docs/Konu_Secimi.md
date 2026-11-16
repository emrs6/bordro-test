# Konu seçimi: taslak (son tarih 21 Ekim 2026, 23:59)

Kaynak: `Hafta_04/Donem_Projesi/Project_Brief.pdf` (48 konu, s. 4–6)
Form: https://docs.google.com/forms/d/e/1FAIpQLSf_D7g8cys_83W6Yqj41-dkjXW9sP1E_UIb7R-ie-p-RVGbOg/viewform

## Not dağılımını belirleyen kurallar
- En az 20 otomatik test (tek komutla, ör. `pytest`), en az 2 test seviyesi (unit + API/E2E)
- Görünür şekilde en az 2 test tasarım tekniği (EP, BVA, karar tablosu, durum geçişi)
- En az 1 yapay zekâ öğesi, doğrulama kanıtıyla birlikte (A–H)
- Puanlama: Test tasarımı 20, Otomasyon 20, AI öğesi 25, Eleştirel değerlendirme 20, Rapor 10, Kilometre taşları 5
- "Mütevazı bir AI öğesi + dürüst değerlendirme" iddialı ama sorgulanmamış bir öğeden daha yüksek puan alır
- Rapor 8–12 sayfa, şablona birebir uyacak. Repo linki + PDF teslim edilecek.

## Strateji
- Dağıtım turlarla yapılıyor. 1. tercihte başkasıyla çakışırsan kura çekiliyor; kaybedersen 2. tercihin büyük ihtimalle başkasının 1. tercihi olarak çoktan gitmiş oluyor.
- **OWN (kendi önerin) hiç çakışmaz**, yazıldığı turda atanır (hoca onayıyla). Listenin başına iyi bir OWN koymak konuyu garantiler.
- Popüler görünen konular: 1 (TodoMVC), 3 (SauceDemo), 8/30/31 (LLM chatbot), 7, 24. Bunları üst sıralara koymak risklidir.
- Kendi yazdığın sistemler (spesifikasyonu ve hataları sen kontrol edersin) karar tablosu, BVA ve mutasyon analizini net göstermeye en uygun olanlar.

## OWN önerisi: Türk bordro (maaş) hesaplayıcısı
Forma yazılacak cümle:
> A Turkish payroll calculator I write (gross-to-net salary with SGK premiums, income tax brackets, stamp tax and minimum wage exemption), tested with boundary value and decision table techniques at unit and API level, where I compare LLM-generated tests against my own hand-written tests using mutation testing (mutmut) to measure which suite catches more planted bugs.

Neden iyi puan alır:
- Vergi dilimleri doğal sınır değerleri (BVA), kesinti kombinasyonları da doğal karar tabloları
- AI öğesi (A) ölçülebilir: LLM testleri ve benim testlerim → mutasyon skoru, kabul/ret tablosu
- Kimseyle çakışmaz (OWN), gerçek hayatta karşılığı olan bir problem
- Seviyeler: unit (pytest) + API (FastAPI + httpx/TestClient), ileride isteğe bağlı Playwright formu

## Önerilen sıralama
1. **OWN**: Bordro hesaplayıcı (yukarıdaki cümle)
2. **35**: Kendi yazdığın alışveriş sepeti ve indirim motoru, A: LLM ile üretilen karar tablosu testleri, doğrulanmış
3. **37**: Ders kayıt kuralları motoru (ön koşul, kontenjan, çakışma), A: yazılı gereksinimlerden LLM testleri
4. **20**: FastAPI/Flask ile küçük REST API, A: OpenAPI'den LLM testleri + mutasyon analizi
5. **42**: Tarih/saat yardımcı kütüphanesi (saat dilimi, artık yıl, tatiller), G: LLM ile uç durum tarihleri
