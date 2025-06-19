""""
Aplikasi Streamlit untuk memprediksi mahasiswa dropout berdasarkan data
hasil belajar serta kondisi keuangan selama dua semester


Model menggunakan Random Forest
Berikut Fitur yang digunakan
- Age_at_enrollment: Usia pada saat mendaftar
- Curricular_units_1st_sem_approved: SKS semester 1 yang disetujui
- Curricular_units_2nd_sem_approved: SKS semester 2 yang disetujui
- IPK_sem1: Nilai IPK semester 1
- IPK_sem2: Nilai IPK semester 2
- Selisih_IPK: Nilai selisih IPK semester 1 dan 2
- Tuition_fees_up_to_date: Pembayaran kuliah lunas (1: Ya, 0: Tidak)
- Debtor: Termasuk memiliki pinjaman (1: Ya, 0:Tidak)
- Scholarship_holder: Termasuk penerima beasiswa (1: Ya, 0:Tidak)
- Status_pembayaran: Gabungan dari status pelunasan dan penunggakan

"""

import numpy as np
import joblib
import streamlit as st

# Load model
model = joblib.load('model.pkl')

# Judul aplikasi
st.title("🎓 Prediksi Dropout Mahasiswa Jaya Jaya Institut")
st.write(
        "Aplikasi ini memprediksi status mahasiswa dropout berdasarkan data akademis serta status pembayaran"
        )

# Keterangan untuk input data pengguna
st.markdown("Masukkan informasi mahasiswa:")

# Input data
Age_at_enrollment = st.number_input(
        "Usia pada saat mendaftar", min_value=16, max_value=60, value=19)
Curricular_units_1st_sem_approved = st.number_input(
        "SKS Semester 1 yang disetujui", min_value=0, max_value=25, value=20)
Curricular_units_2nd_sem_approved = st.number_input(
        "SKS Semester 2 yang disetujui", min_value=0, max_value=25, value=20)
IPK_sem1 = st.slider("IPK Semester 1", min_value=0.0,
                      max_value=4.0, value=3.0)
IPK_sem2 = st.slider("IPK Semester 2", min_value=0.0,
                      max_value=4.0, value=3.0)
Biaya_lunas = st.selectbox(
        "Apakah pembayaran kuliah lunas?", ["Ya", "Tidak"])
Penunggak = st.selectbox(
    "Apakah menunggak biaya kuliah?", ["Ya", "Tidak"])
Peminjam = st.selectbox(
        "Apakah memiliki pinjaman?", ["Ya", "Tidak"])
Beasiswa = st.selectbox(
    "Apakah penerima beasiswa?", ["Ya", "Tidak"])

# Prediksi saat tombol diklik
if st.button("Prediksi mahasiswa sekarang"):
    # Hitung fitur turunan
    Selisih_IPK = IPK_sem1 - IPK_sem2
    Tuition_fees_up_to_date = 1 if Biaya_lunas == "Ya" else 0
    Status_pembayaran = 1 if (
        Biaya_lunas == "Ya" and Penunggak == "Tidak") else 0
    Debtor = 0 if Peminjam == "Tidak" else 1
    Scholarship_holder = 0 if Beasiswa =='Tidak' else 1

    # Susun input sesuai features
    input_data = np.array([[
        Age_at_enrollment,
        Curricular_units_1st_sem_approved,
        Curricular_units_2nd_sem_approved,
        IPK_sem1,
        IPK_sem2,
        Selisih_IPK,
        Tuition_fees_up_to_date,
        Debtor,
        Scholarship_holder,
        Status_pembayaran
    ]])

    # Prediksi
    pred = model.predict(input_data)[0]
    proba = model.predict_proba(input_data)[0]

    # Tampilkan hasil
    status = "🔴 Mahasiswa akan Dropout" if pred == 1 else "🟢 Mahasiswa tidak Dropout"
    st.subheader(f"Hasil Prediksi: {status}")
    st.caption(
        f"Probabilitas Dropout: {proba[1]:.2f} | Tidak Dropout: {proba[0]:.2f}")