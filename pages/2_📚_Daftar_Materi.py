import streamlit as st
import os


st.set_page_config(
    page_title="Daftar Materi - AI Tutor",
    page_icon="📚",
    layout="wide"
)


# =========================================================
# KONFIGURASI
# =========================================================

FOLDER_DATABASE = "database"


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
# LOAD DATA
# =========================================================

database = baca_database()


# =========================================================
# HEADER
# =========================================================

st.title("📚 Daftar Materi")

st.write(
    "Jelajahi seluruh materi yang tersedia "
    "di dalam Knowledge Base AI Tutor Bahasa Indonesia."
)

st.divider()


# =========================================================
# STATISTIK
# =========================================================

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "📚 Total Materi",
        len(database)
    )

with col2:
    st.metric(
        "📁 Format",
        "TXT"
    )

with col3:
    st.metric(
        "🔎 Status",
        "Aktif"
    )


st.divider()


# =========================================================
# DAFTAR MATERI
# =========================================================

if len(database) == 0:

    st.warning(
        "Belum ada materi yang tersedia "
        "di dalam folder database."
    )

else:

    st.subheader("📖 Materi Tersedia")

    # Membuat 3 kolom
    kolom = st.columns(3)

    for index, data in enumerate(database):

        nama = data["nama_file"]

        # Mengubah nama file menjadi judul
        judul = nama.replace(".txt", "")
        judul = judul.replace("_", " ")
        judul = judul.title()

        # Mengambil sedikit isi materi
        isi = data["isi"].strip()

        if len(isi) > 120:
            ringkasan = isi[:120] + "..."
        else:
            ringkasan = isi

        with kolom[index % 3]:

            st.markdown(
                f"""<div style="padding:22px; margin-bottom:20px; border-radius:18px; background-color:#f8f5f0; border:1px solid #e5ded5; min-height:190px;">
                <div style="font-size:32px; margin-bottom:10px;">📖</div>
                <h3 style="margin-bottom:10px;">{judul}</h3>
                <p style="color:#666; font-size:14px; line-height:1.6;">{ringkasan}</p>
                </div>""",
                unsafe_allow_html=True
            )

            with st.expander("Lihat materi"):
                st.write(data["isi"])
# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "AI Tutor Bahasa Indonesia | "
    "Knowledge Base"
)