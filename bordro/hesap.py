"""Aylık ve yıllık bordro hesabı (R9–R21)."""
from dataclasses import dataclass
from decimal import Decimal

from bordro import tarife
from bordro.kurallar import Ikramiye, Zam, aylik_ikramiyeler, aylik_maaslar, girdileri_dogrula
from bordro.para import kurus
from bordro.parametreler import (
    ASGARI_UCRET_GV_MATRAHI, DAMGA_ISTISNASI, DAMGA_ORANI,
    ISSIZLIK_ISCI_ORANI, SGK_ISCI_ORANI, SGK_TAVAN,
)


@dataclass
class AySonucu:
    ay: int
    maas: Decimal
    ikramiye: Decimal
    toplam_brut: Decimal
    sgk_isci: Decimal
    issizlik: Decimal
    gv_matrahi: Decimal
    kumulatif_matrah: Decimal
    hesaplanan_gv: Decimal
    au_istisna: Decimal
    gelir_vergisi: Decimal
    damga: Decimal
    net: Decimal
    dilimler: list[int]
    baslangic_orani: int
    dilim_degisti: bool


@dataclass
class YilSonucu:
    aylar: list[AySonucu]
    toplam_brut: Decimal
    toplam_net: Decimal
    toplam_gelir_vergisi: Decimal
    toplam_sgk: Decimal


def asgari_ucret_istisnasi(ay: int) -> Decimal:
    """Asgari ücrete düşen gelir vergisi; o ayın kümülatif asgari ücret matrahına göre (R15)."""
    T = tarife.kumulatif_vergi
    return kurus(T(ASGARI_UCRET_GV_MATRAHI * ay) - T(ASGARI_UCRET_GV_MATRAHI * (ay - 1)))


def ay_hesapla(ay: int, maas: Decimal, ikramiye: Decimal, onceki_kumulatif: Decimal) -> AySonucu:
    toplam_brut = maas + ikramiye
    sgk_matrahi = min(toplam_brut, SGK_TAVAN)
    sgk_isci = kurus(sgk_matrahi * SGK_ISCI_ORANI)
    issizlik = kurus(sgk_matrahi * ISSIZLIK_ISCI_ORANI)
    gv_matrahi = toplam_brut - sgk_isci - issizlik
    kumulatif = onceki_kumulatif + gv_matrahi
    hesaplanan_gv = kurus(tarife.kumulatif_vergi(kumulatif) - tarife.kumulatif_vergi(onceki_kumulatif))
    au_istisna = asgari_ucret_istisnasi(ay)
    gelir_vergisi = max(Decimal("0"), hesaplanan_gv - au_istisna)
    damga = max(Decimal("0"), kurus(toplam_brut * DAMGA_ORANI) - DAMGA_ISTISNASI)
    net = toplam_brut - sgk_isci - issizlik - gelir_vergisi - damga
    dilimler = tarife.dilimler(onceki_kumulatif, kumulatif)
    baslangic = tarife.oran(onceki_kumulatif)
    return AySonucu(
        ay, maas, ikramiye, toplam_brut, sgk_isci, issizlik, gv_matrahi, kumulatif,
        hesaplanan_gv, au_istisna, gelir_vergisi, damga, net,
        dilimler, baslangic, max(dilimler) > baslangic,
    )


def bordro_hesapla(ocak_brut: Decimal, zamlar: list[Zam], ikramiyeler: list[Ikramiye]) -> YilSonucu:
    """Girdileri doğrular, 12 ayı sırayla hesaplar ve yıllık toplamları döndürür."""
    girdileri_dogrula(ocak_brut, zamlar, ikramiyeler)
    maaslar = aylik_maaslar(ocak_brut, zamlar)
    ikramiye_listesi = aylik_ikramiyeler(ikramiyeler)
    aylar = []
    kumulatif = Decimal("0")
    for ay in range(1, 13):
        sonuc = ay_hesapla(ay, maaslar[ay - 1], ikramiye_listesi[ay - 1], kumulatif)
        aylar.append(sonuc)
        kumulatif = sonuc.kumulatif_matrah
    return YilSonucu(
        aylar,
        toplam_brut=sum((a.toplam_brut for a in aylar), Decimal("0")),
        toplam_net=sum((a.net for a in aylar), Decimal("0")),
        toplam_gelir_vergisi=sum((a.gelir_vergisi for a in aylar), Decimal("0")),
        toplam_sgk=sum((a.sgk_isci + a.issizlik for a in aylar), Decimal("0")),
    )
