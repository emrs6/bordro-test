"""Web API: hesap motorunu POST /api/hesapla ile sunar ve sayfayı (static/) servis eder."""
from dataclasses import asdict
from decimal import Decimal, InvalidOperation
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from bordro.hesap import bordro_hesapla
from bordro.kurallar import Ikramiye, Zam

STATIC = Path(__file__).parent / "static"
Sayi = str | int | float

app = FastAPI(title="Bordro Hesaplayıcı 2026")
app.mount("/static", StaticFiles(directory=STATIC), name="static")


class ZamIstek(BaseModel):
    ay: int
    oran: Sayi


class IkramiyeIstek(BaseModel):
    ay: int
    tutar: Sayi


class HesaplaIstek(BaseModel):
    ocak_brut: Sayi
    zamlar: list[ZamIstek] = []
    ikramiyeler: list[IkramiyeIstek] = []


def sayi(x: Sayi) -> Decimal:
    """JSON sayısını tam okur: 33030.1 → Decimal('33030.1'); ikili kayan nokta artığı taşımaz."""
    try:
        return Decimal(str(x))
    except InvalidOperation:
        raise ValueError(f"Geçersiz sayı: {x}")


def json_uyumlu(deger):
    """Decimal'leri 2 ondalıklı string yapar ("33030" → "33030.00"); listeler ve sözlüklerde de."""
    if isinstance(deger, Decimal):
        return f"{deger.quantize(Decimal('0.01'))}"
    if isinstance(deger, dict):
        return {k: json_uyumlu(v) for k, v in deger.items()}
    if isinstance(deger, list):
        return [json_uyumlu(v) for v in deger]
    return deger


@app.exception_handler(ValueError)
async def dogrulama_hatasi(_: Request, hata: ValueError):
    return JSONResponse(status_code=422, content={"detail": str(hata)})


@app.post("/api/hesapla")
def hesapla(istek: HesaplaIstek):
    yil = bordro_hesapla(
        sayi(istek.ocak_brut),
        [Zam(z.ay, sayi(z.oran)) for z in istek.zamlar],
        [Ikramiye(i.ay, sayi(i.tutar)) for i in istek.ikramiyeler],
    )
    sonuc = asdict(yil)
    return json_uyumlu({"aylar": sonuc.pop("aylar"), "yillik": sonuc})


@app.get("/")
def anasayfa():
    return FileResponse(STATIC / "index.html")
