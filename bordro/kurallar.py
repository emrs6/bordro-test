"""Girdiler: zam ve ikramiye kuralları, doğrulama ve 12 aylık maaş/ikramiye listeleri (R1–R9)."""
from dataclasses import dataclass
from decimal import Decimal

from bordro.para import kurus
from bordro.parametreler import ASGARI_UCRET_BRUT, BRUT_UST_SINIR


@dataclass
class Zam:
    ay: int        # 2–12
    oran: Decimal  # yüzde, ör. Decimal("30") = %30


@dataclass
class Ikramiye:
    ay: int          # 1–12
    tutar: Decimal   # TL


def _iki_ondalikli_mi(x: Decimal) -> bool:
    return x == x.quantize(Decimal("0.01"))


def girdileri_dogrula(ocak_brut: Decimal, zamlar: list[Zam], ikramiyeler: list[Ikramiye]) -> None:
    """Girdiler kurallara uymuyorsa Türkçe mesajlı ValueError fırlatır."""
    tutarlar = [ocak_brut] + [z.oran for z in zamlar] + [i.tutar for i in ikramiyeler]
    if not all(_iki_ondalikli_mi(t) for t in tutarlar):
        raise ValueError("Tutarlar en fazla 2 ondalık basamak içerebilir")
    if ocak_brut < ASGARI_UCRET_BRUT:
        raise ValueError("Ocak brüt maaşı en az 33.030,00 TL olmalı")
    if ocak_brut > BRUT_UST_SINIR:
        raise ValueError("Ocak brüt maaşı en fazla 10.000.000,00 TL olabilir")
    for z in zamlar:
        if not 2 <= z.ay <= 12:
            raise ValueError("Zam ayı 2 ile 12 arasında olmalı")
        if not Decimal("0") < z.oran <= Decimal("100"):
            raise ValueError("Zam oranı 0'dan büyük ve en fazla 100 olmalı")
    if len({z.ay for z in zamlar}) != len(zamlar):
        raise ValueError("Aynı aya birden fazla zam girilemez")
    for i in ikramiyeler:
        if not 1 <= i.ay <= 12:
            raise ValueError("İkramiye ayı 1 ile 12 arasında olmalı")
        if i.tutar <= 0:
            raise ValueError("İkramiye tutarı 0'dan büyük olmalı")


def aylik_maaslar(ocak_brut: Decimal, zamlar: list[Zam]) -> list[Decimal]:
    """12 ayın brüt maaşı. Zamlar ay sırasıyla, bileşik uygulanır; her zamdan sonra kuruşa yuvarlanır."""
    zam_orani = {z.ay: z.oran for z in zamlar}
    maaslar = []
    maas = ocak_brut
    for ay in range(1, 13):
        if ay in zam_orani:
            maas = kurus(maas * (1 + zam_orani[ay] / 100))
        maaslar.append(maas)
    return maaslar


def aylik_ikramiyeler(ikramiyeler: list[Ikramiye]) -> list[Decimal]:
    """12 ayın ikramiye toplamı; aynı aydaki ikramiyeler toplanır."""
    toplamlar = [Decimal("0")] * 12
    for i in ikramiyeler:
        toplamlar[i.ay - 1] += i.tutar
    return toplamlar
