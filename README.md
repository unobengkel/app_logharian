# LogHarian - Sistem Catatan Harian Kerja

LogHarian adalah aplikasi web berbasis Python (Flask) yang dirancang untuk mengelola data kegiatan kerja harian, perencanaan, dan dokumentasi hasil kerja secara terstruktur. Proyek ini dibangun dengan menerapkan prinsip **Clean Architecture** untuk memastikan kode yang rapi, modular, dan mudah dipelihara.

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)
![TailwindCSS](https://img.shields.io/badge/tailwindcss-%2338B2AC.svg?style=for-the-badge&logo=tailwind-css&logoColor=white)

## ✨ Fitur Utama

- **Dashboard Modern**: Ringkasan aktivitas harian dan statistik cepat.
- **Master Data Kegiatan**: Kelola kategori kegiatan kerja dengan status aktif/nonaktif.
- **Perencanaan Kerja**: Susun jadwal rencana kerja mendatang dengan spesifikasi waktu.
- **Catatan Harian**: Dokumentasikan progres dan hasil pekerjaan secara detail.
- **Filter & Pencarian**: Pencarian tingkat lanjut berdasarkan rentang tanggal, jenis kegiatan, dan status.
- **Desain Responsif**: Antarmuka yang dioptimalkan untuk HP, Tablet, dan Desktop.

## 🏗️ Arsitektur Proyek (Clean Architecture)

Aplikasi ini dibagi menjadi 4 lapisan utama:

1.  **Domain Layer**: Berisi entitas bisnis inti (`Entities`) dan antarmuka repositori (`Repository Interfaces`).
2.  **Application Layer**: Berisi logika aplikasi atau Use Cases yang mengoordinasikan alur data.
3.  **Infrastructure Layer**: Implementasi teknis seperti akses database SQLite.
4.  **Interface Layer**: Pengendali (Controllers) dan tampilan (Jinja2 Templates) berbasis Tailwind CSS.

## 📁 Struktur Direktori

```text
src/
├── domain/            # Inti bisnis (Entities & Interfaces)
├── application/       # Logika aplikasi (Use Cases & DTOs)
├── infrastructure/    # Implementasi teknis (DB & Repositories)
└── interface/         # Presentasi (Controllers & Templates)
app.py                 # Entry point aplikasi
requirements.txt       # Daftar dependensi
catatan_harian.db      # Database SQLite (Generated otomatis)
```

## 🚀 Cara Instalasi

### Prasyarat
- Python 3.8 atau lebih tinggi.

### Langkah-langkah
1. **Clone Repositori**:
   ```bash
   git clone https://github.com/username/log-harian.git
   cd log-harian
   ```

2. **Install Dependensi**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Jalankan Aplikasi**:
   ```bash
   python app.py
   ```

4. **Akses di Browser**:
   Buka [http://127.0.0.1:5000](http://127.0.0.1:5000)

## 🛠️ Pengembangan
Untuk mengaktifkan mode pengembangan dengan auto-reload:
```bash
set FLASK_ENV=development
flask run
```

## 📄 Lisensi
Proyek ini dilisensikan di bawah MIT License - lihat berkas [LICENSE](LICENSE) untuk detailnya.

---
*Dibuat dengan ❤️ menggunakan Antigravity AI*
