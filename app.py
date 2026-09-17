import streamlit as st
import os
import re
from collections import Counter
from urllib.parse import quote

# =========================================================
# KONFIGURASI
# =========================================================
st.set_page_config(
    page_title="AI Tutor Bahasa Indonesia",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =========================================================
# STYLE
# =========================================================
st.markdown(r"""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@500;600;700&display=swap');
:root{--ink:#2d2924;--muted:#786f67;--line:rgba(105,83,62,.13);--brown:#8a624b;--cream:#f7f1e8}
body,.stApp,.stMarkdown,p,div,span,button,input,textarea{font-family:'DM Sans',Arial,sans-serif}
.hero-title,.section-title,.question-title,.topic-card h3,.topic-visual h3,.stat-number,.brand-name,.quote,.fact-title,.popular-title{font-family:'Playfair Display',Georgia,serif}
.stApp{background:radial-gradient(circle at 93% 13%,rgba(206,193,174,.28) 0 150px,transparent 151px),radial-gradient(circle at 8% 82%,rgba(215,196,174,.25) 0 170px,transparent 171px),linear-gradient(135deg,#fbf8f3,#f3ece2 52%,#f8f4ee);color:var(--ink)}
footer{visibility:hidden;height:0!important},#MainMenu,footer{visibility:hidden;height:0!important}
[data-testid="stAppViewContainer"]{background:transparent}
[data-testid="stAppViewContainer"]>.main{background:transparent;padding-top:0!important}
[data-testid="stSidebar"]{background:rgba(250,247,242,.95);border-right:1px solid var(--line)}
[data-testid="stSidebar"]>div:first-child{background:transparent}
[data-testid="stSidebar"] .block-container{padding:1.25rem 1.05rem}
.paper-dots{position:fixed;inset:0;pointer-events:none;z-index:0;opacity:.20;background-image:radial-gradient(rgba(105,83,62,.22) 1px,transparent 1px);background-size:28px 28px}
.app-orb{position:fixed;border-radius:50%;pointer-events:none;z-index:0}.orb-a{width:240px;height:240px;right:-80px;top:100px;background:rgba(189,179,162,.16)}.orb-b{width:210px;height:210px;left:24%;bottom:-100px;background:rgba(175,197,178,.13)}
.brand{display:flex;gap:.7rem;align-items:center}.brand-icon{width:48px;height:48px;border-radius:15px;display:grid;place-items:center;background:#efe5d9;box-shadow:0 7px 18px rgba(70,50,35,.09);font-size:1.45rem}.brand-name{font-family:'Playfair Display', Georgia, serif;font-size:1.14rem;font-weight:700;line-height:1.05}.brand-sub{font-size:.68rem;color:#958b82;margin-top:.2rem}.side-item{padding:.62rem .7rem;border-radius:12px;margin:.16rem 0;color:#514a43;font-size:.87rem;transition:.2s}.side-item.active{background:#eee3d8;color:#704c37;font-weight:700}.side-item:hover{transform:translateX(3px);background:#f3ebe3}.side-status{padding:.8rem .85rem;border-radius:15px;background:rgba(232,243,232,.78);border:1px solid rgba(86,116,91,.12)}.quote{margin-top:1rem;padding:1rem .85rem;border:1px solid var(--line);border-radius:16px;background:rgba(255,253,249,.65);font-family:'Playfair Display', Georgia, serif;font-style:italic;line-height:1.5;color:#62564c}.quote small{display:block;margin-top:.5rem;font-family:'DM Sans', Arial, sans-serif;font-style:normal;color:#94877c}
.hero{position:relative;overflow:hidden;min-height:228px;padding:1.35rem 2rem;border-radius:28px;border:1px solid var(--line);background:linear-gradient(90deg,rgba(250,246,240,.98) 0%,rgba(250,246,240,.91) 53%,rgba(235,226,214,.67) 100%);box-shadow:0 16px 42px rgba(74,58,44,.10);animation:fadeUp .55s ease-out}.hero:before{content:"";position:absolute;width:290px;height:290px;right:-80px;top:-80px;border-radius:50%;background:rgba(216,205,188,.28)}.hero:after{content:"📚   🌿   ☕";position:absolute;right:3%;bottom:1rem;font-size:3.4rem;opacity:.42;filter:drop-shadow(0 8px 8px rgba(60,45,30,.08))}.hero-inner{position:relative;z-index:2;max-width:760px}.welcome-pill{display:inline-block;padding:.35rem .75rem;border-radius:999px;background:rgba(255,255,255,.74);border:1px solid var(--line);color:#735743;font-size:.73rem}.hero-title{font-family:'Playfair Display', Georgia, serif;font-size:2.85rem;font-weight:700;line-height:.98;letter-spacing:-.045em;margin:.7rem 0 0}.hero-title span{color:#8b604b}.hero-subtitle{margin-top:.75rem;color:#766d65;font-size:.92rem;line-height:1.55;max-width:660px}.hero-badges{display:flex;flex-wrap:wrap;gap:.5rem;margin-top:.95rem}.hero-badge{padding:.4rem .7rem;border-radius:999px;background:rgba(255,255,255,.78);border:1px solid var(--line);font-size:.72rem;color:#574e46;transition:.2s}.hero-badge:hover{transform:translateY(-2px);box-shadow:0 8px 16px rgba(74,58,44,.08)}
.stat{min-height:84px;padding:.95rem 1rem;border-radius:19px;border:1px solid var(--line);background:rgba(255,253,249,.78);box-shadow:0 9px 24px rgba(74,58,44,.06);transition:.2s}.stat:hover{transform:translateY(-4px);box-shadow:0 15px 28px rgba(74,58,44,.1)}.stat-icon{width:38px;height:38px;border-radius:50%;display:grid;place-items:center;background:#eee4d9;float:left;margin-right:.65rem}.stat-number{font-family:'Playfair Display', Georgia, serif;font-size:1.55rem;font-weight:700;line-height:1}.stat-label{color:#71675e;font-size:.76rem;margin-top:.2rem}.stat-note{color:#9a9087;font-size:.66rem;margin-top:.12rem}
.section-head{display:flex;justify-content:space-between;align-items:end;gap:1rem;margin:1.05rem 0 .6rem}.kicker{color:#967257;text-transform:uppercase;font-size:.66rem;font-weight:800;letter-spacing:.15em}.section-title{font-family:'Playfair Display', Georgia, serif;font-size:1.65rem;font-weight:700;margin-top:.15rem}.section-note{color:#8b8177;font-size:.74rem}

.topic-grid{display:none}.topic-card{position:relative;display:block;min-height:184px;padding:1.05rem 1rem 1rem;border:1px solid rgba(105,83,62,.12);border-radius:21px;text-decoration:none!important;color:#332d27!important;box-shadow:0 10px 24px rgba(74,58,44,.06);overflow:hidden;transition:transform .22s ease,box-shadow .22s ease,border-color .22s ease}.topic-card:before{content:"";position:absolute;width:92px;height:92px;right:-28px;top:-28px;border-radius:50%;background:rgba(255,255,255,.38)}.topic-card:hover{transform:translateY(-7px);box-shadow:0 20px 36px rgba(74,58,44,.13);border-color:rgba(139,98,72,.25)}.topic-card .topic-icon{font-size:2rem;display:block;margin-bottom:.55rem;filter:drop-shadow(0 4px 5px rgba(60,45,30,.08))}.topic-card .topic-num{position:absolute;right:.85rem;top:.75rem;font:700 .68rem 'Playfair Display', Georgia, serif;color:rgba(105,83,62,.5)}.topic-card h3{font:700 1.02rem 'Playfair Display', Georgia, serif;margin:0 0 .38rem;color:#332d27}.topic-card p{font-size:.72rem;line-height:1.45;color:#756a60;margin:0;max-width:170px}.topic-card .topic-arrow{position:absolute;left:1rem;bottom:.9rem;width:32px;height:32px;border-radius:50%;display:grid;place-items:center;background:rgba(255,255,255,.66);border:1px solid rgba(105,83,62,.1);font-size:1rem;transition:.2s}.topic-card:hover .topic-arrow{transform:translateX(4px)}.topic-1{background:linear-gradient(145deg,#f1f6ee,#e5efe3)}.topic-2{background:linear-gradient(145deg,#fbf1e9,#f6e2d7)}.topic-3{background:linear-gradient(145deg,#f4f0f7,#eae3f0)}.topic-4{background:linear-gradient(145deg,#edf3f5,#e1ecef)}


.fact-card,.popular-card,.tip-card{border:1px solid var(--line);border-radius:20px;background:rgba(255,253,249,.84);box-shadow:0 9px 22px rgba(74,58,44,.06)}.fact-card{padding:1rem;background:linear-gradient(145deg,#fff5d9,#fffaf0)}.fact-title,.popular-title{font-family:'Playfair Display', Georgia, serif;font-weight:700;font-size:.98rem}.fact-text{color:#62584f;line-height:1.55;font-size:.77rem;margin-top:.45rem}.popular-card{padding:.85rem;margin-top:.8rem}.popular-item{padding:.52rem .62rem;margin:.34rem 0;border-radius:12px;background:#f8f3ed;border:1px solid rgba(105,83,62,.07);font-size:.7rem;color:#544b43;transition:.2s}.popular-item:hover{transform:translateX(3px);background:#fffaf4}.tip-card{padding:.85rem;margin-top:.8rem}.tip-row{color:#665c53;font-size:.72rem;padding:.18rem 0}
.prompt-label{color:#8c6c52;font-size:.72rem;font-weight:700;letter-spacing:.04em;margin:.65rem 0 .35rem}.prompt-label + div [data-testid="stButton"] button{border-radius:999px!important;background:rgba(255,253,249,.82)!important;border:1px solid rgba(105,83,62,.10)!important;color:#6c5d50!important;font-size:.68rem!important;font-weight:500!important;min-height:40px!important;padding:.35rem .55rem!important;box-shadow:0 5px 14px rgba(74,58,44,.04)!important}.prompt-label + div [data-testid="stButton"] button:hover{transform:translateY(-2px)!important;background:#fffaf4!important;box-shadow:0 10px 20px rgba(74,58,44,.09)!important}
.question-shell{margin-top:.85rem;padding:1rem;border-radius:22px;border:1px solid var(--line);background:rgba(255,253,249,.82);box-shadow:0 11px 28px rgba(74,58,44,.07)}.question-head{display:flex;gap:.6rem;align-items:center}.ai-dot{width:38px;height:38px;border-radius:50%;display:grid;place-items:center;background:#e6ddd2}.question-title{font-family:'Playfair Display', Georgia, serif;font-size:1.22rem;font-weight:700}.question-sub{color:#8a8177;font-size:.71rem;margin-top:.08rem}.prompt-chip{display:inline-block;margin:.3rem .18rem 0 0;padding:.34rem .58rem;border-radius:999px;background:#f4eee7;border:1px solid rgba(105,83,62,.08);color:#6c5d50;font-size:.66rem}textarea{border-radius:15px!important;background:rgba(255,255,255,.84)!important}
.question-card{border-left:4px solid #8b6248;padding:.8rem 1rem;border-radius:0 15px 15px 0;background:rgba(244,235,226,.65);margin:.5rem 0 1rem}.source-card{border:1px solid rgba(86,116,91,.16);border-radius:15px;padding:.85rem 1rem;background:rgba(232,243,232,.65)}.empty-box{text-align:center;padding:1.8rem 1rem;border:1px dashed rgba(139,98,72,.25);border-radius:18px;color:#746a61;background:rgba(255,253,249,.65)}

/* Kartu topik Streamlit: struktur stabil */
.topic-visual{position:relative;min-height:158px;padding:1rem 1rem .62rem;border:1px solid rgba(105,83,62,.12);border-radius:20px 20px 8px 8px;box-shadow:0 10px 24px rgba(74,58,44,.06);overflow:hidden;margin-bottom:0}
.topic-visual:before{content:"";position:absolute;width:92px;height:92px;right:-28px;top:-28px;border-radius:50%;background:rgba(255,255,255,.38);pointer-events:none}
.topic-visual .topic-num{position:absolute;right:.85rem;top:.75rem;font:700 .68rem 'Playfair Display', Georgia, serif;color:rgba(105,83,62,.5)}
.topic-visual .topic-icon{font-size:2rem;display:block;margin-bottom:.45rem}
.topic-visual h3{font:700 1.02rem 'Playfair Display', Georgia, serif;margin:0 0 .38rem;color:#332d27}
.topic-visual p{font-size:.72rem;line-height:1.45;color:#756a60;margin:0;max-width:185px}
.topic-action .stButton>button{border-radius:0 0 10px 10px!important;border:1px solid rgba(105,83,62,.12)!important;border-top:0!important;min-height:38px!important;background:rgba(255,253,249,.82)!important;color:#6f513f!important;font-weight:700!important;box-shadow:0 10px 24px rgba(74,58,44,.06)!important}
.topic-action .stButton>button:hover{transform:translateY(-3px)!important;box-shadow:0 16px 30px rgba(74,58,44,.13)!important}
.topic-1-bg{background:linear-gradient(145deg,#f1f6ee,#e5efe3)}.topic-2-bg{background:linear-gradient(145deg,#fbf1e9,#f6e2d7)}.topic-3-bg{background:linear-gradient(145deg,#f4f0f7,#eae3f0)}.topic-4-bg{background:linear-gradient(145deg,#edf3f5,#e1ecef)}
@keyframes fadeUp{from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:translateY(0)}}
.topic-visual{animation:fadeUp .45s ease-out both}.topic-action{animation:fadeUp .45s ease-out both}.topic-action .stButton{margin-top:0!important}.topic-action .stButton>button{margin-top:0!important}
[data-testid="column"]{min-width:0}
@media(max-width:900px){.hero-title{font-size:2.45rem}.hero{padding:1.2rem 1.35rem}.section-head{align-items:flex-start;flex-direction:column;gap:.25rem}}
@media(max-width:700px){
    .hero{
        padding:1rem .85rem;
        border-radius:16px;
        margin-bottom:1rem;
    }

    .hero-title{
        font-size:1.8rem;
        line-height:1.15;
        margin-bottom:.5rem;
    }

    .hero:after{
        font-size:2rem;
    }

    .hero-badges{
        gap:.3rem;
        flex-wrap:wrap;
    }

    .section-head{
        gap:.2rem;
        margin-bottom:.7rem;
    }

    .section-title{
        font-size:1.3rem;
        line-height:1.25;
    }

    .section-subtitle{
        font-size:.85rem;
        line-height:1.4;
    }

    .stButton>button{
        min-height:44px;
        font-size:.85rem;
        padding:.55rem .7rem;
    }

    textarea{
        font-size:16px!important;
    }

    [data-testid="stTextArea"]{
        width:100%;
    }

    [data-testid="column"]{
        width:100%!important;
        flex:1 1 100%!important;
        min-width:100%!important;
    }

    .question-shell{
        padding:.9rem;
        border-radius:14px;
    }

    .question-title{
        font-size:1rem;
    }

    .question-sub{
        font-size:.8rem;
        line-height:1.4;
    }
}
.stButton>button{border-radius:12px;transition:transform .18s ease,box-shadow .18s ease}.stButton>button:hover{transform:translateY(-2px);box-shadow:0 7px 18px rgba(74,58,44,.10)}.stButton>button[kind='primary']{background:#8b6248!important;border:1px solid #8b6248!important;color:white!important;box-shadow:0 8px 18px rgba(139,98,72,.18)!important}.stButton>button[kind='primary']:hover{background:#76513c!important;border-color:#76513c!important;box-shadow:0 12px 24px rgba(139,98,72,.25)!important}
.topic-card,.topic-card:visited,.topic-card:hover,.topic-card:active{color:#332d27!important;text-decoration:none!important}
.topic-card{cursor:pointer}
</style>
""",unsafe_allow_html=True)

FOLDER_DATABASE = "database"

# =========================================================
# SESSION
# =========================================================
if "riwayat" not in st.session_state:
    st.session_state.riwayat = []

# =========================================================
# DATABASE
# =========================================================
@st.cache_data
def baca_database():
    data = []

    if not os.path.exists(FOLDER_DATABASE):
        os.makedirs(FOLDER_DATABASE)

    for nama_file in sorted(os.listdir(FOLDER_DATABASE)):
        if nama_file.lower().endswith(".txt"):
            lokasi = os.path.join(FOLDER_DATABASE, nama_file)

            try:
                with open(lokasi, "r", encoding="utf-8") as file:
                    isi = file.read()

                data.append({
                    "nama_file": nama_file,
                    "isi": isi
                })
            except Exception as error:
                st.error(f"Gagal membaca {nama_file}: {error}")

    return data


STOPWORDS = {
    "yang", "dan", "di", "ke", "dari", "pada", "dengan", "untuk",
    "dalam", "adalah", "itu", "ini", "atau", "apa", "bagaimana",
    "mengapa", "sebutkan", "jelaskan", "jelaskanlah", "tentang",
    "suatu", "sebuah", "secara", "merupakan", "dapat", "akan",
    "sebagai", "oleh", "lebih", "juga", "tidak", "tersebut",
    "maksud", "dimaksud", "berikut", "yaitu", "yakni", "tolong",
    "jelas", "jelaskanlah", "uraikan", "uraikanlah", "pengertian"
}

QUESTION_WORDS = {
    "apa", "bagaimana", "mengapa", "kapan", "siapa", "sebutkan",
    "jelaskan", "jelaskanlah", "uraikan", "uraikanlah", "terangkan",
    "terangkanlah", "maksud", "dimaksud", "pengertian"
}


def bersihkan_teks(teks):
    teks = teks.lower()
    teks = re.sub(r"[^a-zA-ZÀ-ÿ0-9\s]", " ", teks)
    teks = re.sub(r"\s+", " ", teks)
    return teks.strip()


def token(teks):
    return bersihkan_teks(teks).split()


def ambil_kata_kunci(pertanyaan):
    return [
        kata for kata in token(pertanyaan)
        if len(kata) > 2 and kata not in STOPWORDS
    ]


def ambil_frasa_utama(pertanyaan, isi_dokumen=""):
    """
    Mengambil frasa inti dari pertanyaan.
    Untuk:
    'Apa yang dimaksud dengan kalimat efektif?'
    target menjadi 'kalimat efektif', bukan kata 'kalimat' dan 'efektif'
    secara terpisah.
    """
    kata = token(pertanyaan)

    kandidat = []
    for n in range(min(5, len(kata)), 1, -1):
        for i in range(len(kata) - n + 1):
            bagian = kata[i:i+n]

            if any(k in QUESTION_WORDS for k in bagian):
                continue

            if sum(len(k) > 2 for k in bagian) < 2:
                continue

            frasa = " ".join(bagian)

            if not isi_dokumen or frasa in bersihkan_teks(isi_dokumen):
                kandidat.append(frasa)

        if kandidat:
            return max(kandidat, key=len)

    inti = [k for k in kata if k not in QUESTION_WORDS and len(k) > 2]
    return " ".join(inti[:5])


def frasa_pertanyaan(pertanyaan):
    kata = ambil_kata_kunci(pertanyaan)

    frasa = []
    for n in (4, 3, 2):
        for i in range(len(kata) - n + 1):
            bagian = kata[i:i+n]
            if len(bagian) == n:
                frasa.append(" ".join(bagian))

    return frasa


def hitung_relevansi(pertanyaan, isi, nama_file=""):
    teks = bersihkan_teks(isi)
    kata_kunci = ambil_kata_kunci(pertanyaan)

    if not kata_kunci:
        return 0

    frekuensi = Counter(teks.split())
    skor = 0

    # 1. Frasa inti mendapat bobot sangat tinggi.
    frasa_utama = ambil_frasa_utama(pertanyaan, isi)
    if frasa_utama:
        jumlah_frasa = teks.count(frasa_utama)
        skor += min(jumlah_frasa, 3) * 35

    # 2. Frasa 2-4 kata.
    for frasa in frasa_pertanyaan(pertanyaan):
        if frasa in teks:
            skor += 12

    # 3. Coverage kata kunci.
    ditemukan = 0
    for kata in set(kata_kunci):
        if kata in frekuensi:
            ditemukan += 1
            skor += min(frekuensi[kata], 6)

    if kata_kunci:
        coverage = ditemukan / len(set(kata_kunci))
        skor += int(coverage * 25)

    # 4. Bonus jika target muncul di bagian awal / judul materi.
    awal = teks[:900]
    if frasa_utama and frasa_utama in awal:
        skor += 18

    # 5. Nama file juga dipertimbangkan.
    nama_bersih = bersihkan_teks(nama_file.replace(".txt", "").replace("_", " "))
    skor += sum(4 for kata in set(kata_kunci) if kata in nama_bersih)

    return skor


def cari_materi(pertanyaan, database):
    hasil = []

    for data in database:
        skor = hitung_relevansi(
            pertanyaan,
            data["isi"],
            data["nama_file"]
        )

        if skor > 0:
            hasil.append({
                "nama_file": data["nama_file"],
                "isi": data["isi"],
                "skor": skor
            })

    hasil.sort(key=lambda x: x["skor"], reverse=True)
    return hasil


# =========================================================
# PEMECAHAN KONTEN
# =========================================================
def pecah_blok(isi):
    """
    Memecah TXT menjadi blok yang cukup kecil agar mesin tidak
    mengambil daftar pokok materi panjang sebagai jawaban.
    """
    isi = isi.replace("\r\n", "\n").replace("\r", "\n")
    bagian = re.split(r"\n\s*\n+", isi)

    hasil = []

    for bagian_teks in bagian:
        bagian_teks = bagian_teks.strip()

        if not bagian_teks:
            continue

        # Jika blok sangat panjang, pecah berdasarkan baris.
        if len(bagian_teks) > 1800:
            baris = [b.strip() for b in bagian_teks.split("\n") if b.strip()]
            sementara = ""

            for b in baris:
                if len(sementara) + len(b) + 1 <= 1000:
                    sementara += b + "\n"
                else:
                    if sementara.strip():
                        hasil.append(sementara.strip())
                    sementara = b + "\n"

            if sementara.strip():
                hasil.append(sementara.strip())
        else:
            hasil.append(bagian_teks)

    return hasil


def skor_blok(pertanyaan, blok):
    teks = bersihkan_teks(blok)
    pertanyaan_bersih = bersihkan_teks(pertanyaan)
    kata_kunci = ambil_kata_kunci(pertanyaan)

    # =====================================================
    # MODE DEFINISI: HARUS ADA TARGET YANG BENAR-BENAR
    # DIBAHAS DI BLOK INI.
    #
    # Contoh:
    # "Apa yang dimaksud dengan kalimat efektif?"
    # TIDAK BOLEH mengambil paragraf tentang "Klausa adalah..."
    # hanya karena kata "kalimat" muncul.
    # =====================================================
    pertanyaan_definisi = any(
        x in pertanyaan_bersih
        for x in [
            "apa yang dimaksud",
            "pengertian",
            "definisi",
            "apa itu"
        ]
    )

    if pertanyaan_definisi:
        # Ambil objek setelah pola pertanyaan.
        pola = re.search(
            r"(?:apa yang dimaksud dengan|pengertian|definisi|apa itu)\s+(.+)",
            pertanyaan_bersih
        )

        target = pola.group(1).strip() if pola else ""
        target = re.sub(r"\s+", " ", target).strip()

        # Hapus tanda/kata tanya sisa jika ada.
        target = re.sub(r"\b(adalah|itu|tersebut)\b$", "", target).strip()

        # TARGET WAJIB muncul sebagai frasa utuh.
        if target and target not in teks:
            return 0

        # Jika target hanya muncul di daftar "Pokok Materi",
        # itu bukan definisi.
        if "pokok materi" in teks and not re.search(
            r"\b" + re.escape(target) +
            r"\b.{0,80}\b(adalah|merupakan|ialah|yaitu)\b",
            teks
        ):
            return 0

        skor = 0

        # Kecocokan frasa target.
        skor += 120

        # Definisi langsung mendapat bobot tertinggi.
        if re.search(
            r"\b" + re.escape(target) +
            r"\b.{0,100}\b(adalah|merupakan|ialah|yaitu)\b",
            teks
        ):
            skor += 150

        # Jika kalimat definisi berada sebelum/di sekitar target.
        if re.search(
            r"\b(adalah|merupakan|ialah|yaitu)\b.{0,100}\b" +
            re.escape(target) + r"\b",
            teks
        ):
            skor += 100

        # Sedikit bonus untuk kata kunci lain.
        for kata in set(kata_kunci):
            if kata in teks:
                skor += 3

        return skor

    # =====================================================
    # MODE PERTANYAAN UMUM
    # =====================================================
    frasa_utama = ambil_frasa_utama(pertanyaan, blok)
    skor = 0

    if frasa_utama and frasa_utama in teks:
        skor += 100

    for frasa in frasa_pertanyaan(pertanyaan):
        if frasa in teks:
            skor += 15

    for kata in set(kata_kunci):
        if kata in teks:
            skor += 7

    if "pokok materi" in teks:
        skor -= 45

    return max(skor, 0)


def ambil_jawaban_relevan(pertanyaan, isi, maksimum=1800):
    blok = pecah_blok(isi)

    if not blok:
        return ""

    dinilai = []
    for nomor, bagian in enumerate(blok):
        skor = skor_blok(pertanyaan, bagian)
        if skor > 0:
            dinilai.append((skor, nomor, bagian))

    dinilai.sort(key=lambda x: (-x[0], x[1]))

    if not dinilai:
        return ""

    # Jika ada blok yang sangat kuat karena frasa inti, utamakan.
    terbaik = dinilai[0]
    hasil = terbaik[2].strip()

    # Tambahkan satu blok berikutnya hanya jika masih sangat relevan
    # dan membantu menjelaskan konteks.
    for skor, nomor, bagian in dinilai[1:]:
        if skor < max(20, terbaik[0] * 0.38):
            continue

        tambahan = bagian.strip()

        # Jangan mengulang blok yang sama.
        if tambahan == hasil:
            continue

        if len(hasil) + len(tambahan) + 2 <= maksimum:
            hasil += "\n\n" + tambahan

        if len(hasil) >= maksimum:
            break

    return hasil[:maksimum].strip()


def fallback_jawaban(pertanyaan, isi, maksimum=1400):
    """
    Fallback hanya untuk pertanyaan umum.
    Untuk pertanyaan definisi, jangan mengembalikan paragraf yang
    tidak benar-benar membahas objek yang ditanyakan.
    """
    pertanyaan_bersih = bersihkan_teks(pertanyaan)

    if any(
        x in pertanyaan_bersih
        for x in ["apa yang dimaksud", "pengertian", "definisi", "apa itu"]
    ):
        return ""

    paragraf = pecah_blok(isi)
    kata_kunci = ambil_kata_kunci(pertanyaan)

    kandidat = []

    for nomor, p in enumerate(paragraf):
        teks = bersihkan_teks(p)
        skor = sum(1 for kata in kata_kunci if kata in teks)

        if skor:
            kandidat.append((skor, nomor, p))

    kandidat.sort(key=lambda x: (-x[0], x[1]))

    if not kandidat:
        return ""

    hasil = ""
    for _, _, p in kandidat:
        if len(hasil) + len(p) + 2 <= maksimum:
            hasil += p.strip() + "\n\n"

    return hasil.strip()


def nama_materi(nama_file):
    nama = nama_file.replace(".txt", "")
    nama = nama.replace("_", " ")
    nama = re.sub(r"\s+", " ", nama)
    return nama.strip().title()


# =========================================================
# LOAD
# =========================================================
database = baca_database()

# =========================================================
# TOPIK CEPAT
# =========================================================
_topik_map = {
    "tata-bahasa": "Jelaskan pengertian tata bahasa.",
    "kalimat": "Apa yang dimaksud dengan kalimat efektif?",
    "paragraf": "Apa yang dimaksud dengan paragraf?",
    "keterampilan": "Jelaskan keterampilan membaca.",
}

# =========================================================
# SIDEBAR
# =========================================================
with st.sidebar:
    st.markdown(r"""
    <div class="brand"><div class="brand-icon">📚</div><div><div class="brand-name">AI Tutor<br>Bahasa Indonesia</div><div class="brand-sub">Belajar Lebih Dalam, Lebih Bermakna</div></div></div>
    """, unsafe_allow_html=True)
    st.markdown("<div class='side-item active'>⌂ &nbsp; Beranda</div><div class='side-item'>▣ &nbsp; Knowledge Base</div><div class='side-item'>▤ &nbsp; Daftar Materi</div><div class='side-item'>◷ &nbsp; Riwayat Sesi</div><div class='side-item'>ⓘ &nbsp; Tentang Aplikasi</div>", unsafe_allow_html=True)
    st.divider()
    st.markdown("**Status Database**")
    st.markdown(f'<div class="side-status">🟢 <strong>Database aktif</strong><br><span style="color:#7d746b;font-size:.74rem;">{len(database)} materi tersedia</span></div>', unsafe_allow_html=True)
    with st.expander("📖 Daftar semua materi"):
        for data in database:
            st.write("📄 " + nama_materi(data["nama_file"]))
    st.markdown(r"""
    <div class="quote">“Bahasa adalah jembatan untuk memahami dunia.”<small>— AI Tutor</small></div>
    """, unsafe_allow_html=True)
    st.write("")
    if st.button("🗑️ Hapus semua riwayat", use_container_width=True):
        st.session_state.riwayat=[]
        st.rerun()
    st.caption("AI Tutor Bahasa Indonesia • Python • Streamlit")

# =========================================================
# DEKORASI + HERO
# =========================================================
st.markdown('<div class="paper-dots"></div><div class="app-orb orb-a"></div><div class="app-orb orb-b"></div>', unsafe_allow_html=True)
st.markdown(f"""
<div class="hero"><div class="hero-inner">
<div class="welcome-pill">☀️ &nbsp; Selamat datang &nbsp;•&nbsp; Mari belajar hari ini</div>
<div class="hero-title">AI Tutor<br><span>Bahasa Indonesia</span></div>
<div class="hero-subtitle">Belajar Bahasa Indonesia dengan cara yang lebih mudah, terarah, dan interaktif. Temukan penjelasan dari materi yang paling relevan.</div>
<div class="hero-badges"><span class="hero-badge">📚 {len(database)} Materi</span><span class="hero-badge">🎯 Jawaban Relevan</span><span class="hero-badge">⚡ Berbasis AI</span><span class="hero-badge">💚 Gratis & Mudah Digunakan</span></div>
</div></div>
""", unsafe_allow_html=True)

c1,c2,c3=st.columns(3)
with c1: st.markdown(f'<div class="stat"><div class="stat-icon">📚</div><div class="stat-number">{len(database)}</div><div class="stat-label">Materi Knowledge Base</div><div class="stat-note">Materi lengkap dan terstruktur</div></div>',unsafe_allow_html=True)
with c2: st.markdown(f'<div class="stat"><div class="stat-icon">💬</div><div class="stat-number">{len(st.session_state.riwayat)}</div><div class="stat-label">Pertanyaan dalam sesi</div><div class="stat-note">Mulai ajukan pertanyaanmu!</div></div>',unsafe_allow_html=True)
with c3: st.markdown('<div class="stat"><div class="stat-icon">🎯</div><div class="stat-number" style="font-size:1.05rem;margin-top:.18rem;">Pencarian relevan</div><div class="stat-label">Berbasis frasa & relevansi</div><div class="stat-note">Temukan jawaban yang tepat</div></div>',unsafe_allow_html=True)

left,right=st.columns([3.05,1.05],gap="large")
with left:
    st.markdown('<div class="section-head"><div><div class="kicker">Jelajahi</div><div class="section-title">Apa yang ingin kamu pelajari?</div></div><div class="section-note">Pilih topik atau langsung tanyakan pada AI Tutor.</div></div>',unsafe_allow_html=True)
    _topik=[
        ("📖","Tata Bahasa","Pelajari struktur dan penggunaan bahasa.","Jelaskan tentang tata bahasa Indonesia.","topic-1-bg"),
        ("✍️","Kalimat","Pahami kalimat, klausa, dan kalimat efektif.","Apa yang dimaksud dengan kalimat efektif?","topic-2-bg"),
        ("📝","Paragraf & Wacana","Kenali susunan gagasan dalam teks.","Jelaskan pengertian paragraf.","topic-3-bg"),
        ("🎤","Keterampilan Berbahasa","Eksplorasi membaca, menulis, menyimak, dan berbicara.","Jelaskan keterampilan berbahasa dalam Bahasa Indonesia.","topic-4-bg"),
    ]
    cols=st.columns(4,gap="small")
    for idx,(icon,title,desc,question,bg) in enumerate(_topik):
        with cols[idx]:
            st.markdown(f'<div class="topic-visual {bg}"><span class="topic-num">0{idx+1}</span><span class="topic-icon">{icon}</span><h3>{title}</h3><p>{desc}</p></div>',unsafe_allow_html=True)
            if st.button("Jelajahi  →",key=f"topic_{idx}",use_container_width=True):
                st.session_state.pertanyaan_terpilih=question
                st.rerun()

with right:
    st.markdown('<div class="fact-card"><div class="fact-title">💡 Tahukah Kamu?</div><div class="fact-text">Kalimat efektif dapat menyampaikan gagasan secara tepat, jelas, dan tidak berlebihan.</div></div>',unsafe_allow_html=True)
    st.markdown('<div class="popular-card"><div class="popular-title">🔥 Pertanyaan Populer</div><div class="popular-item">Apa yang dimaksud dengan kalimat efektif?　→</div><div class="popular-item">Jelaskan pengertian paragraf.　→</div><div class="popular-item">Apa saja jenis-jenis teks?　→</div></div>',unsafe_allow_html=True)
    st.markdown('<div class="tip-card"><div class="popular-title">✨ Tips Bertanya</div><div class="tip-row">✓ Gunakan kalimat yang jelas</div><div class="tip-row">✓ Sebutkan topik yang kamu maksud</div></div>',unsafe_allow_html=True)

# =========================================================
# PERTANYAAN + INPUT
# =========================================================
# Gunakan session_state untuk menjaga isi kotak pertanyaan tetap
# ada setelah Streamlit melakukan rerun ketika tombol ditekan.
if "pertanyaan_input" not in st.session_state:
    st.session_state.pertanyaan_input = ""

if "pertanyaan_terpilih" in st.session_state:
    st.session_state.pertanyaan_input = st.session_state.pop("pertanyaan_terpilih")

st.markdown('<div class="prompt-label">✨ Coba pertanyaan ini</div>', unsafe_allow_html=True)
prompt_cols = st.columns(4, gap="small")
contoh=[
    "Apa itu kalimat efektif?",
    "Jelaskan pengertian paragraf.",
    "Apa yang dimaksud dengan teks?",
    "Bagaimana cara menulis yang baik?"
]
for i, p in enumerate(contoh):
    with prompt_cols[i]:
        if st.button(p, key=f"prompt_{i}", use_container_width=True):
            st.session_state.pertanyaan_input = p
            st.rerun()

def bersihkan_pertanyaan():
    st.session_state.riwayat = []
    st.session_state.pertanyaan_input = ""

st.markdown(r'<div class="question-shell"><div class="question-head"><div class="ai-dot">🤖</div><div><div class="question-title">Tanyakan kepada AI Tutor</div><div class="question-sub">Ketik pertanyaanmu di bawah ini. AI akan mencari jawaban dari materi yang paling relevan.</div></div></div></div>',unsafe_allow_html=True)
pertanyaan=st.text_area(
    "Pertanyaan",
    key="pertanyaan_input",
    placeholder="Apa yang ingin kamu ketahui?",
    height=95,
    label_visibility="collapsed"

)


col_tanya,col_bersih=st.columns([4,1])
with col_tanya:
    tombol_tanya=st.button("➤  TANYAKAN",type="primary",use_container_width=True)
with col_bersih:
    st.button (
        "↺ Bersihkan",
        use_container_width=True,
        on_click=bersihkan_pertanyaan
    )

# =========================================================
# PROSES
# =========================================================
if tombol_tanya:
    if not pertanyaan.strip():
        st.warning("Silakan masukkan pertanyaan terlebih dahulu.")

    elif not database:
        st.error("Database TXT belum ditemukan.")

    else:
        with st.spinner("🎯 Mencari bagian materi yang paling relevan..."):
            hasil = cari_materi(pertanyaan, database)

        if hasil:
            utama = hasil[0]

            jawaban = ambil_jawaban_relevan(
                pertanyaan,
                utama["isi"],
                1800
            )

            if not jawaban:
                jawaban = fallback_jawaban(
                    pertanyaan,
                    utama["isi"],
                    1400
                )

            st.session_state.riwayat.insert(0, {
                "pertanyaan": pertanyaan.strip(),
                "jawaban": jawaban,
                "sumber": utama["nama_file"],
                "skor": utama["skor"],
                "terkait": hasil[1:4]
            })

        else:
            st.session_state.riwayat.insert(0, {
                "pertanyaan": pertanyaan.strip(),
                "jawaban": None,
                "sumber": None,
                "skor": 0,
                "terkait": []
            })

# =========================================================
# HASIL
# =========================================================
if st.session_state.riwayat:
    st.divider()
    st.markdown("### 🤖 Hasil Pembelajaran")

    for nomor, item in enumerate(st.session_state.riwayat):
        st.markdown(
            f'<div class="question-card"><strong>👤 Anda</strong><br>'
            f'{item["pertanyaan"]}</div>',
            unsafe_allow_html=True
        )

        if item["jawaban"]:
            st.markdown("#### 🤖 AI Tutor")

            # Sengaja menggunakan Markdown biasa agar teks dari TXT
            # tetap terbaca sebagai paragraf, bukan HTML mentah.
            st.markdown(item["jawaban"])

            st.write("")

            st.markdown("#### 📚 Sumber Utama")
            st.markdown(
                f'<div class="source-card">'
                f'📄 <strong>{nama_materi(item["sumber"])}</strong>'
                f'<br><span style="color:#64748b;font-size:.85rem;">'
                f'Bagian materi dengan relevansi tertinggi.'
                f'</span></div>',
                unsafe_allow_html=True
            )

            if item["terkait"]:
                st.write("")
                with st.expander("📑 Lihat materi terkait"):
                    for terkait in item["terkait"]:
                        st.markdown(
                            f"**📄 {nama_materi(terkait['nama_file'])}**"
                        )

                        potongan_terkait = ambil_jawaban_relevan(
                            item["pertanyaan"],
                            terkait["isi"],
                            850
                        )

                        if not potongan_terkait:
                            potongan_terkait = fallback_jawaban(
                                item["pertanyaan"],
                                terkait["isi"],
                                850
                            )

                        st.write(potongan_terkait or "Tidak ada bagian yang cukup relevan.")

                        st.divider()

        else:
            st.markdown("""
            <div class="empty-box">
                <strong>🔍 Materi belum ditemukan</strong><br>
                Coba gunakan kata kunci yang lebih spesifik sesuai materi
                Bahasa Indonesia yang tersedia.
            </div>
            """, unsafe_allow_html=True)

        if nomor < len(st.session_state.riwayat) - 1:
            st.divider()

# =========================================================
# PENUTUP
# =========================================================
st.write("")
st.markdown("""
<div class="fact-card">
    <div class="fact-label">📚 Terus Belajar</div>
    <div class="fact-text">
        Jelajahi materi, ajukan pertanyaan, dan gunakan AI Tutor sebagai teman belajar Bahasa Indonesia.
    </div>
</div>
""", unsafe_allow_html=True)

# =========================================================
# TENTANG
# =========================================================
st.divider()

with st.expander("ℹ️ Tentang aplikasi"):
    st.write(
        "AI Tutor Bahasa Indonesia menggunakan Knowledge Base TXT. "
        "Sistem memprioritaskan kecocokan frasa, kata kunci, dan bagian "
        "materi yang paling relevan. Sistem tidak menambahkan informasi "
        "dari luar Knowledge Base."
    )
    st.caption(f"Knowledge Base aktif: {len(database)} file TXT")

st.caption(
    "AI Tutor Bahasa Indonesia • Python + Streamlit + TXT Knowledge Base"
)
