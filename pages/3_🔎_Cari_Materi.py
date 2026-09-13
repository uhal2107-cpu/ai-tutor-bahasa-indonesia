import streamlit as st
import os
import json


st.set_page_config(
    page_title="Cari Materi - AI Tutor",
    page_icon="🔎",
    layout="wide"
)


# =========================================================
# KONFIGURASI
# =========================================================

FOLDER_DATABASE = "database"
FILE_RIWAYAT = "riwayat.json"


def simpan_riwayat(pertanyaan, jumlah_hasil):
    riwayat = []

    if os.path.exists(FILE_RIWAYAT):
        try:
            with open(FILE_RIWAYAT, "r", encoding="utf-8") as file:
                riwayat = json.load(file)
        except Exception:
            riwayat = []

    riwayat.append({
        "pertanyaan": pertanyaan,
        "jumlah_hasil": jumlah_hasil
    })

    with open(FILE_RIWAYAT, "w", encoding="utf-8") as file:
        json.dump(
            riwayat,
            file,
            ensure_ascii=False,
            indent=4
        )

# =========================================================
# MEMBACA DATABASE
# =========================================================

def baca_database():

    data = []

    if not os.path.exists(FOLDER_DATABASE):
        return data

    for nama_file in os.listdir(FOLDER_DATABASE):

        if nama_file.lower().endswith(".txt"):

            lokasi_file = os.path.join(
                FOLDER_DATABASE,
                nama_file
            )

            try:
                with open(
                    lokasi_file,
                    "r",
                    encoding="utf-8"
                ) as file:

                    isi = file.read()

                data.append({
                    "nama_file": nama_file,
                    "isi": isi
                })

            except Exception:
                pass

    return data


# =========================================================
# PENCARIAN
# =========================================================

def cari_materi(pertanyaan, database):

    hasil = []

    kata_kunci = pertanyaan.lower().split()

    for data in database:

        teks = (
            data["nama_file"] + " " +
            data["isi"]
        ).lower()

        skor = 0

        for kata in kata_kunci:

            if kata in teks:
                skor += 1

        if skor > 0:

            hasil.append({
                "nama_file": data["nama_file"],
                "isi": data["isi"],
                "skor": skor
            })

    hasil.sort(
        key=lambda x: x["skor"],
        reverse=True
    )

    return hasil


# =========================================================
# LOAD DATABASE
# =========================================================

database = baca_database()


# =========================================================
# HEADER
# =========================================================

st.title("🔎 Cari Materi")

st.write(
    "Cari materi Bahasa Indonesia berdasarkan "
    "kata kunci atau topik yang ingin kamu pelajari."
)

st.divider()


# =========================================================
# SEARCH BOX
# =========================================================

with st.form("form_pencarian"):

    pertanyaan = st.text_input(
        "💬 Apa yang ingin kamu pelajari?",
        placeholder="Contoh: fonologi, kalimat efektif, paragraf..."
    )

    tombol_cari = st.form_submit_button(
        "🔎 Cari Materi"
    )


# =========================================================
# RIWAYAT PENCARIAN
# =========================================================




# =========================================================
# HASIL PENCARIAN
# =========================================================

st.subheader("📚 Hasil Pencarian")

if tombol_cari:

    if pertanyaan.strip():

        hasil = cari_materi(
            pertanyaan,
            database
        )

        # Simpan ke riwayat
        simpan_riwayat(
            pertanyaan.strip(),
            len(hasil)
        )

        # ---------------------------------------------
        # JIKA MATERI DITEMUKAN
        # ---------------------------------------------

        if hasil:

            st.success(
                f"✅ Ditemukan {len(hasil)} materi yang relevan."
            )

            for nomor, data in enumerate(hasil, start=1):

                nama = data["nama_file"]

                judul = nama.replace(".txt", "")
                judul = judul.replace("_", " ")
                judul = judul.title()

                st.markdown(
                    f"### {nomor}. 📖 {judul}"
                )

                st.caption(
                    f"Relevansi: {data['skor']} kata kunci cocok"
                )

                isi = data["isi"].strip()

                # Ringkasan
                if len(isi) > 300:
                    ringkasan = isi[:300] + "..."
                else:
                    ringkasan = isi

                st.write(ringkasan)

                # Materi lengkap
                with st.expander("📖 Lihat materi lengkap"):
                    st.write(data["isi"])

                st.divider()

        # ---------------------------------------------
        # JIKA TIDAK DITEMUKAN
        # ---------------------------------------------

        else:

            st.warning(
                "⚠️ Materi yang sesuai belum ditemukan. "
                "Coba gunakan kata kunci yang lebih umum."
            )

    else:

        st.warning(
            "⚠️ Silakan masukkan kata kunci terlebih dahulu."
        )

else:

    st.info(
        "💡 Masukkan kata kunci, lalu klik "
        "**🔎 Cari Materi** untuk mulai mencari."
    )


# =========================================================
# INFORMASI
# =========================================================

st.markdown(
    """
    **Contoh pencarian:**

    - `fonologi`
    - `kalimat`
    - `paragraf`
    - `klausa`
    - `wacana`
    - `bahasa Indonesia`
    """
)


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "AI Tutor Bahasa Indonesia | Pencarian Knowledge Base"
)
