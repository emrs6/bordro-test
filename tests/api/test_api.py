"""Altyapı testleri: POST /api/hesapla ve ana sayfa (karşılaştırma gruplarına girmez)."""
from fastapi.testclient import TestClient

from api import app

istemci = TestClient(app)


def _istek(ocak_brut="50000", zamlar=None, ikramiyeler=None):
    return istemci.post("/api/hesapla", json={
        "ocak_brut": ocak_brut, "zamlar": zamlar or [], "ikramiyeler": ikramiyeler or [],
    })


def test_gecerli_istek_12_ay():
    cevap = _istek(zamlar=[{"ay": 7, "oran": "30"}], ikramiyeler=[{"ay": 6, "tutar": "50000"}])
    assert cevap.status_code == 200
    govde = cevap.json()
    assert len(govde["aylar"]) == 12
    assert set(govde["yillik"]) == {"toplam_brut", "toplam_net", "toplam_gelir_vergisi", "toplam_sgk"}


def test_50000_ocak_net():
    ocak = _istek().json()["aylar"][0]
    assert ocak["net"] == "40207.53"
    assert ocak["dilimler"] == [15] and ocak["baslangic_orani"] == 15 and ocak["dilim_degisti"] is False


def test_asgari_alti_422_mesaj():
    cevap = _istek(ocak_brut="33029.99")
    assert cevap.status_code == 422
    assert cevap.json()["detail"] == "Ocak brüt maaşı en az 33.030,00 TL olmalı"


def test_eksik_alan_422():
    cevap = istemci.post("/api/hesapla", json={"zamlar": [], "ikramiyeler": []})
    assert cevap.status_code == 422


def test_float_girdi_tam_okunur():
    cevap = _istek(ocak_brut=33030.1)
    assert cevap.status_code == 200
    assert cevap.json()["aylar"][0]["maas"] == "33030.10"


def test_tutarlar_iki_ondalikli_string():
    ocak = _istek(ocak_brut="33030").json()["aylar"][0]
    assert ocak["maas"] == "33030.00" and ocak["damga"] == "0.00"


def test_anasayfa_html_doner():
    cevap = istemci.get("/")
    assert cevap.status_code == 200
    assert cevap.headers["content-type"].startswith("text/html")
