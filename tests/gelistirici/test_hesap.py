"""Geliştirici testleri: spesifikasyonun kontrol değerleri (R10–R19, R21)."""
from decimal import Decimal as D

from bordro.hesap import bordro_hesapla
from bordro.kurallar import Ikramiye


def test_asgari_ucretli_yil():
    yil = bordro_hesapla(D("33030.00"), [], [])
    assert all(a.net == D("28075.50") and a.gelir_vergisi == 0 and a.damga == 0 for a in yil.aylar)
    assert [a.au_istisna for a in yil.aylar] == [D("4211.33")] * 6 + [D("4537.75")] + [D("5615.10")] * 5
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


def test_yillik_toplamlar_asgari_ucret():
    yil = bordro_hesapla(D("33030.00"), [], [])
    assert yil.toplam_brut == D("396360.00")
    assert yil.toplam_net == D("336906.00")
    assert yil.toplam_gelir_vergisi == D("0")
    assert yil.toplam_sgk == D("59454.00")
