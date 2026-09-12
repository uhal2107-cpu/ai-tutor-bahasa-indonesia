import streamlit as st
import os
import re
from collections import Counter

# =========================================================
# KONFIGURASI HALAMAN
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
st.markdown("""
<style>
    .main-title {
        font-size: 2.5rem;
        font-weight: 800;
        margin-bottom: 0.15rem;
    }
    .subtitle {
        color: #64748b;
        font-size: 1.05rem;
        margin-bottom: 1.5rem;
    }
    .stat-card {
        padding: 1rem 1.1rem;
        border: 1px solid rgba(128,128,128,.22);
        border-radius: 14px;
        background: rgba(128,128,128,.06);
        min-height: 95px;
    }
    .stat-number {
        font-size: 1.8rem;
        font-weight: 800;
        line-height: 1.1;
    }
    .stat-label {
        color: #64748b;
        font-size: .9rem;
    }
    .answer-box {
        padding: 1.2rem 1.3rem;
        border-radius: 16px;
        border: 1px solid rgba(128,128,128,.22);
        background: rgba(128,128,128,.05);
        line-height: 1.7;
    }
    .source-box {
        padding: .9rem 1rem;
        border-radius: 12px;
        border: 1px solid rgba(128,128,128,.20);
    }
    .chat-question {
        padding: .8rem 1rem;
        border-radius: 14px;
        border: 1px solid rgba(128,128,128,.18);
        background: rgba(128,128,128,.04);
        margin-bottom: .7rem;
    }
    .small-muted {
        color: #64748b;
        font-size: .85rem;
    }
    div.stButton > button {
        border-radius: 10px;
        font-weight: 650;
    }
</style>
""", unsafe_allow_html=True)

# =========================================================
# KONFIGURASI DATABASE
# =========================================================
FOLDER_DATABASE = "database"

# =========================================================
# SESSION STATE
# =========================================================
if "riwayat" not in st.session_state:
    st.session_state.riwayat = []

# =========================================================
# FUNGSI DATABASE
# =========================================================
@st.cache_data
def baca_database():
    data = []

    if not os.path.exists(FOLDER_DATABASE):
        os.makedirs(FOLDER_DATABASE)

    for nama_file in sorted(os.listdir(FOLDER_DATABASE)):
        if nama_file.lower().endswith(".txt"):
            lokasi_file = os.path.join(FOLDER_DATABASE, nama_file)

            try:
                with open(lokasi_file, "r", encoding="utf-8") as file:
                    isi = file.read()

                data.append({
                    "nama_file": nama_file,
                    "isi": isi,
                })
            except Exception as error:
                st.error(f"Gagal membaca {nama_file}: {error}")

    return data

# =========================================================
# PEMBERSIHAN TEKS
# =========================================================
def bersihkan_teks(teks):
    teks = teks.lower()
    teks = re.sub(r"[^a-zA-ZÀ-ÿ0-9\s]", " ", teks)
    teks = re.sub(r"\s+", " ", teks)
    return teks.strip()

STOPWORDS = {
    "yang", "dan", "di", "ke", "dari", "pada", "dengan", "untuk",
    "dalam", "adalah", "itu", "ini", "atau", "apa", "bagaimana",
    "mengapa", "sebutkan", "jelaskan", "jelaskanlah", "tentang",
    "suatu", "sebuah", "secara", "merupakan", "dapat", "akan",
    "sebagai", "oleh", "lebih", "juga", "tidak", "tersebut",
    "maksud", "dimaksud", "berikut", "yaitu", "yakni"
}

# =========================================================
# KATA KUNCI
# =========================================================
def ambil_kata_kunci(pertanyaan):
    teks = bersihkan_teks(pertanyaan)
    kata = teks.split()

    return [
        item for item in kata
        if len(item) > 2 and item not in STOPWORDS
    ]

# =========================================================
# RELEVANSI
# =========================================================
def hitung_relevansi(pertanyaan, isi):
    kata_kunci = ambil_kata_kunci(pertanyaan)

    if not kata_kunci:
        return 0

    teks_database = bersihkan_teks(isi)
    kata_database = teks_database.split()
    frekuensi = Counter(kata_database)

    skor = 0

    for kata in kata_kunci:
        if kata in frekuensi:
            jumlah = min(frekuensi[kata], 10)
            skor += jumlah

    pertanyaan_bersih = bersihkan_teks(pertanyaan)

    if len(pertanyaan_bersih) > 8 and pertanyaan_bersih in teks_database:
        skor += 20

    # Bonus apabila beberapa kata kunci muncul di bagian awal materi
    bagian_awal = teks_database[:800]
    for kata in kata_kunci:
        if kata in bagian_awal:
            skor += 5

    # Bonus untuk kemunculan kata kunci unik
    kata_unik = set(kata_kunci)
    jumlah_cocok = sum(1 for kata in kata_unik if kata in teks_database)
    skor += jumlah_cocok * 2

    return skor

# =========================================================
# PENCARIAN
# =========================================================
def cari_materi(pertanyaan, database):
    hasil = []

    for data in database:
        skor = hitung_relevansi(pertanyaan, data["isi"])

        if skor > 0:
            hasil.append({
                "nama_file": data["nama_file"],
                "isi": data["isi"],
                "skor": skor,
            })

    hasil.sort(key=lambda x: x["skor"], reverse=True)
    return hasil

# =========================================================
# POTONGAN RELEVAN
# =========================================================
def ambil_potongan_relevan(pertanyaan, isi, jumlah_maksimal=1600):
    kata_kunci = ambil_kata_kunci(pertanyaan)

    paragraf = re.split(r"\n\s*\n|\r\n", isi)
    paragraf_relevan = []

    for p in paragraf:
        p_bersih = bersihkan_teks(p)
        skor = sum(1 for kata in kata_kunci if kata in p_bersih)

        if skor > 0:
            paragraf_relevan.append((skor, p.strip()))

    paragraf_relevan.sort(key=lambda x: x[0], reverse=True)

    hasil = ""

    for _, p in paragraf_relevan:
        if len(hasil) + len(p) <= jumlah_maksimal:
            hasil += p + "\n\n"

    if not hasil.strip():
        hasil = isi[:jumlah_maksimal]

    return hasil.strip()

# =========================================================
# NAMA MATERI
# =========================================================
def nama_materi(nama_file):
    nama = nama_file.replace(".txt", "")
    nama = nama.replace("_", " ")
    nama = re.sub(r"\s+", " ", nama)
    return nama.strip().title()

# =========================================================
# LOAD DATABASE
# =========================================================
database = baca_database()

# =========================================================
# SIDEBAR
# =========================================================
with st.sidebar:
    st.markdown("## 📚 AI Tutor")
    st.caption("Knowledge Base Bahasa Indonesia")

    st.divider()

    st.markdown("### 📊 Database")
    st.metric("Materi tersedia", len(database))

    if database:
        st.success("Database aktif")

        with st.expander("📖 Lihat semua materi", expanded=False):
            for data in database:
                st.write("📄 " + nama_materi(data["nama_file"]))
    else:
        st.warning("Belum ada file TXT.")

    st.divider()

    if st.button("🗑️ Hapus riwayat", use_container_width=True):
        st.session_state.riwayat = []
        st.rerun()

    st.divider()
    st.caption("Python • Streamlit • TXT Knowledge Base")

# =========================================================
# HEADER
# =========================================================
st.markdown(
    '<div class="main-title">📚 AI Tutor Bahasa Indonesia</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="subtitle">Temukan penjelasan dari 20 materi Bahasa Indonesia dalam satu tempat.</div>',
    unsafe_allow_html=True,
)

# =========================================================
# STATISTIK
# =========================================================
c1, c2, c3 = st.columns(3)

with c1:
    st.markdown(
        f'<div class="stat-card"><div class="stat-number">{len(database)}</div>'
        '<div class="stat-label">Materi dalam Knowledge Base</div></div>',
        unsafe_allow_html=True,
    )

with c2:
    st.markdown(
        f'<div class="stat-card"><div class="stat-number">{len(st.session_state.riwayat)}</div>'
        '<div class="stat-label">Pertanyaan sesi ini</div></div>',
        unsafe_allow_html=True,
    )

with c3:
    st.markdown(
        '<div class="stat-card"><div class="stat-number">🔎</div>'
        '<div class="stat-label">Pencarian berbasis relevansi</div></div>',
        unsafe_allow_html=True,
    )

st.write("")

# =========================================================
# PERTANYAAN CONTOH
# =========================================================
st.markdown("### 💡 Mulai dengan pertanyaan")

contoh = [
    "Apa yang dimaksud dengan kalimat efektif?",
    "Apa yang dimaksud dengan paragraf?",
    "Jelaskan keterampilan membaca.",
]

cols = st.columns(3)

for i, pertanyaan_contoh in enumerate(contoh):
    with cols[i]:
        if st.button(pertanyaan_contoh, key=f"contoh_{i}", use_container_width=True):
            st.session_state.pertanyaan_terpilih = pertanyaan_contoh
            st.rerun()

pertanyaan_default = st.session_state.pop("pertanyaan_terpilih", "")

# =========================================================
# INPUT
# =========================================================
st.markdown("### 💬 Tanyakan kepada AI Tutor")

pertanyaan = st.text_area(
    "Pertanyaan",
    value=pertanyaan_default,
    placeholder="Contoh: Apa yang dimaksud dengan kalimat efektif?",
    height=110,
    label_visibility="collapsed",
)

tanya, kosong = st.columns([4, 1])

with tanya:
    tombol = st.button("🔍 TANYAKAN", type="primary", use_container_width=True)

with kosong:
    if st.button("↺ Bersihkan", use_container_width=True):
        st.session_state.riwayat = []
        st.rerun()

# =========================================================
# PROSES
# =========================================================
if tombol:
    if not pertanyaan.strip():
        st.warning("Silakan masukkan pertanyaan terlebih dahulu.")
    elif not database:
        st.error("Database TXT belum ditemukan.")
    else:
        with st.spinner("🔎 Mencari materi yang paling relevan..."):
            hasil = cari_materi(pertanyaan, database)

        if hasil:
            utama = hasil[0]
            jawaban = ambil_potongan_relevan(
                pertanyaan,
                utama["isi"],
                1800,
            )

            st.session_state.riwayat.insert(
                0,
                {
                    "pertanyaan": pertanyaan.strip(),
                    "jawaban": jawaban,
                    "sumber": utama["nama_file"],
                    "skor": utama["skor"],
                    "terkait": hasil[1:4],
                },
            )
        else:
            st.session_state.riwayat.insert(
                0,
                {
                    "pertanyaan": pertanyaan.strip(),
                    "jawaban": None,
                    "sumber": None,
                    "skor": 0,
                    "terkait": [],
                },
            )

# =========================================================
# RIWAYAT / HASIL
# =========================================================
if st.session_state.riwayat:
    st.divider()
    st.markdown("### 🤖 Hasil Pembelajaran")

    for index, item in enumerate(st.session_state.riwayat):
        st.markdown(
            f'<div class="chat-question"><strong>👤 Anda</strong><br>'
            f'{item["pertanyaan"]}</div>',
            unsafe_allow_html=True,
        )

        if item["jawaban"]:
            st.markdown("#### 🤖 AI Tutor")

            st.markdown(
                f'<div class="answer-box">{item["jawaban"]}</div>',
                unsafe_allow_html=True,
            )

            st.write("")

            st.markdown("#### 📚 Sumber Utama")
            st.markdown(
                f'<div class="source-box">📄 <strong>{nama_materi(item["sumber"])}</strong>'
                f'<br><span class="small-muted">Materi dengan tingkat relevansi tertinggi.</span></div>',
                unsafe_allow_html=True,
            )

            if item["terkait"]:
                st.write("")
                with st.expander("📑 Lihat materi terkait"):
                    for terkait in item["terkait"]:
                        st.markdown(f"**📄 {nama_materi(terkait['nama_file'])}**")
                        potongan = ambil_potongan_relevan(
                            item["pertanyaan"],
                            terkait["isi"],
                            900,
                        )
                        st.write(potongan)
                        st.divider()
        else:
            st.warning(
                "Materi yang sesuai belum ditemukan dalam database. "
                "Coba gunakan kata kunci yang lebih spesifik."
            )

        if index < len(st.session_state.riwayat) - 1:
            st.divider()

# =========================================================
# TENTANG
# =========================================================
st.divider()

with st.expander("ℹ️ Tentang AI Tutor Bahasa Indonesia"):
    st.write(
        "AI Tutor Bahasa Indonesia adalah aplikasi pembelajaran yang "
        "mencari materi paling relevan dari Knowledge Base TXT yang tersedia. "
        "Jawaban ditampilkan berdasarkan isi materi yang ditemukan."
    )
    st.caption(
        f"Knowledge Base aktif: {len(database)} file TXT"
    )

st.caption(
    "AI Tutor Bahasa Indonesia • Python + Streamlit + TXT Knowledge Base"
)
