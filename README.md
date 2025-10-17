# 🔍 Flask Linear Regression Web App

Sebuah web aplikasi interaktif berbasis **Flask** untuk melakukan analisis **regresi linear** terhadap dataset CSV secara visual, cepat, dan fleksibel.  
Aplikasi ini mendukung **upload dataset**, **pemilihan variabel X & Y**, **visualisasi hasil regresi**, serta **penyimpanan data pengguna & hasil analisis ke MongoDB**.

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

## 🧱 Contoh Output

📊 **Visualisasi Regresi Linear**
![Arsitektur Sistem](https://raw.githubusercontent.com/intananggreini99/Flask_Pemrog3/main/static/plots/result_jumuah.png)

## 📜 Lisensi

License © 2025 — **Intan Dwi Anggreini & Christine Aulia**
