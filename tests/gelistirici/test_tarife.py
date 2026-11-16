"""Geliştirici testleri: tarifenin spesifikasyonda verilen kontrol değerleri (R14, R16, R18, R19).

Bu testler karşılaştırma gruplarına girmez; yalnızca kodun spesifikasyondaki
sabit tutarlarla tutarlı olduğunu gösterir.
"""
from decimal import Decimal as D

import pytest

from bordro.para import kurus
from bordro.parametreler import ASGARI_UCRET_BRUT, DAMGA_ISTISNASI, DAMGA_ORANI
from bordro.tarife import dilimler, kumulatif_vergi, oran


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
