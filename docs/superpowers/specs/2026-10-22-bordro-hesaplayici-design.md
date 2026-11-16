# Tasarım: Türk Bordro Hesaplayıcısı ve Yapay Zekâ Destekli Test Takımı

- **Ders:** CMPE 411, AI-Driven Software Testing and QA (Güz 2026, İstanbul Bilgi Üniversitesi)
- **Öğrenci:** Emre Sülün. Konu OWN, 22 Ekim 2026'da onaylandı.
- **Tarih:** 22 Ekim 2026
- **İlgili belgeler:** `Proje/Mevzuat_2026.md` (2026 parametreleri ve kaynakları), `Hafta_04/Donem_Projesi/Project_Brief.pdf`, `Project_Report_Template.docx`, `Example_Project_Report.pdf`, `Hafta_05/CMPE 411 Week 5.pdf`

---

## 1. Amaç ve neden

Proje, dersin dönem projesi (notun %20'si). Projenin iki parçası var:

1. **Test edilen uygulama:** Türkiye'de 2026 yılı için brüt maaştan net maaşı hesaplayan küçük bir web uygulaması. Zam ve ikramiyeler dahil 12 ayı hesaplıyor.
2. **Projenin asıl ürünü, test takımı ve deney:** Uygulama için yazılmış otomatik testler, bir de şu soruyu sayılarla cevaplayan bir deney: *"Bir insanın gereksinimden tasarladığı testler mi, LLM'in ürettiği testler mi daha çok hata yakalar? LLM nerede yardım eder, nerede yanıltır?"*

Bordro seçildi çünkü:
- Kuralları resmî ve doğrulanabilir (GİB, SGK). Testlerin "doğru cevabı" (oracle) tartışmasız bir kaynaktan geliyor.
- Doğal sınır değerleri (vergi dilimleri, SGK tavanı, asgari ücret), karar tabloları ve durum geçişleri (aylar ilerledikçe dilim değişimi) içeriyor.
- LLM'i yanıltabilecek tuzakları var: ücret ve ücret dışı tarifelerin farklı olması, kümülatif matrah, yıl içinde değişen asgari ücret istisnası, 2026'da 7,5 kattan 9 kata çıkan SGK tavanı.

**Başarı:** Notlandırmanın her kriterinde tam puana yakın bir sonuç (bkz. §9). Kullanıcı ayrıca kodun her satırını hocaya rahatça anlatabilecek.

## 2. Hedefler, kapsam dışı olanlar ve kesinlikle olmaması gerekenler

**Hedefler**
- Brief'in tüm zorunlu şartlarını karşılamak: ≥20 otomatik test ve tek komutla çalışması; ≥2 test seviyesi (planlanan 3); ≥2 tasarım tekniği (planlanan 4); ≥1 AI öğesi (A) ve doğrulama kanıtı; 5 dakikada kurulup çalışan README.
- Hocanın örnek raporunun "iki haftam daha olsaydı" dediği iki şeyi yapmak: mutasyon testini araçla otomatikleştirmek ve API testi eklemek.
- Week 5 slaytlarındaki iyi uygulamaları görünür şekilde uygulamak: önce spesifikasyon; önce plan sonra kod; üret, çalıştır, ölç, gözden geçir, iyileştir döngüsü; tutulan/reddedilen test günlüğü.
- Kullanıcının raporu şablona birebir uygun yazabileceği tüm ham veriyi (tablolar, sayılar, örnekler) üretmek.

**Kapsam dışı (bilinçli sadeleştirmeler, raporda "known limitations" olarak yazılacak)**
- Devreden SGK matrahı (tavanı aşan ikramiyenin sonraki 2 aya devri). Tavanı aşan kısım SGK'ya tabi tutulmaz ve devredilmez.
- Engellilik indirimi, emekli (SGDP) çalışan, teşvikler, BES, yemek/yol istisnaları, kamu sektörü, kısmi süreli çalışma, eksik gün.
- 2026 dışındaki yıllar. Parametreler tek bir dosyada tutulur ama çok yıllı destek yazılmaz.
- İşveren maliyeti hesabı.
- Veritabanı, kullanıcı girişi, Docker, React gibi bir frontend framework'ü.

**Olmaması gerekenler (kullanıcının açık isteği)**
- **Hocaya anlatılamayacak kadar karmaşık kod.** Bu, tasarımın her kararını bağlar (bkz. §6).
- "LLM ile LLM'i karşılaştırmak": İnsan tarafı testlerin tasarımı (değerler ve beklenen sonuçlar) gerçekten kullanıcıdan gelmeli (bkz. §7).

## 3. Kısıtlar

- **Teslim:** GitHub (veya GitLab) repo linki ve 8–12 sayfalık PDF rapor; rapor şablonu birebir uygulanır. Son tarihten önceki son commit notlanır. Geç teslimde günde 10 puan kesilir.
- **Ara teslimler:**
  - 30 Ekim 23:59: Plan paragrafı (Project Plan formu, https://forms.gle/hq2GNUpRdoUsFQ6N9). OWN sahipleri AI öğesini açıkça yazmalı.
  - 20 Kasım (Lab 3): En az 10 çalışan test gösterilecek (notsuz).
  - 11 Aralık 23:59: Final.
- **Bütünlük kuralları:** AI kullanımı raporun AI usage statement bölümünde beyan edilir. Öğrenci her parçayı açıklayabilmeli; hoca kısa görüşmede kodu anlattırabilir.
- **AI kullanım beyanı (kullanıcının kuralı):** Beyana girecek her metin önce kullanıcıya gösterilir ve onaylanmadan hiçbir dosyaya eklenmez.
- **Ortam:** Kullanıcı Windows 11 kullanıyor, Python 3.11 kurulu. Python biliyor, yazılım testine yeni.
- **Gizlilik:** LLM'e gerçek kişisel veri gönderilmez (Week 5, slayt 37–39). Zaten gerçek bordro verisi kullanılmıyor; tüm girdiler kurgusal.

## 4. Uygulama: davranış

### 4.1 Girdiler (kurallarla giriş, kullanıcının seçimi)
- **Ocak brüt maaşı** (TL, kuruşlu).
- **Zam kuralları** listesi; her biri `(ay, oran %)`. Örnek: "Temmuz'dan itibaren %30". Zam ayı **2–12** arasında olmalı; Ocak'a zam girilemez, çünkü Ocak maaşı zaten girdinin kendisi. Zam o aydan itibaren o anki maaşa uygulanır. Birden fazla zam bileşik etki yapar. **Her zamdan sonra maaş kuruşa yuvarlanır** (`ROUND_HALF_UP`), zamlar ay sırasıyla uygulanır. Örnek: Temmuz %30, sonra Ekim %10 → Temmuz maaşı = yuvarla(Ocak × 1,30), Ekim maaşı = yuvarla(Temmuz maaşı × 1,10).
- **İkramiye** listesi; her biri `(ay, tutar TL)`. Aynı aya birden fazla ikramiye girilirse toplanır.

### 4.2 Doğrulama kuralları (EP/BVA testlerinin kaynağı)
- Ocak brüt maaşı ≥ 33.030,00 TL (brüt asgari ücret) olmalı. 33.029,99 reddedilir.
- Ocak brüt maaşı ≤ 10.000.000,00 TL (makul üst sınır; benim kararım).
- Ay 1–12 arasında bir tam sayı olmalı (ikramiye için 1–12, zam için 2–12).
- Zam oranı 0'dan büyük ve ≤ 100 olmalı (indirim/negatif zam yok; benim kararım).
- Aynı aya iki zam girilemez; doğrulama hatası verir.
- İkramiye tutarı > 0 olmalı.
- Tutarlar en fazla 2 ondalık basamaklı olmalı.
- Geçersiz girdide: Hesap motoru `ValueError` (Türkçe mesajla) fırlatır; API 422 döner; sayfa hatayı kullanıcıya gösterir.

### 4.3 Aylık hesap (m = 1..12, sırayla)
Parametreler `Mevzuat_2026.md`'den gelir. Formüller:

```
toplam_brut_m   = maas_m + ikramiye_m
sgk_matrahi_m   = min(toplam_brut_m, 297.270,00)            # SGK tavanı
sgk_isci_m      = sgk_matrahi_m × 0,14
issizlik_m      = sgk_matrahi_m × 0,01
gv_matrahi_m    = toplam_brut_m − sgk_isci_m − issizlik_m
kum_m           = kum_{m−1} + gv_matrahi_m                  # kum_0 = 0
hesaplanan_gv_m = T(kum_m) − T(kum_{m−1})                   # T = ücret tarifesi, kümülatif
au_istisna_m    = T(28.075,50 × m) − T(28.075,50 × (m−1))    # asgari ücretin GV'si
gelir_vergisi_m = max(0, hesaplanan_gv_m − au_istisna_m)
damga_m         = max(0, toplam_brut_m × 0,00759 − 250,70)
net_m           = toplam_brut_m − sgk_isci_m − issizlik_m − gelir_vergisi_m − damga_m
```

- **T(x):** GVK 103 **ücret** tarifesi (0–190.000 %15; –400.000 %20; –1.500.000 %27; –5.300.000 %35; üstü %40). Ücret dışı tarife (3. dilim 1.000.000) bilinçli olarak kullanılmaz.
- **Yuvarlama (benim kararım):** Her kalem (`sgk_isci`, `issizlik`, `hesaplanan_gv`, `au_istisna`, `damga`) kuruşa yuvarlanır (`Decimal`, `ROUND_HALF_UP`). Kümülatif matrah yuvarlanmış kalemlerden hesaplanır. Doğrulama: Ocak istisnası 4.211,325 → 4.211,33 olur ve bu, ikincil kaynaklardaki rakamla aynı.
- **Kontrol değerleri** (asgari ücretli çalışan için tasarımın kendi tutarlılık testi): Her ay net = 28.075,50, gelir vergisi = 0, damga = 0. İstisna tutarları Ocak–Haziran 4.211,33, Temmuz 4.537,75, Ağustos–Aralık 5.615,10.

### 4.4 Çıktı (aylık)
Her ay için: `ay, maas, ikramiye, toplam_brut, sgk_isci, issizlik, gv_matrahi, kumulatif_matrah, hesaplanan_gv, au_istisna, gelir_vergisi, damga, net, dilimler, baslangic_orani, dilim_degisti`. Ayrıca yıllık toplamlar: toplam brüt, toplam net, toplam gelir vergisi, toplam SGK.

**Dilim tanımları (kesin):**
- **Sınır noktası alt dilime aittir.** Tarife "190.000 TL'ye kadar %15" dediği için kümülatif matrah tam 190.000,00 ise %15 dilimindedir; 190.000,01 ise %20. Aynı kural 400.000 / 1.500.000 / 5.300.000 için de geçerli. `oran(x)` fonksiyonu bu kuralı uygular: `x ≤ 190.000 → 15`, `x ≤ 400.000 → 20`, …
- **`dilimler`:** Bu ayın matrah diliminin (`kum_{m−1}`, `kum_m`] aralığının içinden geçtiği, **pozitif tutarlı** oranların artan listesi. Örnek: kum 168.453 → 196.528,50 ise `[15, 20]`; tamamı tek dilimdeyse `[20]`.
- **`baslangic_orani`:** `oran(kum_{m−1})`; Ocak için `kum_0 = 0` olduğundan 15.
- **`dilim_degisti`:** `max(dilimler) > baslangic_orani`. Bu tek kural üç durumu da kapsar:
  - (a) ay içinde sınır geçişi;
  - (b) önceki ay tam sınırda bitti ve bu ayın tamamı üst dilimde;
  - (c) Ocak'ta yüksek maaşla [15, 20] gibi bir geçiş, yani Ocak'ta da `true` olabilir.
- **Uyarı metni:** `dilim_degisti` true ise "Bu ay %{baslangic} diliminden %{max(dilimler)} dilimine geçtiniz". Birden fazla dilim atlandıysa ara oranlar da listelenir: "(%20 → %27 → %35)".
- Not: T(x) sürekli olduğu için sınır noktasının hangi dilime ait olduğu vergi tutarını değiştirmez; sadece `dilimler` / `baslangic_orani` / `dilim_degisti` alanlarını değiştirir. Sınır değer testleri ve yerleştirilmiş `<` / `<=` hatası bu alanlar üzerinden yakalanır.

## 5. Uygulama: arayüz (kullanıcının seçimi: B düzeni + C'nin yıllık fikri)

Onaylanan taslak: `Proje/.superpowers/brainstorm/.../content/layout-v2.html` ve `inputs-v3.html` (A seçeneği).

- **Sol sütun:** Ocak brüt maaşı; "+ zam ekle" satırları (ay seçici + %); "+ ikramiye ekle" satırları (ay seçici + TL); her satırda ✕ ile silme; **Hesapla** butonu.
- **Sağ sütun (seçili ay, varsayılan Ocak):**
  - Büyük puntoyla net maaş.
  - Brütün bölündüğü renkli yatay çubuk: Net / SGK+işsizlik / Gelir vergisi / Damga, yüzdeleriyle.
  - Kalem kalem kesinti listesi.
  - `dilim_degisti` true ise uyarı: "Bu ay %15 diliminden %20 dilimine geçtiniz…"
- **Alt kısım:** 12 aylık sütun grafiği. Her sütun net maaşı gösterir, ikramiyeden kalan net ayrı renkte üst üste. Bir sütuna tıklamak üst kısmı o aya geçirir. Altında yıllık toplamlar.
- **Uygulama:** Düz HTML + CSS + tek bir `app.js`. Grafik bir kütüphane olmadan, `div`'lerle çizilir. Sayılar Türkçe biçimde gösterilir (`38.280,00 TL`). Sayfa FastAPI tarafından statik dosya olarak sunulur ve `POST /api/hesapla`'ya JSON gönderir.
- **Erişilebilir öğeler:** Playwright testleri `get_by_role` / `get_by_label` ile bulabilsin diye her girdinin `<label>`'ı olur; butonların metni vardır; önemli çıktı alanlarında `data-testid` bulunur.

## 6. Mimari ve kod kuralları ("anlatılabilir kod")

```
bordro-test/                       ← GitHub reposu
├── bordro/
│   ├── parametreler.py            ← 2026 sabitleri (Decimal); her birinin yanında kaynak yorumu
│   ├── tarife.py                  ← T(x): kümülatif gelir vergisi fonksiyonu
│   ├── kurallar.py                ← zam/ikramiye kuralları → 12 aylık maaş+ikramiye; doğrulama
│   └── hesap.py                   ← aylık hesap ve yıllık hesap (bordro_hesapla)
├── api.py                         ← FastAPI: POST /api/hesapla + statik dosyalar
├── static/ index.html, app.js, style.css
├── tests/
│   ├── unit/                      ← insan tasarımı unit testler (tablolardan)
│   ├── api/                       ← API testleri (FastAPI TestClient)
│   ├── e2e/                       ← Playwright testleri
│   └── llm/                       ← LLM'in ürettiği testler (deney sonrası tutulanlar)
├── ai/
│   ├── prompts/                   ← kullanılan istemler (sürümlü)
│   ├── outputs/                   ← LLM ham çıktıları (her çalıştırma ayrı dosya)
│   ├── generate_tests.py          ← istemi gönderir, cevabı kaydeder
│   └── review_log.md              ← her LLM testi için: tut / düzelt / reddet + gerekçe
├── deney/
│   ├── hatali_surum/              ← bilerek hata yerleştirilmiş kopya (bkz. §7.4)
│   └── sonuclar/                  ← coverage, mutasyon ve hata yakalama tabloları
├── docs/
│   ├── test_tasarimi/             ← kullanıcının doldurduğu EP/BVA/karar tablosu/durum tabloları
│   └── anlatim/                   ← her modül için "hoca sorarsa nasıl anlatırım" notları
├── requirements.txt, pytest.ini, README.md
└── .github/workflows/tests.yml    ← her push'ta testler (+ mutasyon)
```

**Kod kuralları**
- Sınıf hiyerarşisi yok; düz fonksiyonlar ve gerektiğinde `dataclass` (aylık sonuç için). Fonksiyonlar ≈30 satırı geçmez.
- İsimler bordro terimleriyle aynı; ASCII Türkçe (`sgk_isci_payi`, `kumulatif_matrah`, `asgari_ucret_istisnasi`).
- Para hesapları sadece `Decimal` ile yapılır, `float` yasak. API sınırında string/Decimal dönüşümü yapılır.
- Her sabit `parametreler.py`'de tanımlıdır ve kaynağı yanında yazar; başka hiçbir dosyada "sihirli sayı" olmaz.
- Docstring'ler kuralı düz dille anlatır; LLM deneyinde "spesifikasyon" olarak bunlar ve `Mevzuat_2026.md` kullanılır.
- Bağımlılıklar az: `fastapi`, `uvicorn`, `pytest`, `pytest-cov`, `httpx`, `pytest-playwright`, mutasyon aracı, LLM SDK'sı.

## 7. Test stratejisi ve AI deneyi

### 7.1 İş bölümü (kullanıcının onayladığı)
- **Claude yazar ve satır satır anlatır:** Uygulamanın tamamı, API, sayfa, AI betiği, deney altyapısı, uçtan uca ve API testleri, hatalı sürüm.
- **Kullanıcı tasarlar:** İnsan tarafı unit testlerin **değerleri ve beklenen sonuçları**. Bunları `Mevzuat_2026.md` ve hesap makinesiyle kendisi hesaplar, `docs/test_tasarimi/` altındaki tablolara yazar. Claude teknikleri örnekle öğretir ve tabloları `pytest.mark.parametrize` koduna çevirir; bu çeviri mekaniktir ve değerleri değiştirmez.
- **Sıra önemli:** Kullanıcı tablolarını LLM çıktılarını görmeden ve hatalı sürümdeki hataları bilmeden tamamlar. Böylece karşılaştırma kirlenmez. Hatalar kullanıcı tablolarını bitirdikten sonra yerleştirilir (ya da kullanıcı listeye bakmaz).

### 7.2 Test seviyeleri
| Seviye | Araç | Ne test eder |
|---|---|---|
| Unit | pytest + parametrize | `tarife.py`, `kurallar.py`, `hesap.py` |
| API | FastAPI TestClient (httpx) | `POST /api/hesapla`: geçerli/geçersiz girdi, 422, JSON şekli |
| Uçtan uca | pytest-playwright (Chromium) | Sayfayı aç, girdi gir, Hesapla, net/uyarı/grafik/ay seçimi; doğrulama hatası mesajı |

Hedef: ≥40 test (≥25 unit, ≥8 API, ≥6 e2e). Hepsi `pytest` ile tek komutla çalışır. E2E testleri sunucuyu bir fixture ile kendisi başlatır.

### 7.3 Test tasarım teknikleri (dördü de görünür şekilde)
| Teknik | Nerede | Örnek |
|---|---|---|
| Sınır değer (BVA) | Vergi dilim sınırları (kümülatif 190.000 / 400.000 / 1.500.000 / 5.300.000 civarı), SGK tavanı (297.269,99 / 297.270,00 / 297.270,01), asgari ücret alt sınırı (33.029,99 / 33.030,00), zam oranı (0 / 0,01 / 100 / 100,01) | |
| Denklik sınıfları (EP) | Geçerli/geçersiz brüt, ay, zam, ikramiye | |
| Karar tablosu | Bir ayın sonucu: {ikramiye var mı} × {SGK tavanı aşılıyor mu} × {bu ay dilim değişiyor mu} × {istisna dönemi: Oca–Haz / Tem / Ağu–Ara}. Not: "GV istisnayı aşıyor mu" koşulu bilinçli olarak kullanılmadı. Girdiler en az asgari ücret olduğu için bu koşul sadece tam asgari ücrette eşitlik olarak oluşur; kombinasyonların yarısı imkânsız kalırdı. Asgari ücret eşitlik durumu ayrı bir sınır değer testi olarak yer alır. | |
| Durum geçişi | Aylar ilerledikçe dilim durumu: %15 → %20 → %27 → %35 → %40; bir ayda iki dilim atlama (büyük ikramiye) | |

Her test adı ya da açıklaması dayandığı kuralı (`Mevzuat_2026.md` bölümünü) söyler. Rapordaki "Requirement / Technique / Test values / Test function" tablosu bundan üretilir.

### 7.4 AI öğesi (Seçenek A: LLM ile üretilen testler, doğrulanmış)

**Araç:** `ai/generate_tests.py` istemi dosyadan okur, LLM API'sine gönderir, ham cevabı `ai/outputs/<deney>_<n>.md` olarak kaydeder (model adı, ayarlar ve zaman damgasıyla). Varsayılan sağlayıcı Anthropic Claude API; model ID'si plan aşamasında güncel dokümantasyondan seçilir ve sabitlenir. API anahtarını kullanıcı kendisi oluşturur ve ortam değişkeni olarak verir; anahtar repoya girmez. Kullanıcı API'ye ücret ödemek istemezse yedek yol şu: aynı istemler sohbet arayüzüne elle yapıştırılır ve cevaplar aynı klasöre aynı adlandırmayla kaydedilir.

**İstem tasarımı (Week 5, slayt 9–12, 27):** Rol + bağlam (kurallar kelimesi kelimesine) + teknik (BVA/EP/karar tablosu) + çıktı biçimi (pytest, parametrize, gerçek fonksiyon adları) + kısıt ("beklenen değerleri sadece kurallardan türet; her assert somut bir değerle karşılaştırsın"). İki aşama: önce LLM'den test **tablosu**, sonra kod.

**Deneyler:**
| Deney | LLM'e verilen | Amaç |
|---|---|---|
| D1: sadece spesifikasyon | Kurallar + fonksiyon imzaları | Doğruluk testleri üretebiliyor mu? |
| D2: spesifikasyon + kod | Kurallar + **hatalı sürümün** kodu | Hatalı davranışı "doğru" sanıp kopyalıyor mu? (slayt 15) |
| D3: geri bildirimli tur | D1 + coverage/mutasyon raporu ("şu satırlar test edilmiyor") | İyileştirme döngüsü işe yarıyor mu? (slayt 18) |

- Her deney **3 kez** çalıştırılır; aynı istemin farklı çıktılar verdiği ölçülür (slayt 5).
- **Yerleştirilmiş hatalar:** ≈6–8 gerçekçi hata. Örnekler: `<=` yerine `<` dilim sınırı; ücret dışı tarifenin 1.000.000 sınırı; SGK tavanının eski 7,5 katı; istisnanın kümülatif değil sabit hesaplanması; damga istisnasının unutulması; zam sonrası yuvarlama hatası.
  - **Her hata ayrı bir varyanttır** (`deney/hatali_surum/H1/ … H8/`; her biri doğru koddan tek bir değişiklikle ayrılır). Böylece hatalar birbirini maskelemez ve "hangi grup hangi hatayı yakaladı" temiz sayılır.
  - **Yakalama tanımı:** Bir test grubu bir varyantı, doğru kodda tamamen geçip o varyantta en az bir testi kalırsa "yakalamış" sayılır.
  - **D2 için ayrıca birleşik kopya** (`deney/hatali_surum/birlesik/`): Tüm hatalar tek kodda. LLM'e bu verilir (3 çalıştırma). Gerçekçi senaryo budur: geliştirici LLM'e "kodum bu" der.
  - **Kopyalanmış hata tanımı:** Doğru kodda kalan ama ilgili hatalı varyantta geçen test. Yani test, hatanın davranışını "doğru" diye bekliyor.
  - Liste `deney/hatali_surum/HATALAR.md`'de saklanır ve LLM'e asla verilmez.

**Filtre hattı (Week 5, slayt 19–22, Meta yaklaşımı):** Her LLM testi sırayla şu adımlardan geçer: (1) çalışıyor mu (import/sözdizimi), (2) doğru kodda 5 tekrarda tutarlı geçiyor mu, (3) coverage/mutasyon skoruna katkısı var mı, (4) insan incelemesi: beklenen değer kurala uyuyor mu? Sonuç `ai/review_log.md`'ye yazılır: Tut / Düzelt / Reddet / Sor ve gerekçe; reddetme nedenleri slayt 20'deki kategorilerle etiketlenir (uydurulmuş API, kopyalanmış hata, boş assert, tekrar, uydurulmuş kural). İnceleme kararlarını kullanıcı verir, Claude gerekçeleri tartışmasında yardım eder.

### 7.5 Ölçümler (rapor §6 ve §7 için)
**Karşılaştırma grupları (kesin tanım):**
- **İnsan:** Yalnızca kullanıcının tasarladığı unit testler (`tests/unit/`). Claude'un yazdığı API ve e2e testleri hiçbir karşılaştırma grubuna girmez; "altyapı testleri" olarak ayrı raporlanır.
- **LLM (ham):** Bir deneyin bir çalıştırmasının çalışabilen tüm testleri, değiştirilmeden.
- **LLM (tutulan):** İnsan incelemesinde "Tut" alanlar. "Düzelt" alanlar ayrı bir sütunda raporlanır (LLM fikri + insan düzeltmesi) ve "tutulan" sayısına katılmaz. Böylece LLM'e haksız puan verilmez.
- **Birlikte:** İnsan + LLM (tutulan).
- Sayılar **her deney için ayrı** (D1, D2, D3; her birinde 3 çalıştırmanın ortalaması ± min/max) ve ayrıca **D1 ∪ D3 tutulanların birleşimi** olarak verilir. D2 bir "tuzak deneyi" olduğu için birleşime katılmaz; kendi kopyalanmış hata sayısıyla raporlanır.
- **Ölçüm kapsamı:** Coverage ve mutasyon yalnızca `bordro/` paketi üzerinde ölçülür. LLM testleri unit seviyesinde üretildiği için adil karşılaştırma budur. `api.py` ayrıca altyapı testleriyle ölçülür.

Her grup için:
- Test sayısı (üretilen / çalışan / tutulan)
- Satır ve dal (branch) kapsamı (`pytest-cov`)
- Mutasyon skoru (öldürülen / toplam mutant) doğru kod üzerinde
- Hatalı sürümdeki yerleştirilmiş hatalardan kaçını yakaladığı
- D2'de "hatayı bekleyen" (kopyalanmış hata) test sayısı
- Çalıştırmalar arası değişkenlik (3 tekrarın farkı)
- Dilim/tarife tuzaklarına düşme örnekleri

**Mutasyon aracı:** mutmut. Not: Güncel mutmut sürümlerinin Windows'ta doğrudan çalışmadığı biliniyor; mutasyon testi GitHub Actions (Linux) ya da WSL'de çalıştırılır. Plan aşamasında doğrulanacak; mutmut uygun olmazsa yedek cosmic-ray (Windows'ta çalışır). Plan paragrafında mutmut yazıldığı için tercih mutmut.

## 8. Teslimler ve takvim

| Tarih | Teslim | Sorumlu |
|---|---|---|
| 30 Ekim 23:59 | Plan paragrafı (form). Taslağı Claude yazar, kullanıcı onaylayıp kendisi gönderir. | Kullanıcı gönderir |
| ~Kasım ilk haftası | Uygulama çekirdeği + parametreler + ilk unit testler; kullanıcı test tasarım tablolarına başlar | Birlikte |
| 20 Kasım (Lab 3) | ≥10 çalışan test gösterilir (hedef: çekirdek unit + birkaç API testi) | Kullanıcı gösterir |
| Kasım sonu | API + sayfa + e2e; AI deneyleri D1–D3; ölçümler | Birlikte |
| Aralık ilk haftası | Rapor (şablona göre); README; son temizlik | Kullanıcı yazar, Claude destekler |
| 11 Aralık 23:59 | Repo linki + PDF rapor (Learn) | Kullanıcı gönderir |

Not: Vize Week 5'ten yaklaşık iki hafta sonra (Kasım başı). O hafta proje temposu düşürülebilir.

**Plan paragrafı taslağı (kullanıcı onayına sunulacak):**
> I will write a Turkish payroll calculator in Python that computes the monthly gross-to-net salary for 2026 (SGK and unemployment premiums with the SGK ceiling, cumulative income tax brackets for wage income, the minimum wage tax exemption and stamp tax), with raises and bonuses entered as rules, and a small web page that shows the result for each month of the year. I will test it at three levels: unit tests with pytest for the calculation rules, API tests for a FastAPI endpoint, and end-to-end tests with Playwright on the web page. I will design the tests with boundary value analysis (tax bracket limits, the SGK ceiling, the minimum wage), equivalence partitioning (valid and invalid inputs), a decision table (bonus, ceiling, bracket change, exemption) and state transition (moving through tax brackets during the year). As the AI element (option A), I will ask an LLM to generate tests from the written rules, review every expected value against the official 2026 parameters, and compare the generated suite with my own tests using coverage, mutation testing (mutmut) and a version of the code with planted defects, including an experiment where the LLM also sees the code.

## 9. Notlandırmaya eşleme

| Kriter (puan) | Tasarımdaki karşılığı |
|---|---|
| Test tasarımı (20) | 4 teknik; kullanıcının tabloları; her test bir kurala bağlı |
| Otomasyon kalitesi (20) | Tek komut; bağımsız testler; rol/label tabanlı locator'lar; CI; 5 dakikalık README |
| AI öğesi (25) | Tekrarlanabilir betik; sürümlü istemler; ham çıktılar; 3 deney × 3 tekrar |
| Eleştirel değerlendirme (20) | Filtre hattı; review log; kopyalanmış hata ölçümü; mutasyon ve yerleştirilmiş hata karşılaştırması; "AI'ya neyi emanet etmem" bölümü |
| Rapor (10) | Şablon başlıkları; numaralı tablo ve şekiller; rapor dili İngilizce (ders dili) |
| Kilometre taşları (5) | 21 Ekim ✓; 30 Ekim plan; 20 Kasım ≥10 test |

## 10. Uygulayıcıya bırakılanlar
- Kesin model ID'si ve LLM ayarları (güncel API dokümantasyonuna göre).
- CSS ayrıntıları ve renk paleti (taslaktaki düzene sadık kalmak şartıyla).
- Test dosyalarının ayrıntılı bölünmesi; fixture yapısı.
- Hatalı sürümdeki hataların kesin listesi (§7.4'teki örneklere benzer, gerçekçi hatalar).
- Mutmut yapılandırması ve CI iş akışının ayrıntıları.

## 11. Benim kararlarım (kullanıcının gözden geçirmesi için)
1. Kapsam dışı bırakılanlar (§2). En önemlisi devreden SGK matrahı.
2. Zamlar sadece yüzde olarak girilir, Şubat–Aralık aylarına uygulanır, bileşik etki yapar ve her zamdan sonra maaş kuruşa yuvarlanır. Aynı aya iki zam hata verir; aynı aydaki ikramiyeler toplanır.
2b. Dilim sınır noktası alt dilime aittir; `dilim_degisti = max(dilimler) > baslangic_orani` (§4.4).
2c. Karşılaştırma grupları ve ölçüm kapsamı §7.5'teki gibi: "İnsan" sadece kullanıcının unit testleri; "Düzelt" alanlar LLM sayılmaz; ölçüm sadece `bordro/` üzerinde.
2d. Her yerleştirilmiş hata ayrı varyant; D2'ye birleşik kopya verilir.
3. Brüt üst sınırı 10.000.000 TL; zam oranı 0 < oran ≤ 100.
4. Her kalem kuruşa `ROUND_HALF_UP` ile yuvarlanır.
5. Arayüz düz HTML/JS, grafik kütüphanesiz; sunucu FastAPI.
6. Üç test seviyesi (unit + API + e2e).
7. Varsayılan LLM Claude API; yedek yol elle sohbet.
8. Mutasyon testi Linux'ta (CI/WSL) çalışır.
9. Rapor dili İngilizce.
