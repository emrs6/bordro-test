// Bordro sayfası: girdileri toplar, POST /api/hesapla'ya gönderir, sonucu çizer.
const AYLAR = ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran",
               "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"];
const KISA = ["Oca", "Şub", "Mar", "Nis", "May", "Haz", "Tem", "Ağu", "Eyl", "Eki", "Kas", "Ara"];
const TL = new Intl.NumberFormat("tr-TR", { minimumFractionDigits: 2, maximumFractionDigits: 2 });

const $ = (sec) => document.querySelector(sec);
let sonuc = null;      // son API cevabı
let seciliAy = 1;

// "50.000,50" → "50000.50": nokta binlik ayırıcı, virgül ondalık ayırıcı (Türkçe yazım).
function turkceSayi(metin) {
  const temiz = metin.trim().replace(/\s/g, "").replace(/\./g, "").replace(",", ".");
  if (!/^\d+(\.\d+)?$/.test(temiz)) throw new Error(`Geçersiz sayı: ${metin}`);
  return temiz;
}
const tl = (x) => `${TL.format(Number(x))} TL`;

function satirEkle(kapsayici, sablonId, ilkAy) {
  const satir = document.getElementById(sablonId).content.firstElementChild.cloneNode(true);
  const secim = satir.querySelector("select");
  AYLAR.forEach((ad, i) => { if (i + 1 >= ilkAy) secim.add(new Option(ad, i + 1)); });
  satir.querySelector(".sil").addEventListener("click", () => satir.remove());
  kapsayici.appendChild(satir);
}

// Boş bırakılmış zam/ikramiye satırları yok sayılır.
function satirlariOku(kapsayici, alan) {
  return [...kapsayici.querySelectorAll(".satir")]
    .filter((s) => s.querySelector(`[name=${alan}]`).value.trim() !== "")
    .map((s) => ({ ay: Number(s.querySelector("select").value),
                   [alan]: turkceSayi(s.querySelector(`[name=${alan}]`).value) }));
}

// Hata varsa eski sonuç gizlenir; yoksa yeni girdiye aitmiş gibi görünürdü.
function hataGoster(mesaj) {
  const kutu = $("#hata");
  kutu.textContent = mesaj;
  kutu.hidden = !mesaj;
  if (mesaj) {
    $("#ay-detay").hidden = true;
    $("#yillik").hidden = true;
    $("#bos").hidden = false;
  }
}

async function hesapla(olay) {
  olay.preventDefault();
  hataGoster("");
  let istek;
  try {
    istek = { ocak_brut: turkceSayi($("#ocak-brut").value),
              zamlar: satirlariOku($("#zamlar"), "oran"),
              ikramiyeler: satirlariOku($("#ikramiyeler"), "tutar") };
  } catch (hata) { return hataGoster(hata.message); }
  const cevap = await fetch("/api/hesapla", { method: "POST",
    headers: { "Content-Type": "application/json" }, body: JSON.stringify(istek) });
  const govde = await cevap.json();
  if (!cevap.ok) {
    return hataGoster(typeof govde.detail === "string" ? govde.detail : "Girdiler eksik ya da hatalı.");
  }
  sonuc = govde;
  ayGoster(1);
}

function dilimUyarisi(ay) {
  if (!ay.dilim_degisti) return "";
  const yol = [ay.baslangic_orani, ...ay.dilimler.filter((o) => o > ay.baslangic_orani)];
  const son = yol[yol.length - 1];
  let metin = `Bu ay %${ay.baslangic_orani} diliminden %${son} dilimine geçtiniz.`;
  if (yol.length > 2) metin += ` (${yol.map((o) => "%" + o).join(" → ")})`;
  return metin;
}

function cubukCiz(ay) {
  const brut = Number(ay.toplam_brut);
  const parcalar = [
    ["Net", Number(ay.net), "var(--net)"],
    ["SGK + işsizlik", Number(ay.sgk_isci) + Number(ay.issizlik), "var(--sgk)"],
    ["Gelir v.", Number(ay.gelir_vergisi), "var(--gv)"],
    ["Damga", Number(ay.damga), "var(--damga)"],
  ];
  $("#cubuk").innerHTML = parcalar.map(([, t, renk]) =>
    `<div style="width:${(100 * t / brut).toFixed(2)}%;background:${renk}"></div>`).join("");
  $("#cubuk-aciklama").innerHTML = parcalar.map(([ad, t, renk]) =>
    `<span style="color:${renk}">${ad} %${(100 * t / brut).toFixed(1)}</span>`).join(" · ");
}

function kesintiTablosu(ay) {
  const satirlar = [
    ["Brüt maaş", ay.maas], ["İkramiye", ay.ikramiye], ["Toplam brüt", ay.toplam_brut],
    ["SGK işçi payı (%14)", "−" + ay.sgk_isci], ["İşsizlik sigortası (%1)", "−" + ay.issizlik],
    ["Hesaplanan gelir vergisi", ay.hesaplanan_gv], ["Asgari ücret istisnası", ay.au_istisna],
    ["Kesilen gelir vergisi", "−" + ay.gelir_vergisi], ["Damga vergisi", "−" + ay.damga],
  ];
  $("#kesintiler").innerHTML = satirlar.map(([ad, t]) =>
    `<tr><td>${ad}</td><td>${t.startsWith("−") ? "−" + tl(t.slice(1)) : tl(t)}</td></tr>`).join("")
    + `<tr class="toplam"><td>Net maaş</td><td>${tl(ay.net)}</td></tr>`;
}

function grafikCiz() {
  const enYuksek = Math.max(...sonuc.aylar.map((a) => Number(a.net)));
  $("#grafik").innerHTML = sonuc.aylar.map((a) => {
    const net = Number(a.net);
    const ikramiyeNet = net * Number(a.ikramiye) / Number(a.toplam_brut);  // orantılı pay
    const yukseklik = (x) => (150 * x / enYuksek).toFixed(1);
    const sinif = ["sutun", a.ay === seciliAy ? "secili" : "", a.dilim_degisti ? "degisti" : ""].join(" ");
    return `<button type="button" class="${sinif}" data-testid="ay-sutunu-${a.ay}" data-ay="${a.ay}"
      title="${AYLAR[a.ay - 1]}: ${tl(a.net)}"><span class="govde">
      <span class="ikramiye-parca" style="height:${yukseklik(ikramiyeNet)}px"></span>
      <span class="net-parca" style="height:${yukseklik(net - ikramiyeNet)}px"></span></span>${KISA[a.ay - 1]}</button>`;
  }).join("");
  $("#grafik").querySelectorAll(".sutun").forEach((s) =>
    s.addEventListener("click", () => ayGoster(Number(s.dataset.ay))));
}

function ayGoster(ayNo) {
  seciliAy = ayNo;
  const ay = sonuc.aylar[ayNo - 1];
  $("#bos").hidden = true;
  $("#ay-detay").hidden = false;
  $("[data-testid=secili-ay]").textContent = AYLAR[ayNo - 1];
  $("[data-testid=net-maas]").textContent = tl(ay.net);
  const uyari = dilimUyarisi(ay);
  $("[data-testid=dilim-uyarisi]").textContent = uyari;
  $("[data-testid=dilim-uyarisi]").hidden = !uyari;
  cubukCiz(ay);
  kesintiTablosu(ay);
  $("#yillik").hidden = false;
  $("[data-testid=yillik-net]").textContent = tl(sonuc.yillik.toplam_net);
  $("#yillik-gv").textContent = tl(sonuc.yillik.toplam_gelir_vergisi);
  $("#yillik-sgk").textContent = tl(sonuc.yillik.toplam_sgk);
  grafikCiz();
}

$("#zam-ekle").addEventListener("click", () => satirEkle($("#zamlar"), "zam-satiri", 2));
$("#ikramiye-ekle").addEventListener("click", () => satirEkle($("#ikramiyeler"), "ikramiye-satiri", 1));
$("#form").addEventListener("submit", hesapla);
