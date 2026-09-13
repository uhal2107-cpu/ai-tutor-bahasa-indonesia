import streamlit as st

st.set_page_config(
    page_title="Tentang - AI Tutor Bahasa Indonesia",
    page_icon="📖",
    layout="wide"
)

st.title("📖 Tentang AI Tutor Bahasa Indonesia")

st.write(
    "AI Tutor Bahasa Indonesia merupakan aplikasi pembelajaran "
    "berbasis Python dan Streamlit yang membantu pengguna "
    "menemukan materi yang relevan berdasarkan pertanyaan."
)

st.divider()

st.header("🎯 Tujuan Aplikasi")

st.write(
    "Aplikasi ini dirancang untuk membantu proses pembelajaran "
    "dengan memanfaatkan kumpulan materi dalam bentuk file TXT "
    "sebagai knowledge base."
)

st.header("⚙️ Cara Kerja")

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("1️⃣ Pertanyaan")
    st.write(
        "Pengguna memasukkan pertanyaan "
        "atau topik yang ingin dipelajari."
    )

with col2:
    st.subheader("2️⃣ Pencarian")
    st.write(
        "Sistem menganalisis kata kunci "
        "dan mencocokkannya dengan materi."
    )

with col3:
    st.subheader("3️⃣ Jawaban")
    st.write(
        "Materi yang paling relevan ditampilkan "
        "sebagai jawaban."
    )

st.divider()

st.header("🛠️ Teknologi")

teknologi = [
    "Python",
    "Streamlit",
    "Knowledge Base TXT",
    "Sistem pencarian berbasis relevansi"
]

for item in teknologi:
    st.write(f"• {item}")

st.divider()

st.header("📚 Knowledge Base")

st.write(
    "Materi pembelajaran disimpan dalam folder "
    "`database/` dan dibaca secara otomatis oleh aplikasi."
)

st.info(
    "AI Tutor Bahasa Indonesia membantu pengguna "
    "menemukan informasi pembelajaran secara lebih cepat "
    "berdasarkan materi yang tersedia."
)

st.divider()

st.caption(
    "AI Tutor Bahasa Indonesia | "
    "Python + Streamlit + TXT Knowledge Base"
)