"""Altyapı testleri: sayfa, gerçek tarayıcıda (Playwright, Chromium).

Locator'lar yalnızca kullanıcının gördüğü adlar (label, rol) ve data-testid'dir.
"""
import pytest
from playwright.sync_api import Page, expect

pytestmark = pytest.mark.e2e


def _hesapla(page: Page, sunucu: str, ocak_brut: str) -> None:
    page.goto(sunucu)
    page.get_by_label("Ocak brüt maaşı").fill(ocak_brut)
    page.get_by_role("button", name="Hesapla").click()


def test_ocak_net_gosterilir(page: Page, canli_sunucu):
    _hesapla(page, canli_sunucu, "50000")
    expect(page.get_by_test_id("secili-ay")).to_have_text("Ocak")
    expect(page.get_by_test_id("net-maas")).to_have_text("40.207,53 TL")


def test_turkce_sayi_bicimi(page: Page, canli_sunucu):
    _hesapla(page, canli_sunucu, "50.000")
    expect(page.get_by_test_id("net-maas")).to_have_text("40.207,53 TL")


def test_ikramiye_ve_zam_ekleme(page: Page, canli_sunucu):
    page.goto(canli_sunucu)
    page.get_by_label("Ocak brüt maaşı").fill("50.000")
    page.get_by_role("button", name="+ İkramiye ekle").click()
    page.get_by_label("İkramiye ayı").select_option(label="Haziran")
    page.get_by_label("İkramiye tutarı (TL)").fill("300.000")
    page.get_by_role("button", name="+ Zam ekle").click()
    page.get_by_label("Zam ayı").select_option(label="Temmuz")
    page.get_by_label("Zam oranı (%)").fill("30")
    page.get_by_role("button", name="Hesapla").click()
    page.get_by_test_id("ay-sutunu-6").click()
    expect(page.get_by_test_id("secili-ay")).to_have_text("Haziran")
    expect(page.get_by_test_id("dilim-uyarisi")).to_have_text("Bu ay %20 diliminden %27 dilimine geçtiniz.")
    page.get_by_test_id("ay-sutunu-7").click()
    expect(page.get_by_test_id("secili-ay")).to_have_text("Temmuz")
    expect(page.locator("#kesintiler")).to_contain_text("65.000,00 TL")


def test_dilim_uyarisi_temmuzda(page: Page, canli_sunucu):
    _hesapla(page, canli_sunucu, "33.030")
    expect(page.get_by_test_id("dilim-uyarisi")).to_be_hidden()
    page.get_by_test_id("ay-sutunu-7").click()
    expect(page.get_by_test_id("dilim-uyarisi")).to_be_visible()
    expect(page.get_by_test_id("dilim-uyarisi")).to_have_text("Bu ay %15 diliminden %20 dilimine geçtiniz.")


def test_asgari_alti_hata_mesaji(page: Page, canli_sunucu):
    _hesapla(page, canli_sunucu, "33.029,99")
    expect(page.get_by_test_id("hata-mesaji")).to_have_text("Ocak brüt maaşı en az 33.030,00 TL olmalı")
    expect(page.get_by_test_id("net-maas")).to_be_hidden()


def test_bos_satir_yok_sayilir(page: Page, canli_sunucu):
    page.goto(canli_sunucu)
    page.get_by_label("Ocak brüt maaşı").fill("50.000")
    page.get_by_role("button", name="+ Zam ekle").click()
    page.get_by_role("button", name="Hesapla").click()
    expect(page.get_by_test_id("hata-mesaji")).to_be_hidden()
    expect(page.get_by_test_id("net-maas")).to_have_text("40.207,53 TL")
