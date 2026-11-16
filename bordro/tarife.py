"""Kümülatif gelir vergisi tarifesi (R14, R18, R19)."""
from decimal import Decimal

from bordro.parametreler import UCRET_TARIFESI


def kumulatif_vergi(matrah: Decimal) -> Decimal:
    """T(x): yıl başından beri birikmiş matrah için toplam gelir vergisi (yuvarlamasız)."""
    vergi = Decimal("0")
    alt_sinir = Decimal("0")
    for ust_sinir, yuzde in UCRET_TARIFESI:
        if ust_sinir is None or matrah <= ust_sinir:
            return vergi + (matrah - alt_sinir) * yuzde / 100
        vergi += (ust_sinir - alt_sinir) * yuzde / 100
        alt_sinir = ust_sinir
    return vergi  # buraya gelinmez: son dilimin üst sınırı yok


def oran(matrah: Decimal) -> int:
    """Birikmiş matrahın içinde bulunduğu dilimin oranı. Sınır noktası alt dilime aittir."""
    for ust_sinir, yuzde in UCRET_TARIFESI:
        if ust_sinir is None or matrah <= ust_sinir:
            return yuzde
    return UCRET_TARIFESI[-1][1]


def dilimler(onceki: Decimal, simdiki: Decimal) -> list[int]:
    """(onceki, simdiki] aralığının pozitif tutarla geçtiği oranlar, artan sırada."""
    sonuc = []
    alt_sinir = Decimal("0")
    for ust_sinir, yuzde in UCRET_TARIFESI:
        dilim_ust = simdiki if ust_sinir is None else min(simdiki, ust_sinir)
        if dilim_ust > max(onceki, alt_sinir):
            sonuc.append(yuzde)
        if ust_sinir is None:
            break
        alt_sinir = ust_sinir
    return sonuc
