# 🔍 Flask Linear Regression Web App

Sebuah web aplikasi interaktif berbasis **Flask** untuk melakukan analisis **regresi linear** terhadap dataset CSV secara visual, cepat, dan fleksibel.  
Aplikasi ini mendukung **upload dataset**, **pemilihan variabel X & Y**, **visualisasi hasil regresi**, serta **penyimpanan data pengguna & hasil analisis ke MongoDB**.

---

## 🚀 Fitur Utama

✅ **Upload Dataset**
- Upload file CSV untuk data *training* dan *testing*.
- Data disimpan otomatis ke MongoDB serta direktori `uploads/`.

✅ **Pilih Variabel**
- Pilih variabel bebas (X) dan variabel target (Y) secara dinamis.
- Mendukung lebih dari satu variabel X.

✅ **Regresi Linear Custom**
- Menggunakan model buatan sendiri dari direktori `matriks/operations/linear_regression.py`.
- Tidak menggunakan scikit-learn — sepenuhnya implementasi internal.

✅ **Visualisasi Hasil**
- Menampilkan hasil regresi berupa grafik dan evaluasi model.
- Grafik disimpan ke folder `static/plots/`.

✅ **Database MongoDB**
- Menggunakan MongoDB (via Docker) untuk menyimpan data user, file path, hasil evaluasi, dan visualisasi.

✅ **Docker Compose Support**
- Semua service (Flask + MongoDB) terbungkus dalam satu stack Docker Compose.

---

## 🏗️ Arsitektur Sistem

![Arsitektur Sistem](https://raw.githubusercontent.com/intananggreini99/Flask_Pemrog3/main/static/images/architecture.png)
---

## ⚙️ Instalasi & Menjalankan (via Docker Compose)

### 1️⃣ Clone repositori
```bash
git clone https://github.com/intananggreini99/Flask_Pemrog3.git
cd Flask_Pemrog3
````

### 2️⃣ Pastikan file `.env` sudah berisi:

```env
MONGO_URI=mongodb://intanchris:sdt25@mongo:27017/appdb?authSource=appdb
MONGO_DB=appdb
FLASK_ENV=production
SECRET_KEY=change-me
PORT=5000
```

### 3️⃣ Jalankan Docker Compose

```bash
docker compose up -d --build
```

### 4️⃣ Akses aplikasi

* Buka: **[http://localhost:5000/](http://localhost:5000/)**
* Cek health: **[http://localhost:5000/healthz](http://localhost:5000/healthz)**

---

## 🧠 Teknologi yang Digunakan

| Komponen           | Fungsi                                              |
| ------------------ | --------------------------------------------------- |
| **Flask**          | Web framework utama                                 |
| **MongoDB**        | Database penyimpanan hasil analisis                 |
| **Docker Compose** | Mengatur container Flask & MongoDB                  |
| **Matplotlib**     | Visualisasi hasil regresi                           |
| **Pandas**         | Membaca & manipulasi dataset CSV                    |
| **Gunicorn**       | Production WSGI server untuk Flask                  |
| **Python-dotenv**  | Membaca konfigurasi dari `.env`                     |
| **Certifi**        | Sertifikat SSL untuk koneksi Mongo Atlas (opsional) |

---

## 🧩 Cara Menggunakan Aplikasi

1️⃣ **Upload Dataset**

* Masuk ke halaman utama
* Masukkan nama user
* Upload `training.csv` dan `testing.csv`
* Klik **Next**

2️⃣ **Pilih Variabel**

* Pilih variabel bebas (X) dan target (Y)
* Klik **Regression Analysis**

3️⃣ **Lihat Hasil**

* Aplikasi akan menampilkan hasil regresi, evaluasi model, dan grafik hubungan X–Y.

---

## 🧰 Pengembangan Lokal (tanpa Docker)

Jika ingin menjalankan langsung di lokal:

```bash
pip install -r requirements.txt
python app.py
```

Akses di:

```
http://127.0.0.1:5000
```

---

## 🧱 Contoh Output

📊 **Visualisasi Regresi Linear**
![](static/images/example_plot.png)

📋 **Tabel Evaluasi Model**

| Metric | Value |
| ------ | ----- |
| MAE    | 2.14  |
| MSE    | 6.31  |
| R²     | 0.87  |

---

## 🔒 Struktur Data MongoDB

Koleksi: `submissions`

```json
{
  "_id": "ObjectId",
  "nama_user": "Intan Dwi",
  "file_train": "uploads/training/data_train.csv",
  "file_test": "uploads/testing/data_test.csv",
  "x_columns": ["Feature1", "Feature2"],
  "y_column": "Target",
  "evaluasi": {
    "MAE": 1.24,
    "MSE": 4.62,
    "R2": 0.89
  },
  "visualisasi_path": "result_Intan_Dwi.png",
  "created_at": "2025-10-17T14:00:00"
}
```

---

## 💾 Backup & Akses Database

Akses MongoDB melalui **MongoDB Compass**:

```
mongodb://intanchris:sdt25@localhost:27017/appdb?authSource=appdb
```

---

## 📜 Lisensi

MIT License © 2025 — **Intan Dwi Anggreini**

---

> 💡 *“Data tells a story — this app helps you visualize it.”*

```

---

Apakah kamu mau saya bantu buatkan versi **README bilingual (Indonesia + English)** atau versi **README dengan badge GitHub & preview screenshot (Markdown style GitHub repo modern)**?  
Itu bisa bikin project kamu terlihat jauh lebih profesional di GitHub.
```
