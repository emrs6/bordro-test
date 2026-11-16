# Durum geçişi (State Transition)

## Kısa ders
Sistemin bir **durumu** varsa ve bir olayla başka bir duruma geçiyorsa, her geçişi ayrı test ederiz.

**Örnek:** Sipariş durumu: Hazırlanıyor → (kargoya verildi) → Kargoda → (teslim edildi) → Teslim. Testler: her ok bir test, artı geçersiz geçişler (Teslim → Hazırlanıyor olamaz).

## Bordroda durum: "Hangi vergi dilimindeyim?"
Yıl boyunca birikmiş matrah büyüdükçe çalışan dilimden dilime geçer: **%15 → %20 → %27 → %35 → %40**. Olay "bir ayın maaşının eklenmesi". R19'daki `baslangic_orani`, `dilimler` ve `dilim_degisti` bu geçişi gösterir.

Denemeniz gereken geçişler:
- %15'te kalış (geçiş yok)
- %15 → %20 (ay içinde sınırı geçme)
- Önceki ay tam sınırda bitti, bu ay tamamı üst dilimde (R19'daki "starting rate" kuralı)
- Bir ayda birden fazla dilim atlama (büyük ikramiye)
- Ocak'ta geçiş (yüksek maaş ya da Ocak ikramiyesi)

## Tablonuz (en az 5 geçiş)

| Geçiş | Senaryo (Ocak brüt, zam, ikramiye) | Ay | Beklenen `baslangic_orani` | Beklenen `dilimler` | Beklenen `dilim_degisti` | Gerekçe |
|---|---|---|---|---|---|---|
| G1 | | | | | | |
| G2 | | | | | | |
| G3 | | | | | | |
| G4 | | | | | | |
| G5 | | | | | | |
