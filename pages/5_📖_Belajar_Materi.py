import streamlit as st
import os
from quiz_data import QUIZ_DATA


st.set_page_config(
    page_title="Belajar Materi - AI Tutor",
    page_icon="📖",
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
# LOAD DATABASE
# =========================================================

database = baca_database()


# =========================================================
# HEADER
# =========================================================

st.title("📖 Belajar Materi")

st.write(
    "Pilih materi Bahasa Indonesia yang ingin kamu pelajari "
    "dan pahami isi materinya secara lebih mendalam."
)

st.divider()


# =========================================================
# PILIH MATERI
# =========================================================

if not database:

    st.warning(
        "⚠️ Database materi belum ditemukan."
    )

else:

    daftar_materi = []

    for data in database:

        nama = data["nama_file"]

        judul = nama.replace(".txt", "")
        judul = judul.replace("_", " ")
        judul = judul.title()

        daftar_materi.append(judul)


    pilihan = st.selectbox(
        "📚 Pilih materi yang ingin dipelajari:",
        daftar_materi
    )


    # =====================================================
    # CARI MATERI YANG DIPILIH
    # =====================================================

    data_terpilih = None

    for data in database:

        nama = data["nama_file"]

        judul = nama.replace(".txt", "")
        judul = judul.replace("_", " ")
        judul = judul.title()

        if judul == pilihan:

            data_terpilih = data
            break


    # =====================================================
    # TAMPILKAN MATERI
    # =====================================================

    if data_terpilih:

        st.subheader(
            f"📖 {pilihan}"
        )

        isi = data_terpilih["isi"].strip()


        # -------------------------------------------------
        # RINGKASAN
        # -------------------------------------------------

        st.markdown("### 📝 Ringkasan Materi")

        if len(isi) > 500:

            ringkasan = isi[:500] + "..."

        else:

            ringkasan = isi

        st.info(ringkasan)


        # -------------------------------------------------
        # MATERI LENGKAP
        # -------------------------------------------------

        st.markdown("### 📚 Materi Lengkap")

        with st.expander(
            "Buka materi lengkap",
            expanded=True
        ):

            st.write(isi)


        # -------------------------------------------------
        # LATIHAN
        # -------------------------------------------------

        st.divider()

        st.subheader("🧠 Latihan Pemahaman")

        st.write(
            "Setelah membaca materi, coba jawab pertanyaan berikut."
        )

        pertanyaan_latihan = (
            f"Apa yang kamu pahami tentang materi "
            f"**{pilihan}**?"
        )

        st.markdown(
            f"**💬 {pertanyaan_latihan}**"
        )

        jawaban = st.text_area(
            "✍️ Tulis jawabanmu di sini:",
            placeholder="Tuliskan pemahamanmu tentang materi..."
        )

        if st.button(
            "✅ Periksa Jawaban"
        ):

            if jawaban.strip():

                jumlah_kata = len(
                    jawaban.strip().split()
                )

                if jumlah_kata >= 10:

                    st.success(
                        "🎉 Jawabanmu sudah cukup lengkap. "
                        "Bagus! Coba bandingkan kembali dengan materi "
                        "yang telah kamu baca."
                    )

                else:

                    st.warning(
                        "💡 Jawabanmu masih cukup singkat. "
                        "Coba jelaskan dengan lebih lengkap "
                        "menggunakan konsep dari materi."
                    )

            else:

                st.warning(
                    "⚠️ Silakan tuliskan jawaban terlebih dahulu."
                )
        # -------------------------------------------------
        # KUIS MATERI
        # -------------------------------------------------

        st.divider()

        st.subheader("🧠 Kuis Materi")

        st.write(
            "Uji pemahamanmu dengan menjawab 5 soal pilihan ganda "
            "berdasarkan materi yang sedang dipelajari."
        )

        # Membuat pencocokan nama materi yang aman
        kunci_kuis = None

        for nama_materi in QUIZ_DATA.keys():

            if (
                nama_materi.lower().replace("-", "").replace(" ", "")
                ==
                pilihan.lower().replace("-", "").replace(" ", "")
            ):
                kunci_kuis = nama_materi
                break

        soal_kuis = QUIZ_DATA.get(kunci_kuis, [])

        if soal_kuis:

            jawaban_kuis = []

            with st.form(
                f"form_kuis_{pilihan}"
            ):

                for nomor, soal in enumerate(
                    soal_kuis,
                    start=1
                ):

                    st.markdown(
                        f"**{nomor}. {soal['question']}**"
                    )

                    jawaban = st.radio(
                        "Pilih jawaban:",
                        soal["options"],
                        key=f"{pilihan}_{nomor}"
                    )

                    jawaban_kuis.append(jawaban)

                    st.write("")

                tombol_nilai = st.form_submit_button(
                    "✅ Periksa Nilai"
                )

            if tombol_nilai:

                jumlah_benar = 0

                for index, soal in enumerate(
                    soal_kuis
                ):

                    jawaban_benar = soal["options"][
                        soal["answer"]
                    ]

                    if jawaban_kuis[index] == jawaban_benar:

                        jumlah_benar += 1

                nilai = round(
                    (
                        jumlah_benar
                        / len(soal_kuis)
                    ) * 100
                )

                st.divider()

                st.subheader("📊 Hasil Kuis")

                st.success(
                    f"🎉 Nilai kamu: **{nilai}/100**"
                )

                st.write(
                    f"Jawaban benar: **{jumlah_benar} "
                    f"dari {len(soal_kuis)} soal**."
                )

                if nilai >= 80:

                    st.balloons()

                    st.success(
                        "🏆 Sangat baik! "
                        "Pemahamanmu terhadap materi sudah bagus."
                    )

                elif nilai >= 60:

                    st.info(
                        "👍 Cukup baik! "
                        "Coba pelajari kembali bagian yang belum dikuasai."
                    )

                else:

                    st.warning(
                        "📖 Sebaiknya baca kembali materi "
                        "dan coba kerjakan kuis lagi."
                    )
                # -------------------------------------------------
                # PEMBAHASAN JAWABAN
                # -------------------------------------------------

                st.divider()

                st.subheader("📖 Pembahasan Jawaban")

                for index, soal in enumerate(soal_kuis):

                    jawaban_benar = soal["options"][
                        soal["answer"]
                    ]

                    jawaban_pengguna = jawaban_kuis[index]

                    st.markdown(
                        f"**Soal {index + 1}**"
                    )

                    if jawaban_pengguna == jawaban_benar:

                        st.success(
                            f"✅ Benar! Jawabanmu: **{jawaban_pengguna}**"
                        )

                    else:

                        st.error(
                            f"❌ Jawabanmu: **{jawaban_pengguna}**"
                        )

                        st.info(
                            f"✔️ Jawaban yang benar: **{jawaban_benar}**"
                        )

                    st.write("")
        else:

            st.warning(
                "⚠️ Kuis untuk materi ini belum tersedia."
            )

# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "AI Tutor Bahasa Indonesia | Belajar Materi"
)