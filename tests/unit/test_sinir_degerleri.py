"""İNSAN grubu: sınır değer analizi.

Değerler ve beklenen sonuçlar docs/test_tasarimi/sinir_degerleri.md tablosundan birebir alınmıştır
(tasarım: Emre Sülün, elle hesap). Bu dosya yalnızca tablonun pytest karşılığıdır.
"""
import re
from decimal import Decimal as D

import pytest

from bordro.hesap import bordro_hesapla
from bordro.kurallar import Ikramiye, Zam


@pytest.mark.parametrize("ocak_brut, ocak_net", [
    pytest.param("33030.00", "28075.50", id="R2-tam-alt-sinir"),
    pytest.param("33030.01", "28075.51", id="R2-alt-sinirin-1-kurus-ustu"),
    pytest.param("9999999.99", "6324307.72", id="R2-ust-sinirin-1-kurus-alti"),
    pytest.param("10000000.00", "6324307.73", id="R2-tam-ust-sinir"),
])
def test_ocak_brut_gecerli_sinirlar(ocak_brut, ocak_net):
    assert bordro_hesapla(D(ocak_brut), [], []).aylar[0].net == D(ocak_net)


@pytest.mark.parametrize("ocak_brut, mesaj", [
    pytest.param("33029.99", "Ocak brüt maaşı en az 33.030,00 TL olmalı", id="R2-alt-sinirin-1-kurus-alti"),
    pytest.param("10000000.01", "Ocak brüt maaşı en fazla 10.000.000,00 TL olabilir", id="R2-ust-sinirin-1-kurus-ustu"),
])
def test_ocak_brut_gecersiz_sinirlar(ocak_brut, mesaj):
    with pytest.raises(ValueError, match=re.escape(mesaj)):
        bordro_hesapla(D(ocak_brut), [], [])


@pytest.mark.parametrize("oran, subat_brut", [
    pytest.param("99.99", "66056.70", id="R4-zam-ust-sinirinin-0.01-alti"),
    pytest.param("100.00", "66060.00", id="R4-tam-zam-ust-siniri"),
])
def test_zam_orani_gecerli_sinirlar(oran, subat_brut):
    assert bordro_hesapla(D("33030.00"), [Zam(2, D(oran))], []).aylar[1].maas == D(subat_brut)


def test_zam_orani_ust_sinirin_ustu():  # R4: zam üst sınırının 0,01 puan üstü
    with pytest.raises(ValueError, match=re.escape("Zam oranı 0'dan büyük ve en fazla 100 olmalı")):
        bordro_hesapla(D("33030.00"), [Zam(2, D("100.01"))], [])


def test_ikramiye_sifir_reddedilir():  # R6: ikramiye alt sınırında geçersiz değer
    with pytest.raises(ValueError, match=re.escape("İkramiye tutarı 0'dan büyük olmalı")):
        bordro_hesapla(D("33030.00"), [], [Ikramiye(1, D("0.00"))])
