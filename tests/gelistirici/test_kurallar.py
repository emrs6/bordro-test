"""Geliştirici testleri: zam/ikramiye kuralları ve doğrulama (R3, R5, R7, R8)."""
from decimal import Decimal as D

import pytest

from bordro.kurallar import Ikramiye, Zam, aylik_ikramiyeler, aylik_maaslar, girdileri_dogrula


def test_bilesik_zam_ve_yuvarlama():
    maaslar = aylik_maaslar(D("33030.01"), [Zam(7, D("30")), Zam(10, D("10"))])
    assert len(maaslar) == 12
    assert maaslar[:6] == [D("33030.01")] * 6
    assert maaslar[6] == D("42939.01")
    assert maaslar[9] == D("47232.91")


def test_ayni_ay_ikramiyeler_toplanir():
    ikramiyeler = aylik_ikramiyeler([Ikramiye(6, D("100")), Ikramiye(6, D("50"))])
    assert ikramiyeler[5] == D("150")
    assert sum(ikramiyeler) == D("150")


def test_ocak_zammi_reddedilir():
    with pytest.raises(ValueError, match="Zam ayı 2 ile 12 arasında olmalı"):
        girdileri_dogrula(D("50000"), [Zam(1, D("10"))], [])


def test_ayni_aya_iki_zam_reddedilir():
    with pytest.raises(ValueError, match="Aynı aya birden fazla zam girilemez"):
        girdileri_dogrula(D("50000"), [Zam(7, D("10")), Zam(7, D("5"))], [])


def test_ucuncu_ondalik_reddedilir():
    with pytest.raises(ValueError, match="Tutarlar en fazla 2 ondalık basamak içerebilir"):
        girdileri_dogrula(D("33030.001"), [], [])
