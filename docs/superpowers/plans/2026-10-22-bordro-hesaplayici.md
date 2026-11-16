# Bordro Hesaplayıcı ve AI Destekli Test Takımı: Uygulama Planı

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 2026 Türk bordrosunu (zam ve ikramiye dahil 12 ay) hesaplayan bir FastAPI + düz HTML uygulaması kurmak. Bunun üstüne insan tasarımı testlerle LLM üretimi testleri coverage, mutasyon ve yerleştirilmiş hatalarla karşılaştıran bir deney altyapısı kurmak.

**Architecture:**
- **Hesap motoru:** `bordro/` paketi, saf Python fonksiyonları ve `Decimal` ile çalışır.
- **API:** `api.py` motoru `POST /api/hesapla` ile sunar ve `static/` sayfasını servis eder.
- **AI deneyi:** `ai/` (istem gönderme, filtre) ve `deney/` (hatalı varyantlar, ölçüm) altında, uygulamadan ayrı duran betikler.

**Tech Stack:** Python 3.11, FastAPI, uvicorn, pytest, pytest-cov, httpx, pytest-playwright (Chromium), mutmut (WSL/Linux), anthropic SDK (`claude-opus-5-5`), düz HTML/CSS/JS.

**Spec:** `docs/superpowers/specs/2026-10-22-bordro-hesaplayici-design.md`. Kural kaynağı: `docs/Mevzuat_2026.md`.

## Global Constraints

- Repo kökü `E:\CMPE411\Proje`. GitHub reposu `emrs6/bordro-test`; görünürlüğü (public/private) kullanıcı seçer.
- Python 3.11.9, sanal ortam `.venv`. Komutlar Windows'ta `.venv\Scripts\python -m pytest`; mutasyon ise WSL Ubuntu'da çalışır.
- Para değerleri yalnızca `decimal.Decimal`; `float` kullanmak yasak. Yuvarlama `kurus(x) = x.quantize(Decimal("0.01"), ROUND_HALF_UP)`.
- Tüm 2026 sabitleri yalnızca `bordro/parametreler.py`'de tanımlıdır ve her birinin yanında kaynak yorumu bulunur:
  - `ASGARI_UCRET_BRUT=33030.00`
  - `SGK_TAVAN=297270.00`
  - `SGK_ISCI_ORANI=0.14`
  - `ISSIZLIK_ISCI_ORANI=0.01`
  - `DAMGA_ORANI=0.00759`
  - `DAMGA_ISTISNASI=250.70`
  - `ASGARI_UCRET_GV_MATRAHI=28075.50`
  - `BRUT_UST_SINIR=10000000.00`
  - Ücret tarifesi: 190.000 %15 / 400.000 %20 / 1.500.000 %27 / 5.300.000 %35 / üstü %40
- Dilim sınır noktası alt dilime aittir (`x ≤ 190000 → 15`).
- Kod kuralları:
  - Sınıf hiyerarşisi yok; yalnızca düz fonksiyon ve `@dataclass`.
  - Fonksiyonlar ≈30 satırı geçmez.
  - İsimler ASCII Türkçe bordro terimleri.
- Bağımlılıklar yalnızca şunlar: `fastapi uvicorn pytest pytest-cov httpx pytest-playwright mutmut anthropic`.
- Test klasörleri ve karşılaştırmadaki yerleri:
  - `tests/unit/`: İNSAN grubu. Yalnızca kullanıcının tablolarından üretilir.
  - `tests/gelistirici/`: Claude'un geliştirme testleri; spesifikasyondaki kontrol değerlerine dayanır. Karşılaştırma dışı.
  - `tests/api/`, `tests/e2e/`: Altyapı testleri. Karşılaştırma dışı.
  - `tests/llm/`: İncelemeden "Tut" alan LLM testleri.
- `pytest` repo kökünden tek komutla tüm testleri çalıştırır.
- **AI kullanım beyanı:** Beyana girecek her metin önce kullanıcıya gösterilir ve onayı olmadan hiçbir dosyaya yazılmaz.
- **Dış dünyaya dokunan işlemler kullanıcı onayı ister:** GitHub repo oluşturma/push, API'ye para harcayan çağrılar, form gönderimi (formu her zaman kullanıcı kendisi gönderir).
- **Gizli bilgi:** API anahtarı repoya girmez (`.env` `.gitignore`'da). Gerçek kişisel veri LLM'e gönderilmez.
- Her görevin sonunda Claude yazdığı kodu kullanıcıya satır satır anlatır ve `docs/anlatim/<modul>.md` notunu yazar ya da günceller.

## Review Focus

1. **Sayfada Türkçe sayı biçimi:** Kullanıcı `50.000` ya da `50.000,50` yazar. Nokta binlik ayırıcı, virgül ondalık ayırıcı olarak okunmalı. 50.000 TL'yi 50 TL sanmak en olası gerçek hata. Task 8'deki `test_turkce_sayi_bicimi` testi bunu sabitler.
2. **Eklenip boş bırakılan zam/ikramiye satırı:** Sayfa çökmemeli; ya satırı yok saymalı ya da Türkçe hata göstermeli. Karar: boş satır yok sayılır. Task 8'deki `test_bos_satir_yok_sayilir` testi.
3. **Tek ayda birden çok dilim atlayan dev ikramiye:** Örnek: Ocak'ta 6.000.000 TL ikramiye → `dilimler == [15, 20, 27, 35, 40]` ve uyarı ara oranları listeler. Task 2 ve Task 4'teki testler.
4. **API'ye JSON float ile sayı gelmesi** (`33030.1`): `Decimal(str(x))` ile tam okunmalı, ikili kayan nokta artığı taşımamalı. Task 6'daki `test_float_girdi_tam_okunur` testi.
5. **Aynı aya iki ikramiye** (toplanır) ve **Ocak'a zam** (reddedilir): Sessizce yanlış hesap yerine belirgin davranış. Task 3'teki testler.

---

## Aşama 0: Plan paragrafı (son tarih 30 Ekim 23:59)

### Task 0: Plan paragrafını onaylat, kullanıcı göndersin

**Files:** Yok (form).

- [ ] **Step 1:** Spec §8'deki İngilizce paragrafı kullanıcıya göster. Kullanıcının istediği düzeltmeleri yap; paragraf 3 test seviyesi, 4 tekniği ve AI öğesini (A, mutmut, yerleştirilmiş hatalar) açıkça içermeli.
- [ ] **Step 2:** Kullanıcı paragrafı https://forms.gle/hq2GNUpRdoUsFQ6N9 formuna **kendisi** gönderir. Claude göndermez. Gönderim onayının ekran görüntüsünü saklamasını hatırlat.
- [ ] **Step 3:** Gönderilen son metni `docs/plan_paragrafi.md` dosyasına kaydet (Task 1'den sonra commit edilir).

---

## Aşama 1: Hesap motoru (Lab 3 hedefi, 20 Kasım: ≥10 çalışan test)

### Task 1: Repo iskeleti

**Files:**
- Create: `.gitignore`, `requirements.txt`, `pytest.ini`, `pyproject.toml`, `README.md` (iskelet), `bordro/__init__.py`, `tests/gelistirici/test_iskelet.py`, `docs/gereksinimler.md`
- Move: `Konu_Secimi.md` → `docs/Konu_Secimi.md`; `Mevzuat_2026.md` → `docs/Mevzuat_2026.md`

**Interfaces:**
- Produces: `docs/gereksinimler.md` numaralı gereksinimler (R1…Rn). Hem kullanıcı hem LLM bu belgeden test türetir; testler R-numarasıyla izlenir.

- [ ] **Step 1:** `git init` (kök `E:\CMPE411\Proje`). Ardından:
  - `.gitignore` içeriği: `.venv/ __pycache__/ .pytest_cache/ .coverage htmlcov/ mutants/ .env .superpowers/ deney/gecici/`
  - `pytest.ini`: `testpaths = tests`, `addopts = -q`, marker `e2e`
  - `pyproject.toml`: yalnızca `[tool.mutmut] source_paths = ["bordro/"]`
- [ ] **Step 2:** `py -3.11 -m venv .venv`, `requirements.txt` (Global Constraints'teki 8 paket, sürümler kurulumda sabitlenir), `.venv\Scripts\pip install -r requirements.txt`, `.venv\Scripts\playwright install chromium`.
- [ ] **Step 3:** `docs/gereksinimler.md` dosyasını yaz. Spec §4.1–§4.4'ü numaralı, düz İngilizce kurallar olarak yazar. Örnek: "R3: The SGK base is the month's total gross capped at 297,270.00 TL." Doğrulama kuralları, aylık formüller, dilim tanımları (sınır alt dilime ait, `dilimler`, `baslangic_orani`, `dilim_degisti`) ve yuvarlama dahil olmalı. Kod içermez; LLM'e de aynen verilecek. Kullanıcıya okut ve onaylat.
- [ ] **Step 4:** Duman testi `tests/gelistirici/test_iskelet.py::test_paket_yuklenir` yaz (`import bordro`); `.venv\Scripts\python -m pytest` → 1 passed.
- [ ] **Step 5:** Commit: `chore: repo iskeleti, gereksinimler`.
- [ ] **Step 6:** Kullanıcıya sor: repo public mi private mı? Onaydan sonra `gh repo create emrs6/bordro-test --<secim> --source . --push`. Private seçilirse hocanın GitHub kullanıcı adı ileride collaborator olarak eklenir.

### Task 2: Parametreler ve kümülatif tarife

**Files:**
- Create: `bordro/parametreler.py`, `bordro/para.py`, `bordro/tarife.py`
- Test: `tests/gelistirici/test_tarife.py`

**Interfaces:**
- Produces:
  - `kurus(x: Decimal) -> Decimal` (`bordro/para.py`)
  - `kumulatif_vergi(matrah: Decimal) -> Decimal`: T(x), yuvarlamasız
  - `oran(matrah: Decimal) -> int`: sınır alt dilime ait; `oran(0) == 15`
  - `dilimler(onceki: Decimal, simdiki: Decimal) -> list[int]`: (onceki, simdiki] aralığında pozitif tutarlı oranlar, artan sırada
  - Tüm sabitler `bordro/parametreler.py`'de; tarife `UCRET_TARIFESI: list[tuple[Decimal | None, int]]` olarak tutulur

- [ ] **Step 1: Başarısız testleri yaz.** Değerler GİB tarifesinin kendi sabit tutarlarından geliyor:

```python
@pytest.mark.parametrize("matrah, vergi", [
    ("0", "0"), ("190000", "28500"), ("400000", "70500"),
    ("1500000", "367500"), ("5300000", "1697500"),
])
def test_tarife_sabit_tutarlari(matrah, vergi):
    assert kumulatif_vergi(D(matrah)) == D(vergi)

@pytest.mark.parametrize("matrah, beklenen", [
    ("190000", 15), ("190000.01", 20), ("400000", 20), ("5300000", 35), ("5300000.01", 40),
])
def test_sinir_alt_dilime_aittir(matrah, beklenen):
    assert oran(D(matrah)) == beklenen

def test_dilimler_tek_ayda_gecis():
    assert dilimler(D("168453.00"), D("196528.50")) == [15, 20]

def test_dilimler_tam_sinirda_biten_ay_tek_dilim():
    assert dilimler(D("161924.50"), D("190000.00")) == [15]

def test_dilimler_dev_ikramiye_tum_dilimler():
    assert dilimler(D("0"), D("6000000")) == [15, 20, 27, 35, 40]

def test_damga_istisnasi_asgari_ucretin_damgasidir():
    assert kurus(ASGARI_UCRET_BRUT * DAMGA_ORANI) == DAMGA_ISTISNASI
```

- [ ] **Step 2:** `.venv\Scripts\python -m pytest tests/gelistirici/test_tarife.py` → FAIL (ImportError).
- [ ] **Step 3:** Üç modülü yaz.
- [ ] **Step 4:** Aynı komut → hepsi PASS.
- [ ] **Step 5:** Kullanıcıya satır satır anlat; `docs/anlatim/tarife.md` yaz. Commit: `feat: 2026 parametreleri ve kümülatif tarife`.

### Task 3: Zam/ikramiye kuralları ve doğrulama

**Files:**
- Create: `bordro/kurallar.py`
- Test: `tests/gelistirici/test_kurallar.py`

**Interfaces:**
- Consumes: `kurus`, sabitler
- Produces:
  - `@dataclass Zam(ay: int, oran: Decimal)`
  - `@dataclass Ikramiye(ay: int, tutar: Decimal)`
  - `girdileri_dogrula(ocak_brut: Decimal, zamlar: list[Zam], ikramiyeler: list[Ikramiye]) -> None`: aşağıdaki mesajlarla `ValueError` fırlatır
  - `aylik_maaslar(ocak_brut: Decimal, zamlar: list[Zam]) -> list[Decimal]`: 12 eleman; zamlar ay sırasıyla uygulanır, her zamdan sonra `kurus`
  - `aylik_ikramiyeler(ikramiyeler: list[Ikramiye]) -> list[Decimal]`: 12 eleman; aynı ay toplanır
- Hata mesajları (birebir):
  - `"Ocak brüt maaşı en az 33.030,00 TL olmalı"`
  - `"Ocak brüt maaşı en fazla 10.000.000,00 TL olabilir"`
  - `"Zam ayı 2 ile 12 arasında olmalı"`
  - `"İkramiye ayı 1 ile 12 arasında olmalı"`
  - `"Zam oranı 0'dan büyük ve en fazla 100 olmalı"`
  - `"Aynı aya birden fazla zam girilemez"`
  - `"İkramiye tutarı 0'dan büyük olmalı"`
  - `"Tutarlar en fazla 2 ondalık basamak içerebilir"`

- [ ] **Step 1: Başarısız testleri yaz:**
  - `test_bilesik_zam_ve_yuvarlama`: `aylik_maaslar(D("33030.01"), [Zam(7, D("30")), Zam(10, D("10"))])` → `[0..5] == 33030.01`, `[6] == 42939.01`, `[9] == 47232.91`
  - `test_ayni_ay_ikramiyeler_toplanir`: `Ikramiye(6, 100) + Ikramiye(6, 50)` → `[5] == 150`
  - `test_ocak_zammi_reddedilir`: `pytest.raises(ValueError, match="Zam ayı 2 ile 12")`
  - `test_ayni_aya_iki_zam_reddedilir`
  - `test_ucuncu_ondalik_reddedilir`: `D("33030.001")`
- [ ] **Step 2:** `.venv\Scripts\python -m pytest tests/gelistirici/test_kurallar.py` → FAIL.
- [ ] **Step 3:** `bordro/kurallar.py`'yi yaz.
- [ ] **Step 4:** Aynı komut → PASS.
- [ ] **Step 5:** Anlat, `docs/anlatim/kurallar.md` yaz. Commit: `feat: zam/ikramiye kuralları ve doğrulama`.

### Task 4: Aylık ve yıllık bordro hesabı

**Files:**
- Create: `bordro/hesap.py`
- Test: `tests/gelistirici/test_hesap.py`

**Interfaces:**
- Consumes: Task 2 ve Task 3'ün tamamı
- Produces:
  - `@dataclass AySonucu`: `ay:int, maas, ikramiye, toplam_brut, sgk_isci, issizlik, gv_matrahi, kumulatif_matrah, hesaplanan_gv, au_istisna, gelir_vergisi, damga, net: Decimal; dilimler: list[int]; baslangic_orani: int; dilim_degisti: bool`
  - `@dataclass YilSonucu`: `aylar: list[AySonucu]; toplam_brut, toplam_net, toplam_gelir_vergisi, toplam_sgk: Decimal` (`toplam_sgk` = SGK işçi payı + işsizlik toplamı)
  - `ay_hesapla(ay: int, maas: Decimal, ikramiye: Decimal, onceki_kumulatif: Decimal) -> AySonucu`
  - `bordro_hesapla(ocak_brut: Decimal, zamlar: list[Zam], ikramiyeler: list[Ikramiye]) -> YilSonucu`: önce `girdileri_dogrula` çağırır
- Formüller spec §4.3'teki gibi. Ayrıca:
  - `au_istisna_m = kurus(T(28075.50·m) − T(28075.50·(m−1)))`
  - `damga = max(0, kurus(toplam_brut·0.00759) − 250.70)`
  - `dilim_degisti = max(dilimler) > baslangic_orani`

- [ ] **Step 1: Başarısız testleri yaz** (spesifikasyonun kontrol değerleri):

```python
def test_asgari_ucretli_yil():
    yil = bordro_hesapla(D("33030.00"), [], [])
    assert all(a.net == D("28075.50") and a.gelir_vergisi == 0 and a.damga == 0 for a in yil.aylar)
    assert [a.au_istisna for a in yil.aylar] == [D("4211.33")]*6 + [D("4537.75")] + [D("5615.10")]*5
    assert yil.aylar[6].dilimler == [15, 20] and yil.aylar[6].dilim_degisti

def test_50000_ocak_ornegi():
    a = bordro_hesapla(D("50000"), [], []).aylar[0]
    assert (a.sgk_isci, a.issizlik, a.hesaplanan_gv, a.gelir_vergisi, a.damga, a.net) == \
        (D("7000.00"), D("500.00"), D("6375.00"), D("2163.67"), D("128.80"), D("40207.53"))

def test_sgk_tavani_ikramiye_ayinda():
    a = bordro_hesapla(D("50000"), [], [Ikramiye(6, D("300000"))]).aylar[5]
    assert a.sgk_isci == D("41617.80") and a.issizlik == D("2972.70")

def test_ocakta_dev_ikramiye_dilim_uyarisi():
    a = bordro_hesapla(D("50000"), [], [Ikramiye(1, D("6000000"))]).aylar[0]
    assert a.dilimler == [15, 20, 27, 35, 40] and a.baslangic_orani == 15 and a.dilim_degisti
```

- [ ] **Step 2:** `.venv\Scripts\python -m pytest tests/gelistirici/test_hesap.py` → FAIL.
- [ ] **Step 3:** `bordro/hesap.py`'yi yaz.
- [ ] **Step 4:** `.venv\Scripts\python -m pytest` → tüm geliştirici testleri PASS.
- [ ] **Step 5:** Anlat, `docs/anlatim/hesap.md` yaz. Commit: `feat: aylık ve yıllık bordro hesabı`. Push (repo varsa).

### Task 5: İnsan tarafı test tasarımı (KULLANICI yapar, Claude öğretir ve çevirir)

**Files:**
- Create: `docs/test_tasarimi/sinir_degerleri.md`, `denklik_siniflari.md`, `karar_tablosu.md`, `durum_gecisi.md`; `tests/unit/test_*.py`

**Interfaces:**
- Consumes: Yalnızca `docs/gereksinimler.md` ve `docs/Mevzuat_2026.md`. Kullanıcı `tests/gelistirici/`'ye ve LLM çıktılarına **bakmaz**.
- Produces: `tests/unit/` (İNSAN grubu); her test adı ya da `ids` değeri R-numarası taşır.

- [ ] **Step 1:** Her teknik için kullanıcıya kısa ders anlat. Örnek olarak bordro dışından Lab 1'deki kargo örneğini kullan, bordro değerleri verme. Her dosyaya boş tablo şablonu koy: `| R-no | Teknik | Girdi | Beklenen | Gerekçe |`.
- [ ] **Step 2:** Kullanıcı tabloları doldurur; beklenen değerleri hesap makinesiyle kendisi hesaplar. Minimum: BVA ≥10 satır, EP ≥6, karar tablosu ≥8 kural (spec §7.3'teki 4 koşul), durum geçişi ≥5 geçiş.
- [ ] **Step 3:** Claude her tabloyu birebir `pytest.mark.parametrize` koduna çevirir; değerleri değiştirmez. Çeviri sırasında tablodaki bir değerin şüpheli göründüğünü fark ederse **düzeltmez**, sadece "bu satırı tekrar kontrol eder misin?" diye sorar. Kararı kullanıcı verir ve raporda not edilir.
- [ ] **Step 4:** `.venv\Scripts\python -m pytest tests/unit`. Kalan testler için hata kodda mı tabloda mı, birlikte incelenir. Kodda gerçek hata çıkarsa rapor §7 için "failure / defect / error" olarak kaydedilir.
- [ ] **Step 5:** Commit: `test: insan tasarımı unit testler`. **Lab 3 kontrol noktası:** `tests/unit` ≥10 geçen test.

---

## Aşama 2: API, sayfa, uçtan uca

### Task 6: FastAPI uç noktası

**Files:**
- Create: `api.py`
- Test: `tests/api/test_api.py`

**Interfaces:**
- Consumes: `bordro_hesapla`, `Zam`, `Ikramiye`
- Produces:
  - `POST /api/hesapla`
    - İstek: `{"ocak_brut": str|number, "zamlar": [{"ay": int, "oran": str|number}], "ikramiyeler": [{"ay": int, "tutar": str|number}]}`
    - Cevap 200: `{"aylar": [ {AySonucu alanları; Decimal'ler "1234.56" biçiminde string} ], "yillik": {"toplam_brut", "toplam_net", "toplam_gelir_vergisi", "toplam_sgk"}}`
    - `ValueError` olursa 422 + `{"detail": "<Türkçe mesaj>"}`. Sayılar `Decimal(str(x))` ile okunur.
  - `GET /` → `static/index.html`. `/static` mount edilir.

- [ ] **Step 1:** Başarısız testleri yaz (`TestClient(app)`):
  - `test_gecerli_istek_12_ay`
  - `test_50000_ocak_net` (`aylar[0]["net"] == "40207.53"`)
  - `test_asgari_alti_422_mesaj` (`detail` metni Task 3'tekiyle aynı)
  - `test_eksik_alan_422`
  - `test_float_girdi_tam_okunur`: `ocak_brut: 33030.1` → `aylar[0]["maas"] == "33030.10"`
  - `test_anasayfa_html_doner`
- [ ] **Step 2:** `.venv\Scripts\python -m pytest tests/api` → FAIL.
- [ ] **Step 3:** `api.py`'yi yaz (pydantic istek modelleri + `ValueError` exception handler).
- [ ] **Step 4:** Aynı komut → PASS. Elle kontrol: `.venv\Scripts\uvicorn api:app --reload`.
- [ ] **Step 5:** Anlat, `docs/anlatim/api.md`. Commit: `feat: hesap API'si`.

### Task 7: Sayfa (B düzeni + yıllık grafik)

**Files:**
- Create: `static/index.html`, `static/app.js`, `static/style.css`

**Interfaces:**
- Consumes: `POST /api/hesapla`
- Produces (Task 8 bu adlara dayanır):
  - Label'lar: `"Ocak brüt maaşı"`, her zam satırında `"Zam ayı"` / `"Zam oranı (%)"`, her ikramiye satırında `"İkramiye ayı"` / `"İkramiye tutarı (TL)"`
  - Butonlar: `"Hesapla"`, `"+ Zam ekle"`, `"+ İkramiye ekle"`, satır silme `"Sil"`
  - `data-testid`: `net-maas`, `secili-ay`, `dilim-uyarisi` (yalnızca `dilim_degisti` olduğunda görünür), `hata-mesaji`, `ay-sutunu-1` … `ay-sutunu-12`, `yillik-net`
- Davranış:
  - Girdiler Türkçe biçimde okunur: binlik `.` silinir, `,` → `.`. Gösterim `Intl.NumberFormat("tr-TR", {minimumFractionDigits: 2})` + " TL".
  - Boş zam/ikramiye satırı istekten çıkarılır.
  - Varsayılan seçili ay Ocak; bir sütuna tıklayınca seçili ay değişir.
  - Uyarı metni spec §4.4'teki gibi.
  - Grafik kütüphanesiz, `div` yükseklikleriyle çizilir.
  - Görünüm `Proje/.superpowers/brainstorm/*/content/layout-v2.html` ve `inputs-v3.html` taslaklarına sadık kalır.

- [ ] **Step 1:** Üç dosyayı yaz.
- [ ] **Step 2:** Sunucuyu başlat ve tarayıcıda elle doğrula:
  - 50.000 → Ocak net `40.207,53 TL`
  - Haziran'a 300.000 ikramiye → Haziran sütununda ikramiye rengi
  - 33.029,99 → `hata-mesaji` görünür
- [ ] **Step 3:** Ekran görüntüsünü kullanıcıya göster, onay al. Anlat, `docs/anlatim/sayfa.md`. Commit: `feat: bordro sayfası`.

### Task 8: Uçtan uca testler

**Files:**
- Create: `tests/e2e/conftest.py`, `tests/e2e/test_sayfa.py`

**Interfaces:**
- Consumes: Task 7'deki label/buton/testid adları
- Produces: `canli_sunucu` fixture'ı (session scope; uvicorn'u boş bir portta thread içinde başlatır, `base_url` döndürür)

- [ ] **Step 1:** Testleri yaz (`@pytest.mark.e2e`; locator olarak yalnızca `get_by_label`, `get_by_role`, `get_by_test_id`):
  - `test_ocak_net_gosterilir`
  - `test_turkce_sayi_bicimi` (`"50.000"` → `40.207,53 TL`)
  - `test_ikramiye_ve_zam_ekleme`
  - `test_dilim_uyarisi_temmuzda` (asgari ücret, Temmuz sütununa tıkla → `dilim-uyarisi` görünür)
  - `test_asgari_alti_hata_mesaji`
  - `test_bos_satir_yok_sayilir` ("+ Zam ekle", boş bırak, Hesapla → hata yok, sonuç var)
- [ ] **Step 2:** `.venv\Scripts\python -m pytest tests/e2e` → PASS (sayfa zaten var; bir testin bilerek kırıldığını görmek için `app.js`'teki biçim çevirisini geçici olarak bozup FAIL gör, sonra geri al).
- [ ] **Step 3:** `.venv\Scripts\python -m pytest` → tüm takım PASS.
- [ ] **Step 4:** Anlat. Commit: `test: uçtan uca testler`.

### Task 9: CI ve README

**Files:**
- Create: `.github/workflows/tests.yml`
- Modify: `README.md`

- [ ] **Step 1:** Workflow yaz:
  - `push` ile tetiklenen iş: ubuntu-latest, Python 3.11, `pip install -r requirements.txt`, `playwright install --with-deps chromium`, `pytest`
  - `workflow_dispatch` ile tetiklenen ayrı `mutasyon` işi: Task 14'teki betiği çalıştırır
- [ ] **Step 2:** README'yi tamamla. Şu sırayı içermeli, 5 dakikada uygulanabilir olmalı: kurulum (venv, pip, playwright) → `pytest` → `uvicorn api:app` → `http://127.0.0.1:8000`. Ayrıca klasör haritası ve test gruplarının anlamı.
- [ ] **Step 3:** Temiz bir klonda README'yi birebir uygula; süreyi ölç (≤5 dk). Push; Actions yeşil.
- [ ] **Step 4:** Commit: `ci: test iş akışı, README`.

---

## Aşama 3: AI deneyi

> Ön koşul: Task 5 tamamlandı. İnsan tabloları LLM çıktılarından ve hata listesinden önce bitmiş olmalı.

### Task 10: Yerleştirilmiş hata varyantları ve yakalama ölçer

**Files:**
- Create: `deney/hatali_surum/H1/bordro/` … `H8/bordro/` (her biri `bordro/`'nun tek değişiklikli tam kopyası), `deney/hatali_surum/birlesik/bordro/`, `deney/hatali_surum/HATALAR.md`, `deney/hata_yakalama.py`
- Test: `tests/gelistirici/test_varyantlar.py`

**Interfaces:**
- Produces: `python deney/hata_yakalama.py <test_klasoru>...`
  - Her test klasörünü doğru kodda ve her H-varyantında çalıştırır.
  - **İzolasyon:** Her çalıştırma `deney/gecici/<id>/` altında sıfırdan kurulan bir klasörde yapılır; içinde yalnızca ilgili `bordro/` kopyası, test klasörünün kopyası ve `pytest.ini` bulunur. Böylece gerçek paket hatalı varyantı gölgeleyemez.
  - Çıktı: `deney/sonuclar/hata_yakalama.md` (satır = test grubu, sütun = H1…H8, hücre = yakaladı / yakalamadı) ve ham JSON.

- [ ] **Step 1:** Spec §7.4'teki örneklere benzer 6–8 gerçekçi hata seç. Her biri için `HATALAR.md`'ye yaz: hata ne, hangi R-numarasını bozuyor, hangi teknik yakalamalı. **Kullanıcı bu dosyayı ölçüm bitene kadar okumaz.**
- [ ] **Step 2:** `test_her_varyant_dogru_koddan_farkli`: Her varyant için, sonucu doğru koddan farklı olan en az bir `bordro_hesapla` girdisi var olmalı. Hatalar "eşdeğer mutant" olmasın.
- [ ] **Step 3:** Varyantları ve `hata_yakalama.py`'yi yaz. `birlesik/` tüm hataları birlikte içerir.
- [ ] **Step 4:** `.venv\Scripts\python deney/hata_yakalama.py tests/gelistirici tests/unit` → tablo üretilir. Doğru kodda iki grup da tamamen geçmeli.
- [ ] **Step 5:** Commit: `feat(deney): yerleştirilmiş hata varyantları`.

### Task 11: LLM test üretici ve istemler

**Files:**
- Create: `ai/generate_tests.py`, `ai/prompts/D1.md`, `ai/prompts/D2.md`, `ai/prompts/D3.md`, `ai/prompts/ornek_test.py` (few-shot için tek kargo örneği), `ai/outputs/.gitkeep`

**Interfaces:**
- Produces: `python ai/generate_tests.py --deney D1|D2|D3 --tekrar N [--elle]`
  - İstem şablonu yer tutucuları: `{GEREKSINIMLER}` = `docs/gereksinimler.md`; `{IMZALAR}` = `bordro/` genel fonksiyon imzaları ve dataclass alanları; D2 için `{KOD}` = `deney/hatali_surum/birlesik/bordro/*.py`; D3 için `{GERI_BILDIRIM}` = Task 13'ün raporu
  - **İki turlu konuşma** (Week 5, slayt 12): Tur 1'de test tablosu istenir; tur 2'de "şimdi bu tablonun pytest kodunu yaz" denir.
  - Model `claude-opus-5-5`, `output_config.effort="high"`, adaptive thinking (varsayılan), sunucu taraflı `fallbacks="default"`. Bu modelde `temperature` desteklenmez; değişkenlik raporda olduğu gibi ölçülür. SDK kullanımı için claude-api becerisinin `python/claude-api/README.md` dosyası okunur, tahmin yürütülmez.
  - Çıktı: `ai/outputs/<deney>_<N>.md`. Üst bilgi: model, effort, tarih, istemin SHA-256'sı, `usage`; ardından tur 1 ve tur 2'nin ham metni.
  - `--elle`: API çağırmaz. İstemleri `ai/outputs/<deney>_<N>_istem.md`'ye yazar ve kullanıcının sohbet cevaplarını yapıştıracağı boş bölümler bırakır.
- İstem içeriği (D1/D2/D3 ortak çekirdek, spec §7.4 ve slayt 9–10, 27):
  - Rol
  - Gereksinimler kelimesi kelimesine
  - Teknikler: BVA, EP, karar tablosu, durum geçişi
  - pytest + parametrize, yalnızca verilen fonksiyon adları
  - "Beklenen değerleri yalnızca gereksinimlerden türet"
  - "Her assert somut bir değerle karşılaştırsın"
  - "Gereksinimin söylemediği bir şeyi test etmen gerekirse varsayım olarak listele"
  - D2'ye ayrıca kod eklenir ve "beklenen değerleri yalnızca gereksinimlerden türet" cümlesi **korunur** (gerçekçi senaryo).

- [ ] **Step 1:** `test_istem_yer_tutuculari_doldurulur` (`tests/gelistirici/`): Şablon doldurulunca `{` yer tutucusu kalmamalı ve D2 isteminde birleşik kodun bir satırı geçmeli. Bu test API çağırmaz.
- [ ] **Step 2:** Betiği ve istemleri yaz; Step 1'deki test PASS.
- [ ] **Step 3:** Kullanıcıdan karar al:
  - (a) API anahtarı oluşturmak (Anthropic Console; `ANTHROPIC_API_KEY` ortam değişkeni ya da `ant auth login`). Tahmini maliyet D1+D2+D3 × 3 tekrar ≈ 9 çağrı, birkaç dolar; çalıştırmadan önce `count_tokens` ile hesaplayıp kullanıcıya söyle ve onay al.
  - (b) ya da `--elle` yolu.
- [ ] **Step 4:** D1 ve D2'yi 3'er kez üret. Commit: `feat(ai): LLM test üretici, D1/D2 çıktıları`.

### Task 12: Filtre hattı ve insan incelemesi

**Files:**
- Create: `ai/filtre.py`, `ai/review_log.md`, `tests/llm/D1/`, `tests/llm/D3/`

**Interfaces:**
- Produces: `python ai/filtre.py ai/outputs/D1_1.md`
  - (1) Çıktıdaki python kod bloklarını `deney/adaylar/D1_1/test_*.py`'ye çıkarır; içeriğe dokunmaz.
  - (2) `pytest --collect-only` ile toplama hatalarını sayar (uydurulmuş import/API).
  - (3) Doğru kodda 5 kez çalıştırıp test başına geçti/kaldı kararlılığını raporlar.
  - (4) `deney/hata_yakalama.py` ile varyant matrisini üretir.
  - (5) D2 için "kopyalanmış hata" sayar: doğru kodda kalan ama ilgili varyantta geçen test.
  - Çıktı: `deney/adaylar/<id>/filtre_raporu.md`.
- `ai/review_log.md` sütunları: `çalıştırma | test id | R-no | karar (Tut/Düzelt/Reddet/Sor) | kategori (uydurulmuş API, kopyalanmış hata, boş assert, tekrar, uydurulmuş kural, diğer) | gerekçe`

- [ ] **Step 1:** `test_kod_bloklari_cikarilir`: Örnek bir markdown'dan 2 blok çıkar, sıra korunur.
- [ ] **Step 2:** `filtre.py`'yi yaz; testi geçir.
- [ ] **Step 3:** Altı çıktıyı (D1×3, D2×3) filtreden geçir. Raporları kullanıcıya özetle.
- [ ] **Step 4:** **Kullanıcı** hayatta kalan her testi `docs/gereksinimler.md` ile karşılaştırıp karar verir. Claude gerekçe tartışmasında yardım eder; kararı kullanıcı yazar. "Tut" alanlar `tests/llm/D1/`'e değiştirilmeden kopyalanır. "Düzelt" alanlar ayrı tutulur (`deney/duzeltilen/`).
- [ ] **Step 5:** Commit: `test(ai): D1/D2 incelemesi ve tutulan LLM testleri`.

### Task 13: D3 geri bildirim turu

**Files:**
- Modify: `ai/prompts/D3.md`
- Create: `ai/outputs/D3_*.md`, `tests/llm/D3/`

- [ ] **Step 1:** D1 tutulanlarının `pytest --cov=bordro --cov-branch --cov-report=term-missing` çıktısından ve hayatta kalan mutantların özetinden `{GERI_BILDIRIM}` metnini oluştur: hangi satırlar/dallar test edilmiyor, hangi mutantlar yaşıyor. Hata listesinden **bilgi sızdırma**.
- [ ] **Step 2:** D3'ü 3 kez üret → Task 12'deki filtre ve inceleme → `tests/llm/D3/`.
- [ ] **Step 3:** Commit: `test(ai): D3 geri bildirimli tur`.

### Task 14: Ölçüm ve sonuç tabloları

**Files:**
- Create: `deney/olcum.py`, `deney/mutasyon.sh`, `deney/sonuclar/*.md`

**Interfaces:**
- Produces:
  - `python deney/olcum.py`: Spec §7.5'teki tüm tabloları `deney/sonuclar/` altına yazar.
    - Gruplar: İnsan = `tests/unit`; LLM ham (çalıştırma başına `deney/adaylar/<id>`); LLM tutulan = `tests/llm/D1` + `tests/llm/D3`; Birlikte
    - Ölçüler: test sayısı (üretilen / toplanan / kararlı geçen / tutulan), satır ve dal coverage (`--cov=bordro`), H1…H8 yakalama, D2 kopyalanmış hata sayısı, 3 tekrar ortalaması ve min/max
  - `bash deney/mutasyon.sh <grup_klasoru>`: WSL ya da CI'da çalışır. `pyproject.toml`'daki `pytest_add_cli_args_test_selection`'ı gruba ayarlar, `mutmut run` + `mutmut export-cicd-stats` çalıştırır, skoru `deney/sonuclar/mutasyon_<grup>.json`'a yazar.

- [ ] **Step 1:** `test_olcum_tablo_bicimi`: Sahte bir ham JSON'dan beklenen markdown tablosu başlıkları üretilir.
- [ ] **Step 2:** Betikleri yaz; testi geçir.
- [ ] **Step 3:** WSL'de (`wsl -d Ubuntu-26.04`) repo içinde Linux venv kur. `mutasyon.sh`'yi İnsan, LLM tutulan ve Birlikte grupları için çalıştır.
- [ ] **Step 4:** `olcum.py`'yi çalıştır. Sonuç tablolarını kullanıcıyla birlikte oku; rapor §6–7 için ilginç bulguları (yardım ettiği ve yanılttığı en az birer somut örnek) `deney/sonuclar/bulgular.md`'ye not et.
- [ ] **Step 5:** Commit: `feat(deney): ölçüm sonuçları`.

---

## Aşama 4: Rapor desteği (teslim 11 Aralık 23:59)

### Task 15: Rapor malzemeleri

**Files:**
- Create: `docs/rapor/sekiller/*.png`, `docs/rapor/tablolar.md`, `docs/rapor/ai_kullanim_beyani_taslak.md` (yalnızca onaydan sonra)

- [ ] **Step 1:** `docs/rapor/tablolar.md` dosyasını hazırla. İçeriği:
  - Şablon §3 için "Requirement / Technique / Test values / Test function" tablosu (`tests/unit` ve `docs/test_tasarimi`'nden)
  - §7 için seviye başına test sayıları ve coverage
  - §6 için karşılaştırma tabloları
- [ ] **Step 2:** 2–3 şekil üret (matplotlib ya da sayfa ekran görüntüsü):
  - Sayfa ekran görüntüsü
  - Grup başına yakalanan hata / mutasyon skoru çubuk grafiği
  - Mimari şeması
- [ ] **Step 3:** **AI kullanım beyanı:** Taslak metni sohbette kullanıcıya göster (Tool / What I used it for / How I checked the result). Yalnızca onaydan sonra dosyaya yaz; itiraz gelirse düzeltip tekrar göster.
- [ ] **Step 4:** Raporu kullanıcı yazar (İngilizce, şablon başlıkları, 8–12 sayfa). Claude bölüm bölüm geri bildirim verir. Son kontrol: şablon başlıkları birebir; şekil ve tablolar numaralı; README komutu raporda tekrarlanıyor; repo linki doğru; son commit push edilmiş.
- [ ] **Step 5:** Kullanıcı PDF'i ve repo linkini Learn'e kendisi yükler. Commit: `docs: rapor malzemeleri`.
