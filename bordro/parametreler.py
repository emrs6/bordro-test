"""2026 bordro parametreleri. Bütün sabitler yalnızca bu dosyada tanımlıdır.

Kaynaklar ve hesap kontrolleri: docs/Mevzuat_2026.md
"""
from decimal import Decimal

# SGK, "Prime Esas Kazanç Miktarları" (özel sektör, 1/1/2026–31/12/2026)
ASGARI_UCRET_BRUT = Decimal("33030.00")      # aylık kazanç alt sınırı = brüt asgari ücret
SGK_TAVAN = Decimal("297270.00")             # aylık kazanç üst sınırı (alt sınırın 9 katı)

# 5510 s. Kanun (işçi payı %9 malullük-yaşlılık-ölüm + %5 genel sağlık), 4447 s. Kanun
SGK_ISCI_ORANI = Decimal("0.14")
ISSIZLIK_ISCI_ORANI = Decimal("0.01")

# 488 s. Damga Vergisi Kanunu, (1) sayılı tablo: binde 7,59
DAMGA_ORANI = Decimal("0.00759")
# Asgari ücretin damga vergisi: 33.030,00 × 0,00759 = 250,70 (DVK istisnası)
DAMGA_ISTISNASI = Decimal("250.70")

# Asgari ücretin aylık gelir vergisi matrahı: 33.030,00 − %15 (SGK + işsizlik) = 28.075,50
ASGARI_UCRET_GV_MATRAHI = Decimal("28075.50")

# Tasarım kararı (spec §4.2): Ocak brüt maaşı için makul üst sınır
BRUT_UST_SINIR = Decimal("10000000.00")

# GİB, Gelir Vergisi Tarifesi 2026 (GVK md. 103), ÜCRET gelirleri.
# Her satır: (dilimin üst sınırı, oran %). Son dilimin üst sınırı yok (None).
UCRET_TARIFESI = [
    (Decimal("190000"), 15),
    (Decimal("400000"), 20),
    (Decimal("1500000"), 27),
    (Decimal("5300000"), 35),
    (None, 40),
]
