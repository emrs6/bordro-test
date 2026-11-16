"""Para yuvarlama (R20)."""
from decimal import ROUND_HALF_UP, Decimal


def kurus(x: Decimal) -> Decimal:
    """Tutarı kuruşa yuvarlar; yarımlar yukarı (0,005 → 0,01)."""
    return x.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
