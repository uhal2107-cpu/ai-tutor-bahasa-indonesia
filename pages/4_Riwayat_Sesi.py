import streamlit as st
import os
import json


st.set_page_config(
    page_title="Riwayat Sesi",
    page_icon="🕘",
    layout="wide"
)


# =========================================================
# KONFIGURASI
# =========================================================

FILE_RIWAYAT = "riwayat.json"


# =========================================================
# MEMBACA RIWAYAT
# =========================================================

def baca_riwayat():

    if not os.path.exists(FILE_RIWAYAT):
        return []

    try:
        with open(
            FILE_RIWAYAT,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    except Exception:
        return []


# =========================================================
# HEADER
# =========================================================

st.title("🕘 Riwayat Sesi")

st.write(
    "Lihat kembali riwayat pencarian materi yang telah dilakukan."
)

st.divider()


# =========================================================
# LOAD RIWAYAT
# =========================================================

riwayat = baca_riwayat()


# =========================================================
# TAMPILKAN RIWAYAT
# =========================================================

if len(riwayat) == 0:

    st.info(
        "📝 Belum ada riwayat pencarian. "
        "Silakan lakukan pencarian terlebih dahulu."
    )

else:

    st.subheader("📚 Pencarian Sebelumnya")

    st.write(
        f"Total pencarian: **{len(riwayat)}**"
    )

    st.divider()

    for index, item in enumerate(
        reversed(riwayat),
        start=1
    ):

        st.markdown(
            f"""
            ### {index}. 🔎 {item["pertanyaan"]}

            Ditemukan **{item["jumlah_hasil"]} materi**
            yang relevan.
            """
        )

        st.divider()


# =========================================================
# FOOTER
# =========================================================

st.caption(
    "AI Tutor Bahasa Indonesia | Riwayat Sesi"
)