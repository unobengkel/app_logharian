# 📋 Analisa Sistem Pencatatan Kegiatan Kerja (Catatan Harian)

> **Dokumen Analisa & Desain Sistem**
> Dibuat oleh: Sistem Analis
> Tanggal: 9 Mei 2026

---

## Daftar Isi
1. [Task 1: Struktur Direktori & File Markdown](#task-1-struktur-direktori--file-markdown)
2. [Task 2: Desain Arsitektur Sistem (Clean Architecture)](#task-2-desain-arsitektur-sistem-clean-architecture)
3. [Task 3: Desain ERD Database](#task-3-desain-erd-database)
4. [Task 4: Desain Use Case Diagram](#task-4-desain-use-case-diagram)
5. [Task 5: Desain DFD Level 0 (Context Diagram)](#task-5-desain-dfd-level-0-context-diagram)
6. [Task 6: Desain DFD Level 1](#task-6-desain-dfd-level-1)
7. [Task 7: Desain Struktur Database (SQLite DDL)](#task-7-desain-struktur-database-sqlite-ddl)
8. [Task 8: Desain Form-Form UI](#task-8-desain-form-form-ui)
9. [Task 9: Desain REST API Endpoint](#task-9-desain-rest-api-endpoint)
10. [Task 10: Desain Struktur Direktori Proyek Python](#task-10-desain-struktur-direktori-proyek-python)
11. [Task 11: Desain Routing URL](#task-11-desain-routing-url)
12. [Task 12: Desain Template HTML](#task-12-desain-template-html)
13. [Task 13: Desain Alur Navigasi Aplikasi](#task-13-desain-alur-navigasi-aplikasi)
14. [Task 14: Desain Validasi & Error Handling](#task-14-desain-validasi--error-handling)
15. [Task 15: Desain Responsive Breakpoints](#task-15-desain-responsive-breakpoints)
16. [Task 16: Desain Filter & Pencarian](#task-16-desain-filter--pencarian)
17. [Task 17: Ringkasan & Finalisasi Dokumen Analisa](#task-17-ringkasan--finalisasi-dokumen-analisa)

---

## Task 1: Struktur Direktori & File Markdown

### Struktur Direktori

```
widget_gauge_v2/
├── document/
│   └── analisa_sistem/
│       └── analisa_sistem.md          ← FILE INI
├── src/                                (akan dibuat)
│   ├── application/                    [Use Cases]
│   ├── domain/                         [Entities]
│   ├── infrastructure/                 [Database, Repositories]
│   └── interface/                      [Controllers, Templates]
├── app.py                              (main entry)
└── requirements.txt
```

### Tujuan Dokumen
Dokumen ini berisi seluruh hasil analisa dan desain sistem **Pencatatan Kegiatan Kerja (Catatan Harian)** yang akan dibangun menggunakan:
- **Backend**: Python (Flask/FastAPI)
- **Database**: SQLite
- **Frontend**: HTML + Tailwind CSS (Server-side rendering)
- **Arsitektur**: Clean Architecture
- **Komunikasi**: REST API (HTTP GET/POST)

---

---

## Task 2: Desain Arsitektur Sistem (Clean Architecture)

### Konsep Clean Architecture

Arsitektur ini memisahkan kode ke dalam **4 lapisan (layers)** dengan aturan ketergantungan: **lapisan dalam tidak boleh tahu tentang lapisan luar**. Semua ketergantungan mengarah ke dalam (dari luar ke dalam).

```
┌─────────────────────────────────────────────────────────────┐
│                      INTERFACE LAYER                         │
│  ┌─────────────────────────────────────────────────────────┐│
│  │  Controllers (HTTP Handlers)                            ││
│  │  - menerima request dari browser                        ││
│  │  - memanggil Use Case                                   ││
│  │  - mengirim response ke template                        ││
│  │  Templates (HTML + Tailwind)                            ││
│  └─────────────────────────────────────────────────────────┘│
├─────────────────────────────────────────────────────────────┤
│                   APPLICATION LAYER                          │
│  ┌─────────────────────────────────────────────────────────┐│
│  │  Use Cases (Interactors)                                ││
│  │  - KelolaKegiatan (CRUD master kegiatan)                ││
│  │  - BuatRencanaHarian                                    ││
│  │  - CatatKegiatanHarian                                  ││
│  │  - LihatDaftar (dengan filter tanggal)                  ││
│  └─────────────────────────────────────────────────────────┘│
├─────────────────────────────────────────────────────────────┤
│                    DOMAIN LAYER                              │
│  ┌─────────────────────────────────────────────────────────┐│
│  │  Entities (Business Objects)                            ││
│  │  - Kegiatan (id, nama, deskripsi, status)               ││
│  │  - Perencanaan (id, tgl, kegiatan_id, catatan)          ││
│  │  - CatatanHarian (id, tgl, kegiatan_id, deskripsi, jam) ││
│  │  Repository Interfaces (protocol/ABC)                   ││
│  └─────────────────────────────────────────────────────────┘│
├─────────────────────────────────────────────────────────────┤
│                  INFRASTRUCTURE LAYER                        │
│  ┌─────────────────────────────────────────────────────────┐│
│  │  Database (SQLite)                                      ││
│  │  Repository Implementations                             ││
│  │  - KegiatanRepository                                   ││
│  │  - PerencanaanRepository                                ││
│  │  - CatatanHarianRepository                              ││
│  └─────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────┘
```

### Alur Request-Response

```
Browser (User)
    │
    ▼
┌────────────────┐
│  Controller    │  ← Interface Layer (menerima HTTP request)
│  (handler)     │
└───────┬────────┘
        │ call use case
        ▼
┌────────────────┐
│  Use Case      │  ← Application Layer (logika bisnis)
│  (interactor)  │
└───────┬────────┘
        │ call repository interface
        ▼
┌────────────────┐
│  Repository    │  ← Domain Layer (interface)
│  Interface     │
└───────┬────────┘
        │ implemented by
        ▼
┌────────────────┐
│  Repository    │  ← Infrastructure Layer (SQLite)
│  Impl          │
└───────┬────────┘
        │
        ▼
    SQLite DB
```

### Prinsip Clean Architecture yang Diterapkan

| Prinsip | Penerapan |
|---------|-----------|
| **Separation of Concerns** | Setiap layer punya tanggung jawab berbeda |
| **Dependency Inversion** | Layer dalam (domain) tidak import layer luar |
| **Repository Pattern** | Abstraksi database melalui interface |
| **Use Case Driven** | Setiap fitur adalah satu use case |
| **Testability** | Setiap layer bisa di-test secara independen |

---

---

## Task 3: Desain ERD Database

### Entity Relationship Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                     ERD - SISTEM CATATAN HARIAN                  │
└─────────────────────────────────────────────────────────────────┘

                            ┌───────────────┐
                            │   Kegiatan     │
                            │  (Master)      │
                            ├───────────────┤
                            │ PK id_kegiatan │◄───────────────────┐
                            │ nama_kegiatan  │                    │
                            │ deskripsi      │                    │
                            │ status         │                    │
                            │ created_at     │                    │
                            │ updated_at     │                    │
                            └───────┬───────┘                    │
                                    │                            │
                                    │ 1                           │ 1
                                    │                            │
                                    │ N                           │ N
                           ┌────────┴────────┐         ┌────────┴────────┐
                           │  Perencanaan     │         │  CatatanHarian  │
                           │  (Rencana Kerja) │         │  (Log Harian)   │
                           ├─────────────────┤         ├─────────────────┤
                           │ PK id_rencana   │         │ PK id_catatan   │
                           │ FK id_kegiatan  │────────►│ FK id_kegiatan  │
                           │ tanggal         │         │ tanggal         │
                           │ jam_mulai       │         │ jam_mulai       │
                           │ jam_selesai     │         │ jam_selesai     │
                           │ catatan         │         │ deskripsi       │
                           │ status          │         │ status          │
                           │ created_at      │         │ created_at      │
                           │ updated_at      │         │ updated_at      │
                           └─────────────────┘         └─────────────────┘
```

### Relasi Antar Tabel

| Tabel 1 | Relasi | Tabel 2 | Keterangan |
|---------|--------|---------|------------|
| Kegiatan | 1 → N | Perencanaan | Satu kegiatan bisa direncanakan berkali-kali |
| Kegiatan | 1 → N | CatatanHarian | Satu kegiatan bisa dicatat berkali-kali |

### Penjelasan Entitas

#### 1. **kegiatan** (Master Data Kegiatan)
Entitas utama yang berisi daftar kegiatan yang bisa dilakukan. Data ini adalah **master/referensi** yang akan dipilih saat membuat rencana atau mencatat kegiatan harian.

| Field | Tipe | Keterangan |
|-------|------|------------|
| id_kegiatan | INTEGER (PK) | Primary key auto-increment |
| nama_kegiatan | VARCHAR(200) | Nama kegiatan (wajib) |
| deskripsi | TEXT | Deskripsi kegiatan (opsional) |
| status | VARCHAR(20) | Status: 'aktif' / 'nonaktif' (default 'aktif') |
| created_at | DATETIME | Waktu buat (default: CURRENT_TIMESTAMP) |
| updated_at | DATETIME | Waktu update (default: CURRENT_TIMESTAMP) |

#### 2. **perencanaan** (Rencana Harian)
Berisi **rencana** kegiatan yang akan dilakukan pada suatu hari.

| Field | Tipe | Keterangan |
|-------|------|------------|
| id_rencana | INTEGER (PK) | Primary key auto-increment |
| id_kegiatan | INTEGER (FK) | Foreign key ke tabel kegiatan |
| tanggal | DATE | Tanggal rencana (wajib) |
| jam_mulai | TIME | Jam mulai rencana (opsional) |
| jam_selesai | TIME | Jam selesai rencana (opsional) |
| catatan | TEXT | Catatan tambahan (opsional) |
| status | VARCHAR(20) | Status: 'direncanakan' / 'selesai' / 'batal' (default 'direncanakan') |
| created_at | DATETIME | Waktu buat |
| updated_at | DATETIME | Waktu update |

#### 3. **catatan_harian** (Log Kegiatan Harian)
Berisi **catatan aktual** tentang apa yang sudah dilakukan pada hari ini.

| Field | Tipe | Keterangan |
|-------|------|------------|
| id_catatan | INTEGER (PK) | Primary key auto-increment |
| id_kegiatan | INTEGER (FK) | Foreign key ke tabel kegiatan |
| tanggal | DATE | Tanggal kegiatan (wajib) |
| jam_mulai | TIME | Jam mulai (opsional) |
| jam_selesai | TIME | Jam selesai (opsional) |
| deskripsi | TEXT | Deskripsi / hasil kegiatan (wajib) |
| status | VARCHAR(20) | Status: 'selesai' / 'proses' / 'tertunda' (default 'selesai') |
| created_at | DATETIME | Waktu buat |
| updated_at | DATETIME | Waktu update |

### Key Points Desain

1. **Pemisahan Rencana & Catatan**: Perencanaan dan Catatan Harian dipisah agar pengguna bisa:
   - Merencanakan kegiatan di masa depan
   - Mencatat kegiatan yang sudah dilakukan
   - Membandingkan rencana vs realisasi

2. **Foreign Key ke Kegiatan**: Kedua tabel (perencanaan & catatan_harian) merujuk ke master kegiatan, memastikan konsistensi data.

3. **Field Status**: Masing-masing entitas punya status untuk tracking progress.

---

---

## Task 4: Desain Use Case Diagram

### Diagram Use Case

```
┌─────────────────────────────────────────────────────────────────────┐
│                    SISTEM CATATAN HARIAN KERJA                       │
└─────────────────────────────────────────────────────────────────────┘

                           ┌───────────────────┐
                           │                   │
                           │    P E N G G U N A  │
                           │                   │
                           └─────────┬─────────┘
                                     │
                ┌────────────────────┼────────────────────┐
                │                    │                    │
                ▼                    ▼                    ▼
        ┌───────────────┐   ┌───────────────┐   ┌───────────────┐
        │  Kelola Master │   │  Buat Rencana │   │ Catat Kegiatan│
        │   Kegiatan     │   │   Harian      │   │   Harian      │
        └───────┬───────┘   └───────┬───────┘   └───────┬───────┘
                │                    │                    │
                ├── <<include>> ────┤                    │
                │                   │                    │
                ▼                   ▼                    ▼
        ┌───────────────┐   ┌───────────────┐   ┌───────────────┐
        │  Lihat Daftar  │   │  Lihat Daftar │   │  Lihat Daftar │
        │   Kegiatan     │   │   Rencana     │   │   Catatan     │
        └───────┬───────┘   └───────┬───────┘   └───────┬───────┘
                │                    │                    │
                └────────────────────┼────────────────────┘
                                     │
                                     ▼
                             ┌───────────────┐
                             │  Filter Data  │
                             │  by Tanggal   │
                             └───────────────┘
```

### Daftar Use Case

| Kode | Use Case | Aktor | Deskripsi |
|------|----------|-------|-----------|
| UC-01 | Kelola Master Kegiatan | Pengguna | CRUD data kegiatan (tambah, lihat, edit, hapus) |
| UC-02 | Buat Rencana Harian | Pengguna | Membuat rencana kegiatan untuk hari tertentu |
| UC-03 | Catat Kegiatan Harian | Pengguna | Mencatat kegiatan yang sudah dilakukan |
| UC-04 | Lihat Daftar Kegiatan | Pengguna | Melihat daftar master kegiatan |
| UC-05 | Lihat Daftar Rencana | Pengguna | Melihat daftar rencana harian |
| UC-06 | Lihat Daftar Catatan | Pengguna | Melihat daftar catatan harian |
| UC-07 | Filter Data by Tanggal | Pengguna | Memfilter daftar rencana/catatan berdasarkan tanggal |

### Skenario Use Case Detail

#### UC-01: Kelola Master Kegiatan
```
Aktor: Pengguna
Pre-condition: - 
Post-condition: Data kegiatan tersimpan di database

Alur Normal:
1. Pengguna memilih menu "Master Kegiatan"
2. Sistem menampilkan daftar kegiatan
3. Pengguna memilih aksi:
   a. Tambah: isi form nama & deskripsi → simpan
   b. Edit: klik edit pada kegiatan → ubah data → simpan
   c. Hapus: klik hapus → konfirmasi → hapus
   d. Nonaktifkan: ubah status menjadi nonaktif
4. Sistem menyimpan perubahan

Alur Alternatif:
- Nama kegiatan sudah ada → tampilkan error
- Data tidak lengkap → validasi gagal
```

#### UC-02: Buat Rencana Harian
```
Aktor: Pengguna
Pre-condition: Sudah ada data master kegiatan
Post-condition: Rencana tersimpan di database

Alur Normal:
1. Pengguna memilih menu "Buat Rencana"
2. Sistem menampilkan form rencana (tgl, kegiatan, jam, catatan)
3. Pengguna mengisi form dan submit
4. Sistem menyimpan rencana
5. Sistem menampilkan daftar rencana

Alur Alternatif:
- Tanggal tidak valid → error
- Kegiatan tidak dipilih → validasi gagal
```

#### UC-03: Catat Kegiatan Harian
```
Aktor: Pengguna
Pre-condition: Sudah ada data master kegiatan
Post-condition: Catatan tersimpan di database

Alur Normal:
1. Pengguna memilih menu "Catat Hari Ini"
2. Sistem menampilkan form catatan (tgl, kegiatan, jam, deskripsi)
3. Pengguna mengisi form dan submit
4. Sistem menyimpan catatan
5. Sistem menampilkan daftar catatan

Alur Alternatif:
- Tanggal tidak valid → error
- Deskripsi kosong → validasi gagal
```

#### UC-07: Filter Data by Tanggal
```
Aktor: Pengguna
Pre-condition: Ada data rencana/catatan
Post-condition: Data difilter sesuai tanggal

Alur Normal:
1. Pengguna berada di halaman daftar (rencana/catatan)
2. Pengguna memilih tanggal filter
3. Sistem menampilkan data sesuai tanggal yang dipilih
4. Jika tidak ada data → tampilkan pesan "Tidak ada data"

Alur Alternatif:
- Filter dikosongkan → tampilkan semua data
- Filter diubah → refresh data
```

---

---

## Task 5: Desain DFD Level 0 (Context Diagram)

### Context Diagram (DFD Level 0)

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                      │
│                S I S T E M   C A T A T A N   H A R I A N              │
│                         (Context Diagram)                             │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘

                               ┌─────────────────────┐
                               │                     │
                               │    P E N G G U N A    │
                               │   (External Entity)  │
                               │                     │
                               └──────────┬──────────┘
                                          │
                    ┌─────────────────────┼─────────────────────┐
                    │                     │                     │
                    │   Input Data Flow   │   Output Data Flow  │
                    ▼                     ▼                     ▼
          ┌─────────────────────────────────────────────────────────┐
          │                                                          │
          │              SISTEM CATATAN HARIAN KERJA                 │
          │                   (Boundary / System)                     │
          │                                                          │
          │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
          │  │ Master       │  │ Perencanaan  │  │ Catatan      │  │
          │  │ Kegiatan     │  │ Harian       │  │ Harian       │  │
          │  └──────────────┘  └──────────────┘  └──────────────┘  │
          │                                                          │
          │                  ┌──────────────┐                        │
          │                  │ Filter       │                        │
          │                  │ Tanggal      │                        │
          │                  └──────────────┘                        │
          │                                                          │
          │                     ┌──────────┐                         │
          │                     │ SQLite   │                         │
          │                     │ Database │                         │
          │                     └──────────┘                         │
          └─────────────────────────────────────────────────────────┘
```

### Data Flow Detail

| Kode | Alur Data | Arah | Keterangan |
|------|-----------|------|------------|
| D1 | Data Master Kegiatan | Input | Data kegiatan baru (nama, deskripsi) |
| D2 | Daftar Kegiatan | Output | Tampilan daftar master kegiatan |
| D3 | Data Rencana Harian | Input | Tanggal, kegiatan, jam, catatan |
| D4 | Daftar Rencana | Output | Tampilan daftar rencana harian |
| D5 | Data Catatan Harian | Input | Tanggal, kegiatan, jam, deskripsi |
| D6 | Daftar Catatan | Output | Tampilan daftar catatan harian |
| D7 | Parameter Filter | Input | Tanggal filter yang dipilih |
| D8 | Hasil Filter | Output | Data yang sudah difilter |

### External Entity

| Entity | Deskripsi |
|--------|-----------|
| **Pengguna** | User/client yang menggunakan aplikasi catatan harian. Satu-satunya aktor yang berinteraksi langsung dengan sistem. |

### Proses Tunggal (Sistem)

Sistem Catatan Harian Kerja adalah **satu kesatuan proses** yang menerima input dari pengguna dan menghasilkan output berupa tampilan daftar data. Semua logika ada di dalam sistem ini, termasuk:
- CRUD master kegiatan
- CRUD perencanaan harian
- CRUD catatan harian
- Filter tanggal
- Penyimpanan ke SQLite

### Data Store (Penyimpanan)

| Store | Deskripsi |
|-------|-----------|
| **SQLite Database** | Database lokal yang menyimpan semua data (kegiatan, perencanaan, catatan_harian) |

---

---

## Task 6: Desain DFD Level 1

### DFD Level 1 Diagram

```
┌────────────────────────────────────────────────────────────────────────────┐
│                         DFD LEVEL 1 - SISTEM CATATAN HARIAN                │
└────────────────────────────────────────────────────────────────────────────┘

                               ┌──────────────────┐
                               │                  │
                               │   P E N G G U N A │
                               │                  │
                               └────────┬─────────┘
                                        │
                        ┌───────────────┼───────────────┐
                        │               │               │
                        ▼               ▼               ▼
              ┌─────────────────┐ ┌─────────────┐ ┌─────────────────┐
              │ Proses 1.0      │ │ Proses 2.0  │ │ Proses 3.0      │
              │ Kelola Master   │ │ Kelola      │ │ Kelola Catatan  │
              │ Kegiatan        │ │ Perencanaan │ │ Harian          │
              └────────┬────────┘ └──────┬──────┘ └────────┬────────┘
                       │                 │                  │
                       │                 │                  │
                       ▼                 ▼                  ▼
              ┌──────────────────────────────────────────────────┐
              │               Proses 4.0                          │
              │               Laporan & Filter                    │
              │         (Filter by Tanggal, Tampilkan Data)       │
              └──────────────────────┬───────────────────────────┘
                                     │
                                     ▼
                            ┌──────────────────┐
                            │   Data Store      │
                            │   SQLite DB       │
                            │ ┌────────────────┐│
                            │ │ D1: kegiatan   ││
                            │ │ D2: perencanaan││
                            │ │ D3: catatan_   ││
                            │ │     harian     ││
                            │ └────────────────┘│
                            └──────────────────┘
```

### Detail Proses

| Proses | Nama | Input | Output | Deskripsi |
|--------|------|-------|--------|-----------|
| 1.0 | Kelola Master Kegiatan | Data kegiatan (tambah/edit/hapus) | Daftar kegiatan | CRUD data master kegiatan |
| 2.0 | Kelola Perencanaan | Data rencana (tgl, kegiatan, jam) | Daftar rencana | CRUD rencana harian |
| 3.0 | Kelola Catatan Harian | Data catatan (tgl, kegiatan, deskripsi) | Daftar catatan | CRUD catatan harian |
| 4.0 | Laporan & Filter | Parameter filter (tanggal) | Data yang difilter | Menyaring data berdasarkan tanggal |

### Detail Data Store

| Kode | Nama Store | Struktur Data |
|------|------------|---------------|
| D1 | kegiatan | id_kegiatan, nama_kegiatan, deskripsi, status, created_at, updated_at |
| D2 | perencanaan | id_rencana, id_kegiatan, tanggal, jam_mulai, jam_selesai, catatan, status, created_at, updated_at |
| D3 | catatan_harian | id_catatan, id_kegiatan, tanggal, jam_mulai, jam_selesai, deskripsi, status, created_at, updated_at |

### Aliran Data Antar Proses

```
Proses 1.0 ──(master_kegiatan)──► Proses 4.0  (data master untuk ditampilkan)
Proses 2.0 ──(data_rencana)────► Proses 4.0  (data rencana untuk difilter)
Proses 3.0 ──(data_catatan)────► Proses 4.0  (data catatan untuk difilter)

Proses 4.0 ──(filter_params)───► Proses 2.0  (filter diterapkan ke daftar rencana)
Proses 4.0 ──(filter_params)───► Proses 3.0  (filter diterapkan ke daftar catatan)
```

---

---

## Task 7: Desain Struktur Database (SQLite DDL)

### Script DDL untuk SQLite

```sql
-- ============================================================
-- DATABASE: catatan_harian.db
-- SISTEM: Catatan Harian Kerja
-- DESKRIPSI: Script DDL untuk membuat tabel-tabel database
-- ============================================================

-- Enable foreign key constraints
PRAGMA foreign_keys = ON;

-- ------------------------------------------------------------
-- Tabel 1: kegiatan (Master Data Kegiatan)
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS kegiatan (
    id_kegiatan    INTEGER PRIMARY KEY AUTOINCREMENT,
    nama_kegiatan  VARCHAR(200) NOT NULL,
    deskripsi      TEXT DEFAULT NULL,
    status         VARCHAR(20) NOT NULL DEFAULT 'aktif'
                   CHECK (status IN ('aktif', 'nonaktif')),
    created_at     DATETIME NOT NULL DEFAULT (datetime('now','localtime')),
    updated_at     DATETIME NOT NULL DEFAULT (datetime('now','localtime'))
);

-- Unique constraint on nama_kegiatan
CREATE UNIQUE INDEX IF NOT EXISTS idx_kegiatan_nama ON kegiatan(nama_kegiatan);

-- ------------------------------------------------------------
-- Tabel 2: perencanaan (Rencana Harian)
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS perencanaan (
    id_rencana     INTEGER PRIMARY KEY AUTOINCREMENT,
    id_kegiatan    INTEGER NOT NULL,
    tanggal        DATE NOT NULL,
    jam_mulai      TIME DEFAULT NULL,
    jam_selesai    TIME DEFAULT NULL,
    catatan        TEXT DEFAULT NULL,
    status         VARCHAR(20) NOT NULL DEFAULT 'direncanakan'
                   CHECK (status IN ('direncanakan', 'selesai', 'batal')),
    created_at     DATETIME NOT NULL DEFAULT (datetime('now','localtime')),
    updated_at     DATETIME NOT NULL DEFAULT (datetime('now','localtime')),
    
    -- Foreign Key
    CONSTRAINT fk_perencanaan_kegiatan
        FOREIGN KEY (id_kegiatan)
        REFERENCES kegiatan(id_kegiatan)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- Index untuk filter by tanggal
CREATE INDEX IF NOT EXISTS idx_perencanaan_tanggal ON perencanaan(tanggal);

-- Index untuk filter by kegiatan
CREATE INDEX IF NOT EXISTS idx_perencanaan_kegiatan ON perencanaan(id_kegiatan);

-- ------------------------------------------------------------
-- Tabel 3: catatan_harian (Log Kegiatan Harian)
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS catatan_harian (
    id_catatan     INTEGER PRIMARY KEY AUTOINCREMENT,
    id_kegiatan    INTEGER NOT NULL,
    tanggal        DATE NOT NULL,
    jam_mulai      TIME DEFAULT NULL,
    jam_selesai    TIME DEFAULT NULL,
    deskripsi      TEXT NOT NULL,
    status         VARCHAR(20) NOT NULL DEFAULT 'selesai'
                   CHECK (status IN ('selesai', 'proses', 'tertunda')),
    created_at     DATETIME NOT NULL DEFAULT (datetime('now','localtime')),
    updated_at     DATETIME NOT NULL DEFAULT (datetime('now','localtime')),
    
    -- Foreign Key
    CONSTRAINT fk_catatan_kegiatan
        FOREIGN KEY (id_kegiatan)
        REFERENCES kegiatan(id_kegiatan)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- Index for filter by tanggal
CREATE INDEX IF NOT EXISTS idx_catatan_tanggal ON catatan_harian(tanggal);

-- Index for filter by kegiatan
CREATE INDEX IF NOT EXISTS idx_catatan_kegiatan ON catatan_harian(id_kegiatan);

-- ------------------------------------------------------------
-- Trigger: Auto-update updated_at for kegiatan
-- ------------------------------------------------------------
CREATE TRIGGER IF NOT EXISTS trg_kegiatan_updated
    AFTER UPDATE ON kegiatan
    FOR EACH ROW
BEGIN
    UPDATE kegiatan SET updated_at = datetime('now','localtime')
    WHERE id_kegiatan = OLD.id_kegiatan;
END;

-- ------------------------------------------------------------
-- Trigger: Auto-update updated_at for perencanaan
-- ------------------------------------------------------------
CREATE TRIGGER IF NOT EXISTS trg_perencanaan_updated
    AFTER UPDATE ON perencanaan
    FOR EACH ROW
BEGIN
    UPDATE perencanaan SET updated_at = datetime('now','localtime')
    WHERE id_rencana = OLD.id_rencana;
END;

-- ------------------------------------------------------------
-- Trigger: Auto-update updated_at for catatan_harian
-- ------------------------------------------------------------
CREATE TRIGGER IF NOT EXISTS trg_catatan_updated
    AFTER UPDATE ON catatan_harian
    FOR EACH ROW
BEGIN
    UPDATE catatan_harian SET updated_at = datetime('now','localtime')
    WHERE id_catatan = OLD.id_catatan;
END;

-- ------------------------------------------------------------
-- Sample Data (Optional - untuk testing)
-- ------------------------------------------------------------
-- INSERT INTO kegiatan (nama_kegiatan, deskripsi) VALUES
--     ('Meeting Pagi', 'Meeting harian dengan tim'),
--     ('Coding', 'Mengembangkan fitur aplikasi'),
--     ('Review Code', 'Code review pull request'),
--     ('Menulis Laporan', 'Membuat laporan progress'),
--     ('Testing', 'Testing aplikasi');
```

### Ringkasan Database

| Item | Detail |
|------|--------|
| **DBMS** | SQLite 3 |
| **File Database** | `catatan_harian.db` |
| **Jumlah Tabel** | 3 tabel |
| **Jumlah Index** | 5 index |
| **Jumlah Trigger** | 3 trigger |
| **Foreign Key** | 2 relasi FK dengan CASCADE |
| **Constraints** | NOT NULL, UNIQUE, CHECK, DEFAULT |

---

---

## Task 8: Desain Form-Form UI

### Daftar Form yang Diperlukan

| No | Nama Form | Halaman | Method | Fields |
|----|-----------|---------|--------|--------|
| F1 | Form Tambah/Edit Kegiatan | /kegiatan/form | GET/POST | nama_kegiatan, deskripsi, status |
| F2 | Form Buat Rencana | /rencana/form | GET/POST | tanggal, id_kegiatan, jam_mulai, jam_selesai, catatan |
| F3 | Form Catat Harian | /catatan/form | GET/POST | tanggal, id_kegiatan, jam_mulai, jam_selesai, deskripsi, status |
| F4 | Form Filter Tanggal | Semua halaman daftar | GET | tanggal_mulai, tanggal_selesai |
| F5 | Form Konfirmasi Hapus | Modal di halaman daftar | POST | id (tersembunyi) |

### Detail Form

#### F1: Form Tambah/Edit Kegiatan

```
┌──────────────────────────────────────────────┐
│  ✏️ {Tambah/Edit} Master Kegiatan            │
│                                              │
│  Nama Kegiatan *                              │
│  ┌──────────────────────────────────────────┐│
│  │ Contoh: Meeting Pagi                     ││
│  └──────────────────────────────────────────┘│
│                                              │
│  Deskripsi                                   │
│  ┌──────────────────────────────────────────┐│
│  │ Meeting harian untuk review progress...  ││
│  └──────────────────────────────────────────┘│
│                                              │
│  Status                                      │
│  ┌──────────────────────────────────────────┐│
│  │ [▼] Aktif                                ││
│  └──────────────────────────────────────────┘│
│                                              │
│      [💾 Simpan]      [✖ Batal]             │
└──────────────────────────────────────────────┘
```

#### F2: Form Buat Rencana Harian

```
┌──────────────────────────────────────────────┐
│  📅 Buat Rencana Harian                      │
│                                              │
│  Tanggal *                                   │
│  ┌──────────────────────────────────────────┐│
│  │ [📆 2026-05-09]                          ││
│  └──────────────────────────────────────────┘│
│                                              │
│  Kegiatan *                                  │
│  ┌──────────────────────────────────────────┐│
│  │ [▼ Pilih Kegiatan...]                    ││
│  │  ├ Meeting Pagi                          ││
│  │  ├ Coding                                ││
│  │  ├ Review Code                           ││
│  │  └ ...                                   ││
│  └──────────────────────────────────────────┘│
│                                              │
│  Jam Mulai           Jam Selesai             │
│  ┌──────────┐        ┌──────────┐           │
│  │ 08:00    │        │ 09:00    │           │
│  └──────────┘        └──────────┘           │
│                                              │
│  Catatan                                     │
│  ┌──────────────────────────────────────────┐│
│  │ Catatan tambahan (opsional)...           ││
│  └──────────────────────────────────────────┘│
│                                              │
│      [💾 Simpan]      [✖ Batal]             │
└──────────────────────────────────────────────┘
```

#### F3: Form Catat Harian

```
┌──────────────────────────────────────────────┐
│  📝 Catat Kegiatan Hari Ini                  │
│                                              │
│  Tanggal *                                   │
│  ┌──────────────────────────────────────────┐│
│  │ [📆 2026-05-09] (Default: hari ini)     ││
│  └──────────────────────────────────────────┘│
│                                              │
│  Kegiatan *                                  │
│  ┌──────────────────────────────────────────┐│
│  │ [▼ Pilih Kegiatan...]                    ││
│  └──────────────────────────────────────────┘│
│                                              │
│  Jam Mulai           Jam Selesai             │
│  ┌──────────┐        ┌──────────┐           │
│  │ 10:00    │        │ 12:00    │           │
│  └──────────┘        └──────────┘           │
│                                              │
│  Deskripsi / Hasil *                         │
│  ┌──────────────────────────────────────────┐│
│  │ Jelaskan apa yang sudah dikerjakan...    ││
│  └──────────────────────────────────────────┘│
│                                              │
│  Status                                      │
│  ┌──────────────────────────────────────────┐│
│  │ [▼ Selesai]                              ││
│  └──────────────────────────────────────────┘│
│                                              │
│      [💾 Simpan]      [✖ Batal]             │
└──────────────────────────────────────────────┘
```

#### F4: Form Filter Tanggal

```
┌──────────────────────────────────────────────┐
│  🔍 Filter                                   │
│                                              │
│  Dari Tanggal          Sampai Tanggal        │
│  ┌──────────────┐      ┌──────────────┐     │
│  │ 2026-05-01   │      │ 2026-05-09   │     │
│  └──────────────┘      └──────────────┘     │
│                                              │
│       [🔍 Terapkan Filter]  [✖ Reset]      │
└──────────────────────────────────────────────┘
```

#### F5: Modal Konfirmasi Hapus

```
┌──────────────────────────────────────────────┐
│  ⚠️ Konfirmasi Hapus                         │
│                                              │
│  Apakah Anda yakin ingin menghapus            │
│  "[Nama Kegiatan]"?                          │
│                                              │
│  Data yang sudah dihapus tidak bisa           │
│  dikembalikan.                                │
│                                              │
│    [🗑 Ya, Hapus]    [✖ Batal]              │
└──────────────────────────────────────────────┘
```

### Aturan Validasi Per Field

| Form | Field | Aturan Validasi |
|------|-------|-----------------|
| F1 | nama_kegiatan | Required, max 200 karakter, unique |
| F1 | deskripsi | Optional, max 1000 karakter |
| F2 | tanggal | Required, format YYYY-MM-DD |
| F2 | id_kegiatan | Required, harus dari daftar kegiatan aktif |
| F2 | jam_mulai | Optional, format HH:MM |
| F2 | jam_selesai | Optional, format HH:MM, harus > jam_mulai |
| F3 | tanggal | Required, format YYYY-MM-DD |
| F3 | id_kegiatan | Required, harus dari daftar kegiatan aktif |
| F3 | deskripsi | Required, max 2000 karakter |
| F3 | jam_mulai | Optional, format HH:MM |
| F3 | jam_selesai | Optional, format HH:MM |

---

---

## Task 9: Desain REST API Endpoint

### Daftar Endpoint API

| Kode | Method | Endpoint | Fungsi | Request Body / Params | Response |
|------|--------|----------|--------|-----------------------|----------|
| API-01 | GET | `/api/kegiatan` | Ambil semua kegiatan | - | JSON array kegiatan |
| API-02 | GET | `/api/kegiatan/{id}` | Ambil satu kegiatan | - | JSON kegiatan |
| API-03 | POST | `/api/kegiatan` | Tambah kegiatan baru | nama_kegiatan, deskripsi | JSON kegiatan baru |
| API-04 | POST | `/api/kegiatan/{id}/edit` | Edit kegiatan | nama_kegiatan, deskripsi, status | JSON kegiatan update |
| API-05 | POST | `/api/kegiatan/{id}/hapus` | Hapus kegiatan | - | JSON sukses/gagal |
| API-06 | GET | `/api/rencana` | Ambil daftar rencana | ?tanggal=YYYY-MM-DD (opsional) | JSON array rencana |
| API-07 | GET | `/api/rencana/{id}` | Ambil satu rencana | - | JSON rencana |
| API-08 | POST | `/api/rencana` | Tambah rencana baru | tanggal, id_kegiatan, jam, catatan | JSON rencana baru |
| API-09 | POST | `/api/rencana/{id}/edit` | Edit rencana | tanggal, id_kegiatan, jam, catatan, status | JSON rencana update |
| API-10 | POST | `/api/rencana/{id}/hapus` | Hapus rencana | - | JSON sukses/gagal |
| API-11 | GET | `/api/catatan` | Ambil daftar catatan | ?tanggal=YYYY-MM-DD (opsional) | JSON array catatan |
| API-12 | GET | `/api/catatan/{id}` | Ambil satu catatan | - | JSON catatan |
| API-13 | POST | `/api/catatan` | Tambah catatan baru | tanggal, id_kegiatan, jam, deskripsi, status | JSON catatan baru |
| API-14 | POST | `/api/catatan/{id}/edit` | Edit catatan | tanggal, id_kegiatan, jam, deskripsi, status | JSON catatan update |
| API-15 | POST | `/api/catatan/{id}/hapus` | Hapus catatan | - | JSON sukses/gagal |
| API-16 | GET | `/api/filter` | Filter data by tanggal | type=(rencana/catatan), tanggal_mulai, tanggal_selesai | JSON array data |

### Detail Endpoint

#### API-01: GET /api/kegiatan
```
Request:
  GET /api/kegiatan

Response Success (200):
{
  "status": "success",
  "data": [
    {
      "id_kegiatan": 1,
      "nama_kegiatan": "Meeting Pagi",
      "deskripsi": "Meeting harian dengan tim",
      "status": "aktif",
      "created_at": "2026-05-09 08:00:00",
      "updated_at": "2026-05-09 08:00:00"
    }
  ],
  "total": 5
}
```

#### API-03: POST /api/kegiatan
```
Request:
  POST /api/kegiatan
  Content-Type: application/x-www-form-urlencoded
  
  nama_kegiatan=Meeting Pagi
  deskripsi=Meeting harian dengan tim

Response Success (201):
{
  "status": "success",
  "message": "Kegiatan berhasil ditambahkan",
  "data": {
    "id_kegiatan": 1,
    "nama_kegiatan": "Meeting Pagi",
    "deskripsi": "Meeting harian dengan tim",
    "status": "aktif"
  }
}

Response Error (400):
{
  "status": "error",
  "message": "Nama kegiatan sudah ada"
}
```

#### API-06: GET /api/rencana (dengan filter)
```
Request:
  GET /api/rencana?tanggal=2026-05-09

Response Success (200):
{
  "status": "success",
  "data": [
    {
      "id_rencana": 1,
      "id_kegiatan": 1,
      "nama_kegiatan": "Meeting Pagi",
      "tanggal": "2026-05-09",
      "jam_mulai": "08:00",
      "jam_selesai": "09:00",
      "catatan": "Meeting sprint planning",
      "status": "direncanakan"
    }
  ],
  "total": 3
}
```

#### API-08: POST /api/rencana
```
Request:
  POST /api/rencana
  Content-Type: application/x-www-form-urlencoded
  
  tanggal=2026-05-09
  id_kegiatan=1
  jam_mulai=08:00
  jam_selesai=09:00
  catatan=Meeting sprint planning

Response Success (201):
{
  "status": "success",
  "message": "Rencana berhasil ditambahkan",
  "data": {
    "id_rencana": 1,
    "tanggal": "2026-05-09",
    "id_kegiatan": 1,
    "status": "direncanakan"
  }
}
```

#### API-16: GET /api/filter
```
Request:
  GET /api/filter?type=catatan&tanggal_mulai=2026-05-01&tanggal_selesai=2026-05-09

Response Success (200):
{
  "status": "success",
  "type": "catatan",
  "data": [
    {
      "id_catatan": 1,
      "nama_kegiatan": "Meeting Pagi",
      "tanggal": "2026-05-09",
      "deskripsi": "Meeting sprint planning",
      "status": "selesai"
    }
  ],
  "total": 2,
  "filter": {
    "tanggal_mulai": "2026-05-01",
    "tanggal_selesai": "2026-05-09"
  }
}
```

### Standard Response Format

Semua API mengembalikan JSON dengan format standar:

```json
// Success Response
{
  "status": "success",
  "message": "Pesan sukses (opsional)",
  "data": { ... } | [ ... ],
  "total": 0 (opsional untuk daftar)
}

// Error Response
{
  "status": "error",
  "message": "Deskripsi error",
  "errors": { ... } (opsional, detail validasi)
}
```

### HTTP Status Codes

| Kode | Penggunaan |
|------|------------|
| 200 | GET success, POST success |
| 201 | POST create success |
| 400 | Bad request, validasi gagal |
| 404 | Data tidak ditemukan |
| 409 | Konflik (duplikat data) |
| 500 | Internal server error |

---

---

## Task 10: Desain Struktur Direktori Proyek Python

### Struktur Folder Clean Architecture Python

```
catatan-harian/
├── app.py                              # Entry point - Flask app initialization
├── requirements.txt                    # Dependencies
├── catatan_harian.db                   # SQLite database (auto-generated)
│
├── src/
│   ├── __init__.py
│   │
│   ├── domain/                         # DOMAIN LAYER
│   │   ├── __init__.py
│   │   ├── entities/
│   │   │   ├── __init__.py
│   │   │   ├── kegiatan.py             # Kegiatan entity
│   │   │   ├── perencanaan.py          # Perencanaan entity
│   │   │   └── catatan_harian.py       # CatatanHarian entity
│   │   └── repositories/
│   │       ├── __init__.py
│   │       ├── kegiatan_repo.py        # Interface KegiatanRepository
│   │       ├── perencanaan_repo.py     # Interface PerencanaanRepository
│   │       └── catatan_repo.py         # Interface CatatanRepository
│   │
│   ├── application/                    # APPLICATION LAYER (Use Cases)
│   │   ├── __init__.py
│   │   ├── use_cases/
│   │   │   ├── __init__.py
│   │   │   ├── kelola_kegiatan.py      # UC-01: Kelola Master Kegiatan
│   │   │   ├── buat_rencana.py         # UC-02: Buat Rencana Harian
│   │   │   ├── catat_harian.py         # UC-03: Catat Kegiatan Harian
│   │   │   └── lihat_daftar.py         # UC-04/05/06/07: Lihat & Filter
│   │   └── dto/
│   │       ├── __init__.py
│   │       ├── kegiatan_dto.py         # Data Transfer Object untuk Kegiatan
│   │       ├── rencana_dto.py          # DTO untuk Perencanaan
│   │       └── catatan_dto.py          # DTO untuk CatatanHarian
│   │
│   ├── infrastructure/                 # INFRASTRUCTURE LAYER
│   │   ├── __init__.py
│   │   ├── database/
│   │   │   ├── __init__.py
│   │   │   ├── db_connection.py        # SQLite connection management
│   │   │   └── schema.sql              # DDL script
│   │   └── repositories/
│   │       ├── __init__.py
│   │       ├── sqlite_kegiatan_repo.py     # Implementation KegiatanRepository
│   │       ├── sqlite_perencanaan_repo.py  # Implementation PerencanaanRepository
│   │       └── sqlite_catatan_repo.py      # Implementation CatatanRepository
│   │
│   └── interface/                      # INTERFACE LAYER (Presentation)
│       ├── __init__.py
│       ├── controllers/
│       │   ├── __init__.py
│       │   ├── kegiatan_controller.py  # Handler untuk /kegiatan
│       │   ├── rencana_controller.py   # Handler untuk /rencana
│       │   └── catatan_controller.py   # Handler untuk /catatan
│       └── templates/
│           ├── base.html               # Template base (layout)
│           ├── components/             # Komponen reusable (navbar, sidebar, card)
│           │   ├── navbar.html
│           │   ├── footer.html
│           │   ├── modal_hapus.html
│           │   └── filter_tanggal.html
│           ├── kegiatan/
│           │   ├── daftar.html         # Halaman daftar master kegiatan
│           │   └── form.html           # Halaman tambah/edit kegiatan
│           ├── rencana/
│           │   ├── daftar.html         # Halaman daftar rencana
│           │   └── form.html           # Halaman buat rencana
│           └── catatan/
│               ├── daftar.html         # Halaman daftar catatan harian
│               └── form.html           # Halaman catat harian
```

### Penjelasan Setiap Folder

| Folder | Layer | Tanggung Jawab |
|--------|-------|----------------|
| `domain/` | Domain | Entities & Repository interfaces (tidak bergantung pada layer lain) |
| `application/` | Application | Use cases / inter actors (logika bisnis murni) |
| `infrastructure/` | Infrastructure | Implementasi database & repository (SQLite) |
| `interface/` | Interface | HTTP handlers, controllers, HTML templates |

### Dependency Rule

```
interface/  →  application/  →  domain/
    ↑               ↑               ↑
    |  (menggunakan)  |  (menggunakan) |
    |               |               |
infrastructure/  →  domain/         |
    ↑                               |
    |  (menggunakan)                 |
    └───────────────────────────────┘
```

---

---

## Task 11: Desain Routing URL

### Daftar Route Halaman (Server-Side Rendering)

| Kode | Method | URL Route | Fungsi | Controller |
|------|--------|-----------|--------|------------|
| R-01 | GET | `/` | Halaman Dashboard (home) | DashboardController.index |
| R-02 | GET | `/kegiatan` | Daftar master kegiatan | KegiatanController.index |
| R-03 | GET | `/kegiatan/tambah` | Form tambah kegiatan | KegiatanController.create |
| R-04 | POST | `/kegiatan` | Simpan kegiatan baru | KegiatanController.store |
| R-05 | GET | `/kegiatan/{id}/edit` | Form edit kegiatan | KegiatanController.edit |
| R-06 | POST | `/kegiatan/{id}/update` | Update kegiatan | KegiatanController.update |
| R-07 | POST | `/kegiatan/{id}/hapus` | Hapus kegiatan | KegiatanController.destroy |
| R-08 | GET | `/rencana` | Daftar rencana harian | RencanaController.index |
| R-09 | GET | `/rencana/tambah` | Form buat rencana | RencanaController.create |
| R-10 | POST | `/rencana` | Simpan rencana baru | RencanaController.store |
| R-11 | GET | `/rencana/{id}/edit` | Form edit rencana | RencanaController.edit |
| R-12 | POST | `/rencana/{id}/update` | Update rencana | RencanaController.update |
| R-13 | POST | `/rencana/{id}/hapus` | Hapus rencana | RencanaController.destroy |
| R-14 | GET | `/catatan` | Daftar catatan harian | CatatanController.index |
| R-15 | GET | `/catatan/tambah` | Form catat harian | CatatanController.create |
| R-16 | POST | `/catatan` | Simpan catatan baru | CatatanController.store |
| R-17 | GET | `/catatan/{id}/edit` | Form edit catatan | CatatanController.edit |
| R-18 | POST | `/catatan/{id}/update` | Update catatan | CatatanController.update |
| R-19 | POST | `/catatan/{id}/hapus` | Hapus catatan | CatatanController.destroy |

### Daftar Route API (JSON Response)

| Kode | Method | URL Route | Fungsi |
|------|--------|-----------|--------|
| A-01 | GET | `/api/kegiatan` | API: ambil semua kegiatan |
| A-02 | GET | `/api/kegiatan/{id}` | API: ambil satu kegiatan |
| A-03 | POST | `/api/kegiatan` | API: tambah kegiatan |
| A-04 | GET | `/api/rencana` | API: ambil daftar rencana (?tanggal=) |
| A-05 | POST | `/api/rencana` | API: tambah rencana |
| A-06 | GET | `/api/catatan` | API: ambil daftar catatan (?tanggal=) |
| A-07 | POST | `/api/catatan` | API: tambah catatan |
| A-08 | GET | `/api/filter` | API: filter data by tanggal |

### Mapping Controller dan Method

```python
# app.py - Flask Route Registration

# HTML Pages (Server Render)
routes_html = {
    # Dashboard
    "GET": {
        "/": "dashboard_controller.index",
    },
    
    # Kegiatan
    "GET": {
        "/kegiatan": "kegiatan_controller.index",
        "/kegiatan/tambah": "kegiatan_controller.create",
        "/kegiatan/<int:id>/edit": "kegiatan_controller.edit",
    },
    "POST": {
        "/kegiatan": "kegiatan_controller.store",
        "/kegiatan/<int:id>/update": "kegiatan_controller.update",
        "/kegiatan/<int:id>/hapus": "kegiatan_controller.destroy",
    },
    
    # Rencana
    "GET": {
        "/rencana": "rencana_controller.index",
        "/rencana/tambah": "rencana_controller.create",
        "/rencana/<int:id>/edit": "rencana_controller.edit",
    },
    "POST": {
        "/rencana": "rencana_controller.store",
        "/rencana/<int:id>/update": "rencana_controller.update",
        "/rencana/<int:id>/hapus": "rencana_controller.destroy",
    },
    
    # Catatan
    "GET": {
        "/catatan": "catatan_controller.index",
        "/catatan/tambah": "catatan_controller.create",
        "/catatan/<int:id>/edit": "catatan_controller.edit",
    },
    "POST": {
        "/catatan": "catatan_controller.store",
        "/catatan/<int:id>/update": "catatan_controller.update",
        "/catatan/<int:id>/hapus": "catatan_controller.destroy",
    },
}

# API Routes (JSON)
routes_api = {
    "GET": {
        "/api/kegiatan": "api_kegiatan_controller.index",
        "/api/kegiatan/<int:id>": "api_kegiatan_controller.show",
        "/api/rencana": "api_rencana_controller.index",
        "/api/catatan": "api_catatan_controller.index",
        "/api/filter": "api_filter_controller.index",
    },
    "POST": {
        "/api/kegiatan": "api_kegiatan_controller.store",
        "/api/rencana": "api_rencana_controller.store",
        "/api/catatan": "api_catatan_controller.store",
    },
}
```

### Ringkasan Route

| Tipe | Jumlah Route |
|------|-------------|
| HTML Pages (GET) | 10 route |
| HTML Actions (POST) | 9 route |
| API (GET) | 5 route |
| API (POST) | 3 route |
| **Total** | **27 route** |

---

---

## Task 12: Desain Template HTML

### Daftar Template yang Diperlukan

| Kode | Template | Halaman | Keterangan |
|------|----------|---------|------------|
| T-01 | `base.html` | Semua halaman | Layout utama (navbar, sidebar, footer) |
| T-02 | `dashboard.html` | `/` | Halaman dashboard utama |
| T-03 | `kegiatan/daftar.html` | `/kegiatan` | Daftar master kegiatan |
| T-04 | `kegiatan/form.html` | `/kegiatan/tambah`, `/kegiatan/{id}/edit` | Form tambah/edit kegiatan |
| T-05 | `rencana/daftar.html` | `/rencana` | Daftar rencana harian |
| T-06 | `rencana/form.html` | `/rencana/tambah`, `/rencana/{id}/edit` | Form buat/edit rencana |
| T-07 | `catatan/daftar.html` | `/catatan` | Daftar catatan harian |
| T-08 | `catatan/form.html` | `/catatan/tambah`, `/catatan/{id}/edit` | Form catat/edit harian |

### Desain Template: base.html (Layout Utama)

```html
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Catatan Harian{% endblock %}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    {% block extra_head %}{% endblock %}
</head>
<body class="bg-gray-50 min-h-screen">
    
    <!-- Navbar -->
    <nav class="bg-blue-600 text-white shadow-lg">
        <div class="container mx-auto px-4">
            <div class="flex items-center justify-between h-16">
                <!-- Logo / Brand -->
                <a href="/" class="flex items-center space-x-2">
                    <span class="text-2xl">📋</span>
                    <span class="font-bold text-xl hidden sm:block">Catatan Harian</span>
                </a>
                
                <!-- Mobile Menu Button -->
                <button id="menu-toggle" class="sm:hidden p-2 rounded hover:bg-blue-700">
                    <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/>
                    </svg>
                </button>
                
                <!-- Desktop Menu -->
                <div class="hidden sm:flex items-center space-x-4">
                    <a href="/" class="px-3 py-2 rounded hover:bg-blue-700 transition">Dashboard</a>
                    <a href="/kegiatan" class="px-3 py-2 rounded hover:bg-blue-700 transition">Kegiatan</a>
                    <a href="/rencana" class="px-3 py-2 rounded hover:bg-blue-700 transition">Rencana</a>
                    <a href="/catatan" class="px-3 py-2 rounded hover:bg-blue-700 transition">Catatan</a>
                </div>
            </div>
        </div>
        
        <!-- Mobile Menu (hidden by default) -->
        <div id="mobile-menu" class="hidden sm:hidden bg-blue-700 pb-4">
            <a href="/" class="block px-4 py-2 hover:bg-blue-800">Dashboard</a>
            <a href="/kegiatan" class="block px-4 py-2 hover:bg-blue-800">Kegiatan</a>
            <a href="/rencana" class="block px-4 py-2 hover:bg-blue-800">Rencana</a>
            <a href="/catatan" class="block px-4 py-2 hover:bg-blue-800">Catatan</a>
        </div>
    </nav>
    
    <!-- Main Content -->
    <main class="container mx-auto px-4 py-6">
        <!-- Flash Messages -->
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="mb-4 p-4 rounded-lg {% if category == 'error' %}bg-red-100 text-red-700{% else %}bg-green-100 text-green-700{% endif %}">
                        {{ message }}
                    </div>
                {% endfor %}
            {% endif %}
        {% endwith %}
        
        <!-- Page Content -->
        {% block content %}{% endblock %}
    </main>
    
    <!-- Footer -->
    <footer class="bg-gray-100 border-t mt-8 py-4">
        <div class="container mx-auto px-4 text-center text-gray-500 text-sm">
            &copy; 2026 Sistem Catatan Harian Kerja
        </div>
    </footer>
    
    <!-- Mobile Menu Toggle Script -->
    <script>
        document.getElementById('menu-toggle')?.addEventListener('click', function() {
            const menu = document.getElementById('mobile-menu');
            menu.classList.toggle('hidden');
        });
    </script>
    
    {% block extra_scripts %}{% endblock %}
</body>
</html>
```

### Desain Template: kegiatan/daftar.html (Daftar Master Kegiatan)

```html
{% extends "base.html" %}

{% block title %}Daftar Kegiatan - Catatan Harian{% endblock %}

{% block content %}
<div class="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-6 gap-4">
    <h1 class="text-2xl font-bold text-gray-800">📋 Master Kegiatan</h1>
    <a href="/kegiatan/tambah" 
       class="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition w-full sm:w-auto text-center">
        + Tambah Kegiatan
    </a>
</div>

<!-- Search / Filter -->
<div class="mb-6">
    <input type="text" id="search-kegiatan" placeholder="Cari kegiatan..." 
           class="w-full sm:w-96 px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500">
</div>

<!-- Daftar Kegiatan - Desktop Table -->
<div class="hidden md:block bg-white rounded-lg shadow overflow-x-auto">
    <table class="w-full">
        <thead class="bg-gray-100">
            <tr>
                <th class="px-4 py-3 text-left text-sm font-semibold text-gray-600">No</th>
                <th class="px-4 py-3 text-left text-sm font-semibold text-gray-600">Nama Kegiatan</th>
                <th class="px-4 py-3 text-left text-sm font-semibold text-gray-600">Deskripsi</th>
                <th class="px-4 py-3 text-center text-sm font-semibold text-gray-600">Status</th>
                <th class="px-4 py-3 text-center text-sm font-semibold text-gray-600">Aksi</th>
            </tr>
        </thead>
        <tbody class="divide-y divide-gray-200">
            {% for kegiatan in data %}
            <tr class="hover:bg-gray-50">
                <td class="px-4 py-3 text-sm">{{ loop.index }}</td>
                <td class="px-4 py-3 text-sm font-medium">{{ kegiatan.nama_kegiatan }}</td>
                <td class="px-4 py-3 text-sm text-gray-500">{{ kegiatan.deskripsi or '-' }}</td>
                <td class="px-4 py-3 text-center">
                    {% if kegiatan.status == 'aktif' %}
                        <span class="bg-green-100 text-green-700 px-2 py-1 rounded-full text-xs">Aktif</span>
                    {% else %}
                        <span class="bg-red-100 text-red-700 px-2 py-1 rounded-full text-xs">Nonaktif</span>
                    {% endif %}
                </td>
                <td class="px-4 py-3 text-center">
                    <a href="/kegiatan/{{ kegiatan.id_kegiatan }}/edit" 
                       class="text-blue-600 hover:text-blue-800 mr-2">✏️ Edit</a>
                    <button onclick="confirmHapus('kegiatan', {{ kegiatan.id_kegiatan }}, '{{ kegiatan.nama_kegiatan }}')"
                            class="text-red-600 hover:text-red-800">🗑 Hapus</button>
                </td>
            </tr>
            {% else %}
            <tr>
                <td colspan="5" class="px-4 py-8 text-center text-gray-500">
                    Belum ada data kegiatan. <a href="/kegiatan/tambah" class="text-blue-600 hover:underline">Tambah sekarang</a>
                </td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</div>

<!-- Daftar Kegiatan - Mobile Card -->
<div class="md:hidden space-y-4">
    {% for kegiatan in data %}
    <div class="bg-white rounded-lg shadow p-4">
        <div class="flex justify-between items-start mb-2">
            <h3 class="font-semibold text-gray-800">{{ kegiatan.nama_kegiatan }}</h3>
            {% if kegiatan.status == 'aktif' %}
                <span class="bg-green-100 text-green-700 px-2 py-1 rounded-full text-xs">Aktif</span>
            {% else %}
                <span class="bg-red-100 text-red-700 px-2 py-1 rounded-full text-xs">Nonaktif</span>
            {% endif %}
        </div>
        <p class="text-sm text-gray-500 mb-3">{{ kegiatan.deskripsi or 'Tidak ada deskripsi' }}</p>
        <div class="flex space-x-3">
            <a href="/kegiatan/{{ kegiatan.id_kegiatan }}/edit" 
               class="text-blue-600 text-sm hover:underline">✏️ Edit</a>
            <button onclick="confirmHapus('kegiatan', {{ kegiatan.id_kegiatan }}, '{{ kegiatan.nama_kegiatan }}')"
                    class="text-red-600 text-sm hover:underline">🗑 Hapus</button>
        </div>
    </div>
    {% else %}
    <div class="bg-white rounded-lg shadow p-8 text-center text-gray-500">
        Belum ada data kegiatan.
    </div>
    {% endfor %}
</div>

<!-- Modal Hapus -->
{% include "components/modal_hapus.html" %}

{% endblock %}

{% block extra_scripts %}
<script>
// Search filter functionality
document.getElementById('search-kegiatan')?.addEventListener('keyup', function() {
    const keyword = this.value.toLowerCase();
    // Implementasi filter client-side atau reload dengan parameter
});
</script>
{% endblock %}
```

### Ringkasan Template

| Template | Layout | Fitur Responsive |
|----------|--------|------------------|
| `base.html` | Sidebar horizontal + main content | Navbar collapse ke hamburger di HP |
| `daftar.html` | Tabel (desktop) / Card (mobile) | Auto switch antara tabel ↔ card |
| `form.html` | Form vertikal dengan input | Full width di HP, max-width di PC |
| `modal_hapus.html` | Overlay centered | Full screen overlay di HP |

### Prinsip Desain Template

1. **Mobile-First**: Template dirancang untuk HP dulu (0-450px), lalu diperluas ke tablet (450-999px) dan PC (999px+)
2. **Tailwind Utility**: Semua styling menggunakan Tailwind utility classes
3. **Jinja2 Template**: Menggunakan template engine Jinja2 untuk server-side rendering
4. **Komponen Reusable**: Navbar, footer, modal, dan filter_tanggal dipisah ke folder `components/`
5. **Fungsi handler di base.html**: Konfirmasi Hapus menggunakan JavaScript fungsi global

---

---

## Task 13: Desain Alur Navigasi Aplikasi

### Peta Navigasi

```
                        ┌──────────────────┐
                        │                  │
                        │   DASHBOARD /    │
                        │   (Home Page)    │
                        │                  │
                        └────────┬─────────┘
                                 │
             ┌───────────────────┼───────────────────┐
             │                   │                   │
             ▼                   ▼                   ▼
    ┌────────────────┐  ┌────────────────┐  ┌────────────────┐
    │  Master        │  │  Rencana       │  │  Catatan       │
    │  Kegiatan      │  │  Harian        │  │  Harian        │
    ├────────────────┤  ├────────────────┤  ├────────────────┤
    │  Daftar/Tabel  │  │  Daftar/Tabel  │  │  Daftar/Tabel  │
    │  + Tambah      │  │  + Buat        │  │  + Catat       │
    │  + Edit        │  │  + Edit        │  │  + Edit        │
    │  + Hapus       │  │  + Hapus       │  │  + Hapus       │
    │  + Filter      │  │  + Filter Tgl   │  │  + Filter Tgl  │
    └────────────────┘  └────────────────┘  └────────────────┘
```

### Alur Navigasi Detail

#### A. Alur Dashboard
```
Dashboard (/)
├── Melihat ringkasan statistik
│   ├── Total kegiatan aktif
│   ├── Rencana hari ini
│   ├── Catatan hari ini
│   └── Quick link ke setiap menu
└── Klik menu navigasi → pindah ke halaman terkait
```

#### B. Alur Master Kegiatan
```
/kegiatan (Daftar Kegiatan)
├── [Tambah] → /kegiatan/tambah (Form Tambah)
│              └── Submit → POST /kegiatan → redirect ke /kegiatan
│
├── [Edit] → /kegiatan/{id}/edit (Form Edit)
│             └── Submit → POST /kegiatan/{id}/update → redirect ke /kegiatan
│
├── [Hapus] → Modal Konfirmasi
│              └── Ya → POST /kegiatan/{id}/hapus → redirect ke /kegiatan
│
└── [Filter/Search] → Input search → reload dengan parameter query
```

#### C. Alur Rencana Harian
```
/rencana (Daftar Rencana)
├── [Buat Rencana] → /rencana/tambah (Form Buat Rencana)
│                    └── Submit → POST /rencana → redirect ke /rencana
│
├── [Edit] → /rencana/{id}/edit (Form Edit)
│             └── Submit → POST /rencana/{id}/update → redirect ke /rencana
│
├── [Hapus] → Modal Konfirmasi
│              └── Ya → POST /rencana/{id}/hapus → redirect ke /rencana
│
└── [Filter Tanggal] → Pilih tanggal → reload /rencana?tanggal=YYYY-MM-DD
```

#### D. Alur Catatan Harian
```
/catatan (Daftar Catatan)
├── [Catat Baru] → /catatan/tambah (Form Catat)
│                  └── Submit → POST /catatan → redirect ke /catatan
│
├── [Edit] → /catatan/{id}/edit (Form Edit)
│             └── Submit → POST /catatan/{id}/update → redirect ke /catatan
│
├── [Hapus] → Modal Konfirmasi
│              └── Ya → POST /catatan/{id}/hapus → redirect ke /catatan
│
└── [Filter Tanggal] → Pilih tanggal → reload /catatan?tanggal=YYYY-MM-DD
```

### Diagram State (Perubahan Status)

```
Kegiatan: [aktif] ⇄ [nonaktif]

Rencana: [direncanakan] → [selesai]
         [direncanakan] → [batal]

Catatan: [proses] → [selesai]
         [proses] → [tertunda]
```

### Aturan Navigasi

1. **Setiap halaman daftar** memiliki tombol "Tambah" di bagian atas (responsive: full width di HP)
2. **Setiap item** di daftar memiliki tombol Edit dan Hapus
3. **Filter tanggal** tersedia di halaman daftar rencana dan catatan
4. **Setelah submit form** (simpan/edit/hapus), redirect kembali ke halaman daftar
5. **Pesan flash** (sukses/error) ditampilkan di halaman setelah redirect
6. **Navigasi mobile** menggunakan hamburger menu yang bisa toggle

---

---

## Task 14: Desain Validasi & Error Handling

### Strategi Validasi

Sistem menggunakan **3 lapis validasi**:

| Lapisan | Level | Lokasi | Tujuan |
|---------|-------|--------|--------|
| L1 | Client-side | HTML + JavaScript | Validasi cepat sebelum submit, user experience |
| L2 | Server-side | Controller / Use Case | Validasi bisnis, keamanan data |
| L3 | Database | SQLite Constraints | Integritas data di level database |

### L1: Validasi Client-Side (HTML + JavaScript)

```html
<!-- Contoh validasi di form kegiatan -->
<form id="form-kegiatan" onsubmit="return validateForm()">
    <input type="text" id="nama_kegiatan" name="nama_kegiatan" 
           required maxlength="200"
           class="w-full px-4 py-2 border rounded-lg 
                  focus:outline-none focus:ring-2 focus:ring-blue-500
                  peer"
           oninvalid="this.setCustomValidity('Nama kegiatan harus diisi')"
           oninput="this.setCustomValidity('')">
    <p class="text-red-500 text-sm mt-1 hidden" id="error-nama">
        Nama kegiatan wajib diisi (maks. 200 karakter)
    </p>
</form>

<script>
function validateForm() {
    let valid = true;
    const nama = document.getElementById('nama_kegiatan').value.trim();
    
    if (!nama) {
        document.getElementById('error-nama').classList.remove('hidden');
        valid = false;
    } else if (nama.length > 200) {
        document.getElementById('error-nama').textContent = 'Maksimal 200 karakter';
        document.getElementById('error-nama').classList.remove('hidden');
        valid = false;
    } else {
        document.getElementById('error-nama').classList.add('hidden');
    }
    
    return valid;
}

// Validate jam: jam_selesai harus > jam_mulai
function validateJam() {
    const mulai = document.getElementById('jam_mulai').value;
    const selesai = document.getElementById('jam_selesai').value;
    if (mulai && selesai && selesai <= mulai) {
        alert('Jam selesai harus setelah jam mulai');
        return false;
    }
    return true;
}
</script>
```

### L2: Validasi Server-Side (Python Controller)

```python
# Validasi di Controller / Use Case layer
from datetime import datetime

class ValidationError(Exception):
    def __init__(self, message, errors=None):
        super().__init__(message)
        self.errors = errors or {}

def validate_kegiatan(data):
    """Validasi data kegiatan"""
    errors = {}
    
    # nama_kegiatan: required, max 200
    nama = data.get('nama_kegiatan', '').strip()
    if not nama:
        errors['nama_kegiatan'] = 'Nama kegiatan wajib diisi'
    elif len(nama) > 200:
        errors['nama_kegiatan'] = 'Nama kegiatan maksimal 200 karakter'
    
    # deskripsi: optional, max 1000
    deskripsi = data.get('deskripsi', '').strip()
    if deskripsi and len(deskripsi) > 1000:
        errors['deskripsi'] = 'Deskripsi maksimal 1000 karakter'
    
    return errors

def validate_rencana(data):
    """Validasi data rencana"""
    errors = {}
    
    # tanggal: required, format YYYY-MM-DD
    tanggal = data.get('tanggal', '').strip()
    if not tanggal:
        errors['tanggal'] = 'Tanggal wajib diisi'
    else:
        try:
            datetime.strptime(tanggal, '%Y-%m-%d')
        except ValueError:
            errors['tanggal'] = 'Format tanggal harus YYYY-MM-DD'
    
    # id_kegiatan: required, must be integer
    try:
        id_kegiatan = int(data.get('id_kegiatan', 0))
        if id_kegiatan <= 0:
            errors['id_kegiatan'] = 'Kegiatan harus dipilih'
    except (ValueError, TypeError):
        errors['id_kegiatan'] = 'Kegiatan tidak valid'
    
    # jam: optional, format HH:MM
    for field in ['jam_mulai', 'jam_selesai']:
        jam = data.get(field, '').strip()
        if jam:
            try:
                datetime.strptime(jam, '%H:%M')
            except ValueError:
                errors[field] = f'Format {field} harus HH:MM'
    
    # jam_mulai < jam_selesai
    if not errors.get('jam_mulai') and not errors.get('jam_selesai'):
        mulai = data.get('jam_mulai', '')
        selesai = data.get('jam_selesai', '')
        if mulai and selesai and selesai <= mulai:
            errors['jam_selesai'] = 'Jam selesai harus setelah jam mulai'
    
    return errors

def validate_catatan(data):
    """Validasi data catatan harian"""
    errors = {}
    
    # Reuse validasi yang sama dengan rencana
    errors.update(validate_rencana(data))
    
    # deskripsi: required
    deskripsi = data.get('deskripsi', '').strip()
    if not deskripsi:
        errors['deskripsi'] = 'Deskripsi kegiatan wajib diisi'
    elif len(deskripsi) > 2000:
        errors['deskripsi'] = 'Deskripsi maksimal 2000 karakter'
    
    return errors
```

### L3: Database Constraints (SQLite)

```sql
-- Constraints sudah didefinisikan di DDL:
-- 1. NOT NULL: nama_kegiatan, tanggal, deskripsi, id_kegiatan (FK)
-- 2. UNIQUE: nama_kegiatan
-- 3. CHECK: status di setiap tabel
-- 4. FOREIGN KEY: id_kegiatan → kegiatan(id_kegiatan)
-- 5. CASCADE DELETE/UPDATE: menjaga integritas relasi
```

### Error Handling di Controller

```python
from flask import request, render_template, redirect, flash, jsonify

class KegiatanController:
    
    def store(self):
        """Menyimpan kegiatan baru"""
        data = request.form
        
        # Validasi
        errors = validate_kegiatan(data)
        if errors:
            flash('Mohon perbaiki data yang salah', 'error')
            return render_template('kegiatan/form.html', 
                                 errors=errors, 
                                 data=data)
        
        try:
            # Panggil use case
            use_case = KelolaKegiatan(repository)
            use_case.tambah(data)
            
            flash('Kegiatan berhasil ditambahkan', 'success')
            return redirect('/kegiatan')
            
        except DuplicateError as e:
            flash(str(e), 'error')
            return render_template('kegiatan/form.html', 
                                 errors={'nama_kegiatan': str(e)}, 
                                 data=data)
        
        except Exception as e:
            flash('Terjadi kesalahan sistem', 'error')
            # Log error
            app.logger.error(f'Kesalahan menyimpan kegiatan: {str(e)}')
            return render_template('kegiatan/form.html', data=data), 500
    
    def destroy(self, id):
        """Menghapus kegiatan"""
        try:
            use_case = KelolaKegiatan(repository)
            use_case.hapus(id)
            flash('Kegiatan berhasil dihapus', 'success')
        except NotFoundError:
            flash('Kegiatan tidak ditemukan', 'error')
        except Exception as e:
            flash('Terjadi kesalahan sistem', 'error')
            app.logger.error(f'Kesalahan menghapus kegiatan: {str(e)}')
        
        return redirect('/kegiatan')
```

### API Error Handling (JSON)

```python
class ApiController:
    
    def store_kegiatan(self):
        """API: menyimpan kegiatan"""
        data = request.form
        
        errors = validate_kegiatan(data)
        if errors:
            return jsonify({
                'status': 'error',
                'message': 'Validasi gagal',
                'errors': errors
            }), 400
        
        try:
            use_case = KelolaKegiatan(repository)
            result = use_case.tambah(data)
            return jsonify({
                'status': 'success',
                'message': 'Kegiatan berhasil ditambahkan',
                'data': result.to_dict()
            }), 201
            
        except DuplicateError as e:
            return jsonify({
                'status': 'error',
                'message': str(e)
            }), 409
            
        except Exception as e:
            app.logger.error(str(e))
            return jsonify({
                'status': 'error',
                'message': 'Internal server error'
            }), 500
```

### Matriks Validasi Lengkap

| Entitas | Field | Rule Client | Rule Server | DB Constraint |
|---------|-------|-------------|-------------|---------------|
| **kegiatan** | nama_kegiatan | required, max 200 | required, max 200, unique | NOT NULL, UNIQUE |
| | deskripsi | max 1000 | max 1000 | - |
| | status | dropdown (aktif/nonaktif) | in ['aktif','nonaktif'] | CHECK |
| **perencanaan** | tanggal | required, datepicker | required, format YYYY-MM-DD | NOT NULL |
| | id_kegiatan | required, dropdown | required, integer > 0 | FK, NOT NULL |
| | jam_mulai | optional, timepicker | format HH:MM | - |
| | jam_selesai | optional, > jam_mulai | format HH:MM, > jam_mulai | - |
| | catatan | max 500 | max 500 | - |
| | status | dropdown (direncanakan/selesai/batal) | in ['direncanakan','selesai','batal'] | CHECK |
| **catatan_harian** | tanggal | required, datepicker | required, format YYYY-MM-DD | NOT NULL |
| | id_kegiatan | required, dropdown | required, integer > 0 | FK, NOT NULL |
| | jam_mulai | optional, timepicker | format HH:MM | - |
| | jam_selesai | optional, > jam_mulai | format HH:MM, > jam_mulai | - |
| | deskripsi | required, max 2000 | required, max 2000 | NOT NULL |
| | status | dropdown (selesai/proses/tertunda) | in ['selesai','proses','tertunda'] | CHECK |

### Custom Error Classes

```python
class AppError(Exception):
    """Base error untuk aplikasi"""
    pass

class NotFoundError(AppError):
    """Data tidak ditemukan"""
    pass

class DuplicateError(AppError):
    """Data duplikat"""
    pass

class ValidationError(AppError):
    """Validasi gagal"""
    def __init__(self, message, errors=None):
        super().__init__(message)
        self.errors = errors or {}
```

### HTTP Status Code Mapping

| Situasi | Kode | Response |
|---------|------|----------|
| Sukses GET | 200 | Render template / JSON data |
| Sukses Create | 201 | Redirect / JSON created |
| Validasi gagal | 400 | Tampilkan error + form / JSON errors |
| Data tidak ditemukan | 404 | Halaman 404 / JSON not found |
| Duplikat data | 409 | Error message / JSON conflict |
| Kesalahan server | 500 | Halaman error / JSON 500 |
| Method tidak diizinkan | 405 | Error message |

---

---

## Task 15: Desain Responsive Breakpoints

### Custom Breakpoints (Sesuai Permintaan Client)

| Kategori | Rentang | Target Device | CSS Tailwind Prefix |
|----------|---------|---------------|-------------------|
| **HP** | 0px - 450px | Smartphone portrait | `max-[450px]:` |
| **Tablet** | 450px - 999px | Tablet portrait/landscape, HP landscape | `min-[450px]:` sampai `max-[999px]:` |
| **PC** | 999px+ | Desktop, Laptop | `min-[999px]:` |

### Implementasi di Tailwind CSS

```html
<!-- config di tailwind atau inline di HTML -->
<style>
    /* Tidak perlu konfigurasi khusus Tailwind */
    /* Cukup gunakan media query langsung atau utility classes */
    
    /* HP: 0 - 450px (mobile-first: default styling untuk HP) */
    /* Semua style default adalah untuk HP */
    
    /* Tablet: 451px - 999px */
    @media (min-width: 451px) and (max-width: 999px) {
        /* Style spesifik tablet */
    }
    
    /* PC: 1000px+ */
    @media (min-width: 1000px) {
        /* Style spesifik PC */
    }
</style>
```

### Strategi Responsive per Komponen

#### 1. Navbar (Navigasi)

| Device | Tampilan |
|--------|----------|
| **HP** (0-450px) | Hamburger menu collapsed. Logo + hamburger icon saja |
| **Tablet** (450-999px) | Menu horizontal dengan teks yang lebih kecil. Mungkin dropdown |
| **PC** (999px+) | Full horizontal menu dengan semua link |

```html
<!-- Implementasi Navbar Responsive -->
<nav>
    <!-- PC: Menu penuh -->
    <div class="hidden min-[999px]:flex items-center space-x-4">
        <a href="/">Dashboard</a>
        <a href="/kegiatan">Kegiatan</a>
        <a href="/rencana">Rencana</a>
        <a href="/catatan">Catatan</a>
    </div>
    
    <!-- Tablet: Menu horizontal kompak -->
    <div class="hidden min-[451px]:flex max-[998px]:flex items-center space-x-2 
                max-[450px]:hidden">
        <a href="/" class="text-sm px-2">📊</a>
        <a href="/kegiatan" class="text-sm px-2">📋</a>
        <a href="/rencana" class="text-sm px-2">📅</a>
        <a href="/catatan" class="text-sm px-2">📝</a>
    </div>
    
    <!-- HP: Hamburger -->
    <div class="flex min-[450px]:hidden">
        <button id="menu-toggle">☰</button>
    </div>
</nav>
```

#### 2. Tabel Daftar vs Card

| Device | Tampilan |
|--------|----------|
| **HP** (0-450px) | **Card view** - setiap item ditampilkan dalam card vertikal |
| **Tablet** (450-999px) | **Card view** - grid 2 kolom atau tabel kompak dengan scroll horizontal |
| **PC** (999px+) | **Tabel penuh** - semua kolom terlihat jelas |

```html
<!-- PC: Tabel (999px+) -->
<div class="hidden min-[999px]:block bg-white rounded-lg shadow overflow-x-auto">
    <table class="w-full">...</table>
</div>

<!-- Tablet: Card Grid atau Tabel Compact (450-999px) -->
<div class="hidden max-[998px]:block min-[451px]:hidden bg-white rounded-lg shadow overflow-x-auto">
    <!-- Tabel dengan font lebih kecil -->
    <table class="w-full text-sm">...</table>
</div>

<!-- HP: Card View (0-450px) -->
<div class="block max-[450px]:block space-y-4">
    {% for item in data %}
    <div class="bg-white rounded-lg shadow p-4">
        <h3 class="font-semibold">{{ item.nama_kegiatan }}</h3>
        <p class="text-sm text-gray-500">{{ item.deskripsi }}</p>
        <div class="flex justify-between mt-2">
            <span class="text-xs badge">{{ item.status }}</span>
            <div class="space-x-2">
                <a href="/kegiatan/{{ item.id_kegiatan }}/edit" class="text-blue-600 text-sm">Edit</a>
                <button class="text-red-600 text-sm">Hapus</button>
            </div>
        </div>
    </div>
    {% endfor %}
</div>
```

#### 3. Form Input

| Device | Tampilan |
|--------|----------|
| **HP** (0-450px) | Full width input, satu kolom vertikal, tombol full width |
| **Tablet** (450-999px) | Input 50%-75% width, dua kolom untuk field pendek (jam) |
| **PC** (999px+) | Max-width 600px centered. Dua kolom untuk field pendek |

```html
<!-- Form Responsive -->
<form class="mx-auto min-[999px]:max-w-2xl">
    <!-- Nama: Full width semua device -->
    <div class="mb-4">
        <label class="block text-sm font-medium mb-1">Nama Kegiatan</label>
        <input type="text" 
               class="w-full px-4 py-2 border rounded-lg 
                      focus:outline-none focus:ring-2 focus:ring-blue-500">
    </div>
    
    <!-- Jam: Dua kolom di tablet ke atas, satu kolom di HP -->
    <div class="flex flex-col min-[450px]:flex-row gap-4 mb-4">
        <div class="flex-1">
            <label class="block text-sm font-medium mb-1">Jam Mulai</label>
            <input type="time" 
                   class="w-full px-4 py-2 border rounded-lg
                          focus:outline-none focus:ring-2 focus:ring-blue-500">
        </div>
        <div class="flex-1">
            <label class="block text-sm font-medium mb-1">Jam Selesai</label>
            <input type="time" 
                   class="w-full px-4 py-2 border rounded-lg
                          focus:outline-none focus:ring-2 focus:ring-blue-500">
        </div>
    </div>
    
    <!-- Tombol: Full width di HP, inline di tablet/PC -->
    <div class="flex flex-col min-[450px]:flex-row gap-2">
        <button type="submit" 
                class="bg-blue-600 text-white px-6 py-2 rounded-lg 
                       hover:bg-blue-700 w-full min-[450px]:w-auto">
            💾 Simpan
        </button>
        <a href="/kegiatan" 
           class="bg-gray-300 text-gray-700 px-6 py-2 rounded-lg 
                  hover:bg-gray-400 text-center w-full min-[450px]:w-auto">
            ✖ Batal
        </a>
    </div>
</form>
```

#### 4. Filter Tanggal

| Device | Tampilan |
|--------|----------|
| **HP** (0-450px) | Vertical stack: label + input full width + tombol full width |
| **Tablet** (450-999px) | Inline flex: input + input + tombol |
| **PC** (999px+) | Inline flex dengan label di atas input |

```html
<!-- Filter Tanggal Responsive -->
<div class="bg-white p-4 rounded-lg shadow mb-6">
    <div class="flex flex-col min-[450px]:flex-row gap-2 items-end">
        <div class="w-full min-[450px]:w-auto">
            <label class="block text-xs font-medium mb-1">Dari Tanggal</label>
            <input type="date" 
                   class="w-full min-[450px]:w-40 px-3 py-2 border rounded-lg text-sm
                          focus:outline-none focus:ring-2 focus:ring-blue-500">
        </div>
        <div class="w-full min-[450px]:w-auto">
            <label class="block text-xs font-medium mb-1">Sampai Tanggal</label>
            <input type="date" 
                   class="w-full min-[450px]:w-40 px-3 py-2 border rounded-lg text-sm
                          focus:outline-none focus:ring-2 focus:ring-blue-500">
        </div>
        <button class="bg-blue-600 text-white px-4 py-2 rounded-lg text-sm
                       hover:bg-blue-700 w-full min-[450px]:w-auto">
            🔍 Filter
        </button>
    </div>
</div>
```

#### 5. Dashboard Card

| Device | Tampilan |
|--------|----------|
| **HP** (0-450px) | 1 card per baris (full width) |
| **Tablet** (450-999px) | 2 card per baris (grid 2 kolom) |
| **PC** (999px+) | 3-4 card per baris (grid 3-4 kolom) |

```html
<!-- Dashboard Cards Responsive -->
<div class="grid grid-cols-1 min-[450px]:grid-cols-2 min-[999px]:grid-cols-4 gap-4 mb-8">
    <!-- Card 1: Total Kegiatan -->
    <div class="bg-white rounded-lg shadow p-6">
        <div class="flex items-center justify-between">
            <div>
                <p class="text-gray-500 text-sm">Total Kegiatan</p>
                <p class="text-2xl font-bold">12</p>
            </div>
            <span class="text-3xl">📋</span>
        </div>
    </div>
    
    <!-- Card 2: Rencana Hari Ini -->
    <div class="bg-white rounded-lg shadow p-6">
        <div class="flex items-center justify-between">
            <div>
                <p class="text-gray-500 text-sm">Rencana Hari Ini</p>
                <p class="text-2xl font-bold">4</p>
            </div>
            <span class="text-3xl">📅</span>
        </div>
    </div>
    
    <!-- Card 3: Catatan Hari Ini -->
    <div class="bg-white rounded-lg shadow p-6">
        <div class="flex items-center justify-between">
            <div>
                <p class="text-gray-500 text-sm">Catatan Hari Ini</p>
                <p class="text-2xl font-bold">3</p>
            </div>
            <span class="text-3xl">📝</span>
        </div>
    </div>
    
    <!-- Card 4: Kegiatan Aktif -->
    <div class="bg-white rounded-lg shadow p-6">
        <div class="flex items-center justify-between">
            <div>
                <p class="text-gray-500 text-sm">Kegiatan Aktif</p>
                <p class="text-2xl font-bold">10</p>
            </div>
            <span class="text-3xl">✅</span>
        </div>
    </div>
</div>
```

#### 6. Modal Konfirmasi

| Device | Tampilan |
|--------|----------|
| **HP** (0-450px) | Full screen modal (padding minimal). Tombol stack vertikal |
| **Tablet** (450-999px) | Centered modal dengan padding sedang. Tombol inline |
| **PC** (999px+) | Small centered modal. Tombol inline dengan hover effect |

```html
<!-- Modal Hapus Responsive -->
<div id="modal-hapus" class="fixed inset-0 bg-black bg-opacity-50 hidden 
                            flex items-center justify-center z-50">
    <div class="bg-white rounded-lg shadow-xl mx-4 
                w-full min-[450px]:max-w-md min-[999px]:max-w-sm
                p-6">
        <h3 class="text-lg font-bold mb-4">⚠️ Konfirmasi Hapus</h3>
        <p class="text-gray-600 mb-6">
            Apakah Anda yakin ingin menghapus 
            <span id="nama-item" class="font-semibold">item ini</span>?
        </p>
        <div class="flex flex-col min-[450px]:flex-row gap-2 justify-end">
            <button id="btn-batal" 
                    class="bg-gray-300 text-gray-700 px-4 py-2 rounded-lg 
                           order-2 min-[450px]:order-1">
                ✖ Batal
            </button>
            <button id="btn-hapus" 
                    class="bg-red-600 text-white px-4 py-2 rounded-lg 
                           order-1 min-[450px]:order-2">
                🗑 Ya, Hapus
            </button>
        </div>
    </div>
</div>
```

### Tabel Ringkasan Responsive Layout

| Komponen | HP (0-450px) | Tablet (450-999px) | PC (999px+) |
|----------|-------------|-------------------|-------------|
| **Navbar** | Hamburger | Ikon-only | Full text menu |
| **Daftar** | Card vertikal | Tabel compact / Card grid 2 kolom | Tabel penuh |
| **Form** | Satu kolom full width | Dua kolom sebagian | Max-width 600px centered |
| **Filter** | Stack vertikal | Inline | Inline |
| **Dashboard** | 1 kolom | 2 kolom | 4 kolom |
| **Modal** | Full screen padded | Centered 400px | Centered 384px |
| **Tombol** | Full width | Inline / auto width | Inline / auto width |
| **Grid** | grid-cols-1 | grid-cols-2 | grid-cols-3/4 |
| **Padding** | px-4 | px-6 | px-8 |
| **Font size** | text-sm | text-base | text-base/lg |

### Media Query Summary (CSS)

```css
/* Tidak perlu menulis CSS manual jika menggunakan Tailwind utility classes */
/* Tapi jika perlu custom: */

/* HP: 0 - 450px */
/* (default - tidak perlu media query) */

/* Tablet: 451px - 999px */
@media (min-width: 451px) and (max-width: 999px) {
    .tablet\:grid-2 { grid-template-columns: repeat(2, 1fr); }
    .tablet\:hidden { display: none; }
    .tablet\:block { display: block; }
}

/* PC: 1000px+ */
@media (min-width: 1000px) {
    .desktop\:grid-4 { grid-template-columns: repeat(4, 1fr); }
    .desktop\:hidden { display: none; }
    .desktop\:block { display: block; }
}
```

### Prinsip Mobile-First yang Digunakan

1. **Default = HP**: Semua styling default digunakan untuk HP (0-450px)
2. **Min-width untuk upgrade**: `min-[451px]:` untuk tablet, `min-[999px]:` untuk PC
3. **Max-width untuk override**: `max-[450px]:` jika perlu override spesifik HP
4. **Grid responsive**: `grid-cols-1 min-[450px]:grid-cols-2 min-[999px]:grid-cols-4`
5. **Flex direction**: `flex-col min-[450px]:flex-row` (vertikal di HP, horizontal di atasnya)

---

---

## Task 16: Desain Filter & Pencarian

### Kebutuhan Filter

| Fitur Filter | Halaman | Tipe Filter | Deskripsi |
|-------------|---------|-------------|-----------|
| Filter Tanggal | Daftar Rencana | Rentang tanggal | Menampilkan rencana dalam range tanggal tertentu |
| Filter Tanggal | Daftar Catatan | Rentang tanggal | Menampilkan catatan dalam range tanggal tertentu |
| Search Nama | Daftar Kegiatan | Text search | Mencari kegiatan berdasarkan nama |
| Filter Status | Daftar Kegiatan | Dropdown | Filter berdasarkan status aktif/nonaktif |
| Filter Status | Daftar Rencana | Dropdown | Filter berdasarkan status rencana |
| Filter Status | Daftar Catatan | Dropdown | Filter berdasarkan status catatan |
| Filter Kegiatan | Daftar Rencana/Catatan | Dropdown | Filter berdasarkan jenis kegiatan |

### Desain Filter per Halaman

#### 1. Halaman Daftar Rencana - Filter Panel

```html
<!-- Filter Panel untuk Rencana -->
<div class="bg-white p-4 rounded-lg shadow mb-6">
    <!-- Header Filter (collapsible di mobile) -->
    <div class="flex justify-between items-center mb-4">
        <h3 class="font-semibold text-gray-700 flex items-center gap-2">
            🔍 Filter Rencana
        </h3>
        <button id="toggle-filter" 
                class="min-[450px]:hidden text-blue-600 text-sm hover:underline">
            Tampilkan/Sembunyikan
        </button>
    </div>
    
    <div id="filter-content" class="min-[450px]:block">
        <div class="grid grid-cols-1 min-[450px]:grid-cols-2 min-[999px]:grid-cols-4 gap-4">
            <!-- Filter 1: Tanggal Mulai -->
            <div>
                <label class="block text-xs font-medium text-gray-600 mb-1">Dari Tanggal</label>
                <input type="date" name="tgl_mulai" value="{{ tgl_mulai }}"
                       class="w-full px-3 py-2 border rounded-lg text-sm
                              focus:outline-none focus:ring-2 focus:ring-blue-500">
            </div>
            
            <!-- Filter 2: Tanggal Selesai -->
            <div>
                <label class="block text-xs font-medium text-gray-600 mb-1">Sampai Tanggal</label>
                <input type="date" name="tgl_selesai" value="{{ tgl_selesai }}"
                       class="w-full px-3 py-2 border rounded-lg text-sm
                              focus:outline-none focus:ring-2 focus:ring-blue-500">
            </div>
            
            <!-- Filter 3: Status -->
            <div>
                <label class="block text-xs font-medium text-gray-600 mb-1">Status</label>
                <select name="status" 
                        class="w-full px-3 py-2 border rounded-lg text-sm
                               focus:outline-none focus:ring-2 focus:ring-blue-500">
                    <option value="">Semua Status</option>
                    <option value="direncanakan" {% if status == 'direncanakan' %}selected{% endif %}>Direncanakan</option>
                    <option value="selesai" {% if status == 'selesai' %}selected{% endif %}>Selesai</option>
                    <option value="batal" {% if status == 'batal' %}selected{% endif %}>Batal</option>
                </select>
            </div>
            
            <!-- Filter 4: Pilih Kegiatan -->
            <div>
                <label class="block text-xs font-medium text-gray-600 mb-1">Kegiatan</label>
                <select name="id_kegiatan" 
                        class="w-full px-3 py-2 border rounded-lg text-sm
                               focus:outline-none focus:ring-2 focus:ring-blue-500">
                    <option value="">Semua Kegiatan</option>
                    {% for k in kegiatan %}
                    <option value="{{ k.id_kegiatan }}" 
                            {% if id_kegiatan == k.id_kegiatan %}selected{% endif %}>
                        {{ k.nama_kegiatan }}
                    </option>
                    {% endfor %}
                </select>
            </div>
        </div>
        
        <!-- Tombol Aksi Filter -->
        <div class="flex flex-col min-[450px]:flex-row gap-2 mt-4">
            <button type="submit" 
                    class="bg-blue-600 text-white px-4 py-2 rounded-lg text-sm
                           hover:bg-blue-700 w-full min-[450px]:w-auto">
                🔍 Terapkan Filter
            </button>
            <a href="/rencana" 
               class="bg-gray-200 text-gray-700 px-4 py-2 rounded-lg text-sm
                      hover:bg-gray-300 text-center w-full min-[450px]:w-auto">
                ✖ Reset Filter
            </a>
        </div>
    </div>
</div>

<script>
// Toggle filter di mobile
document.getElementById('toggle-filter')?.addEventListener('click', function() {
    const content = document.getElementById('filter-content');
    content.classList.toggle('hidden');
    this.textContent = content.classList.contains('hidden') ? 'Tampilkan Filter' : 'Sembunyikan Filter';
});
</script>
```

#### 2. Halaman Daftar Catatan - Filter Panel

```html
<!-- Filter Panel untuk Catatan Harian -->
<div class="bg-white p-4 rounded-lg shadow mb-6">
    <div class="grid grid-cols-1 min-[450px]:grid-cols-2 min-[999px]:grid-cols-4 gap-4">
        <!-- Tanggal -->
        <div>
            <label class="block text-xs font-medium text-gray-600 mb-1">Dari Tanggal</label>
            <input type="date" name="tgl_mulai" value="{{ tgl_mulai }}"
                   class="w-full px-3 py-2 border rounded-lg text-sm">
        </div>
        <div>
            <label class="block text-xs font-medium text-gray-600 mb-1">Sampai Tanggal</label>
            <input type="date" name="tgl_selesai" value="{{ tgl_selesai }}"
                   class="w-full px-3 py-2 border rounded-lg text-sm">
        </div>
        
        <!-- Status -->
        <div>
            <label class="block text-xs font-medium text-gray-600 mb-1">Status</label>
            <select name="status" class="w-full px-3 py-2 border rounded-lg text-sm">
                <option value="">Semua Status</option>
                <option value="selesai">Selesai</option>
                <option value="proses">Proses</option>
                <option value="tertunda">Tertunda</option>
            </select>
        </div>
        
        <!-- Kegiatan -->
        <div>
            <label class="block text-xs font-medium text-gray-600 mb-1">Kegiatan</label>
            <select name="id_kegiatan" class="w-full px-3 py-2 border rounded-lg text-sm">
                <option value="">Semua Kegiatan</option>
                {% for k in kegiatan %}
                <option value="{{ k.id_kegiatan }}">{{ k.nama_kegiatan }}</option>
                {% endfor %}
            </select>
        </div>
    </div>
    
    <div class="flex flex-col min-[450px]:flex-row gap-2 mt-4">
        <button type="submit" 
                class="bg-blue-600 text-white px-4 py-2 rounded-lg text-sm
                       hover:bg-blue-700 w-full min-[450px]:w-auto">
            🔍 Terapkan Filter
        </button>
        <a href="/catatan" 
           class="bg-gray-200 text-gray-700 px-4 py-2 rounded-lg text-sm
                  hover:bg-gray-300 text-center w-full min-[450px]:w-auto">
            ✖ Reset
        </a>
    </div>
</div>
```

#### 3. Halaman Daftar Kegiatan - Search

```html
<!-- Search + Filter Kegiatan -->
<div class="flex flex-col min-[450px]:flex-row gap-4 mb-6">
    <!-- Search Box -->
    <div class="flex-1">
        <input type="text" id="search-kegiatan" name="search" 
               value="{{ search }}"
               placeholder="🔍 Cari nama kegiatan..." 
               class="w-full px-4 py-2 border rounded-lg 
                      focus:outline-none focus:ring-2 focus:ring-blue-500">
    </div>
    
    <!-- Filter Status -->
    <select name="status" 
            class="w-full min-[450px]:w-40 px-4 py-2 border rounded-lg
                   focus:outline-none focus:ring-2 focus:ring-blue-500">
        <option value="">Semua Status</option>
        <option value="aktif" {% if status == 'aktif' %}selected{% endif %}>✅ Aktif</option>
        <option value="nonaktif" {% if status == 'nonaktif' %}selected{% endif %}>❌ Nonaktif</option>
    </select>
    
    <button type="submit" 
            class="bg-blue-600 text-white px-6 py-2 rounded-lg
                   hover:bg-blue-700 w-full min-[450px]:w-auto">
        Cari
    </button>
</div>

<script>
// Live search with debounce
let debounceTimer;
document.getElementById('search-kegiatan')?.addEventListener('keyup', function() {
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(() => {
        // Kirim request dengan parameter search
        window.location.href = '/kegiatan?search=' + encodeURIComponent(this.value);
    }, 500); // Delay 500ms
});
</script>
```

### Query Filter di Backend (Python)

```python
class FilterService:
    """Service untuk menangani filter dan pencarian"""
    
    def filter_rencana(self, params):
        """Filter data rencana"""
        query = """
            SELECT r.*, k.nama_kegiatan 
            FROM perencanaan r
            JOIN kegiatan k ON r.id_kegiatan = k.id_kegiatan
            WHERE 1=1
        """
        filters = []
        
        # Filter tanggal
        if params.get('tgl_mulai'):
            query += " AND r.tanggal >= ?"
            filters.append(params['tgl_mulai'])
        if params.get('tgl_selesai'):
            query += " AND r.tanggal <= ?"
            filters.append(params['tgl_selesai'])
        
        # Filter status
        if params.get('status'):
            query += " AND r.status = ?"
            filters.append(params['status'])
        
        # Filter kegiatan
        if params.get('id_kegiatan'):
            query += " AND r.id_kegiatan = ?"
            filters.append(params['id_kegiatan'])
        
        # Order by
        query += " ORDER BY r.tanggal DESC, r.jam_mulai ASC"
        
        return self.db.execute(query, filters).fetchall()
    
    def filter_catatan(self, params):
        """Filter data catatan"""
        query = """
            SELECT c.*, k.nama_kegiatan 
            FROM catatan_harian c
            JOIN kegiatan k ON c.id_kegiatan = k.id_kegiatan
            WHERE 1=1
        """
        filters = []
        
        if params.get('tgl_mulai'):
            query += " AND c.tanggal >= ?"
            filters.append(params['tgl_mulai'])
        if params.get('tgl_selesai'):
            query += " AND c.tanggal <= ?"
            filters.append(params['tgl_selesai'])
        if params.get('status'):
            query += " AND c.status = ?"
            filters.append(params['status'])
        if params.get('id_kegiatan'):
            query += " AND c.id_kegiatan = ?"
            filters.append(params['id_kegiatan'])
        
        query += " ORDER BY c.tanggal DESC, c.jam_mulai ASC"
        return self.db.execute(query, filters).fetchall()
    
    def search_kegiatan(self, keyword, status=None):
        """Cari kegiatan berdasarkan nama"""
        query = """
            SELECT * FROM kegiatan 
            WHERE nama_kegiatan LIKE ?
        """
        filters = [f'%{keyword}%']
        
        if status:
            query += " AND status = ?"
            filters.append(status)
        
        query += " ORDER BY nama_kegiatan ASC"
        return self.db.execute(query, filters).fetchall()
```

### Implementasi di Controller

```python
class RencanaController:
    
    def index(self):
        """Menampilkan daftar rencana dengan filter"""
        params = {
            'tgl_mulai': request.args.get('tgl_mulai'),
            'tgl_selesai': request.args.get('tgl_selesai'),
            'status': request.args.get('status'),
            'id_kegiatan': request.args.get('id_kegiatan', type=int),
        }
        
        filter_service = FilterService(db)
        data_rencana = filter_service.filter_rencana(params)
        
        # Ambil data kegiatan untuk dropdown filter
        kegiatan_repo = SqliteKegiatanRepository(db)
        daftar_kegiatan = kegiatan_repo.ambil_semua(status='aktif')
        
        return render_template('rencana/daftar.html',
                             data=data_rencana,
                             kegiatan=daftar_kegiatan,
                             **params)
    
    def index_api(self):
        """API: menampilkan daftar rencana dengan filter"""
        params = {
            'tgl_mulai': request.args.get('tgl_mulai'),
            'tgl_selesai': request.args.get('tgl_selesai'),
            'status': request.args.get('status'),
            'id_kegiatan': request.args.get('id_kegiatan', type=int),
        }
        
        filter_service = FilterService(db)
        data = filter_service.filter_rencana(params)
        
        return jsonify({
            'status': 'success',
            'data': data,
            'total': len(data),
            'filter': params
        })
```

### URL Query String Format

```python
# Format URL dengan parameter filter

# Filter rencana:
# /rencana?tgl_mulai=2026-05-01&tgl_selesai=2026-05-09&status=direncanakan&id_kegiatan=1

# Filter catatan:
# /catatan?tgl_mulai=2026-05-01&tgl_selesai=2026-05-09&status=selesai

# Search kegiatan:
# /kegiatan?search=Meeting&status=aktif

# API filter:
# /api/rencana?tanggal=2026-05-09
# /api/catatan?tgl_mulai=2026-05-01&tgl_selesai=2026-05-09
```

### Ringkasan Filter

| Halaman | Parameter | Tipe | Default | Contoh |
|---------|-----------|------|---------|--------|
| **Rencana** | `tgl_mulai` | date | kosong | `2026-05-01` |
| | `tgl_selesai` | date | kosong | `2026-05-09` |
| | `status` | string | kosong | `direncanakan` |
| | `id_kegiatan` | int | kosong | `1` |
| **Catatan** | `tgl_mulai` | date | kosong | `2026-05-01` |
| | `tgl_selesai` | date | kosong | `2026-05-09` |
| | `status` | string | kosong | `selesai` |
| | `id_kegiatan` | int | kosong | `1` |
| **Kegiatan** | `search` | string | kosong | `Meeting` |
| | `status` | string | kosong | `aktif` |

### Prinsip Filter

1. **Filter bersifat additive**: Semua parameter yang diberikan akan digabung dengan AND
2. **Parameter kosong diabaikan**: Jika parameter tidak diisi, filter tidak diterapkan untuk field itu
3. **Default tanpa filter**: Menampilkan semua data (diurutkan descending by tanggal)
4. **Reset filter**: Klik tombol Reset akan menghapus semua parameter filter
5. **URL dapat di-bookmark**: Semua filter ada di URL query string

---

---

## Task 17: Ringkasan & Finalisasi Dokumen Analisa

### Ringkasan Sistem

Sistem **Catatan Harian Kerja** adalah aplikasi berbasis web yang memungkinkan pengguna untuk:

1. **Mengelola master data kegiatan** - CRUD daftar kegiatan yang bisa dilakukan
2. **Membuat perencanaan harian** - Merencanakan kegiatan yang akan dilakukan pada hari tertentu
3. **Mencatat kegiatan harian** - Mencatat apa yang sudah dilakukan hari ini
4. **Melihat daftar** - Melihat daftar kegiatan, rencana, dan catatan
5. **Filter by tanggal** - Menyaring data berdasarkan rentang tanggal

### Spesifikasi Teknis

| Aspek | Spesifikasi |
|-------|-------------|
| **Backend** | Python (Flask) |
| **Database** | SQLite 3 |
| **Frontend** | HTML + Tailwind CSS |
| **Template Engine** | Jinja2 |
| **Arsitektur** | Clean Architecture (4 layer) |
| **Komunikasi** | HTTP GET/POST + REST API JSON |
| **Responsive** | HP (0-450px), Tablet (450-999px), PC (999px+) |

### Struktur Database

| Tabel | Primary Key | Foreign Key | Jumlah Field |
|-------|-------------|-------------|--------------|
| `kegiatan` | id_kegiatan | - | 6 |
| `perencanaan` | id_rencana | id_kegiatan → kegiatan | 9 |
| `catatan_harian` | id_catatan | id_kegiatan → kegiatan | 9 |

### Jumlah Komponen

| Komponen | Jumlah |
|----------|--------|
| **Halaman HTML** | 8 halaman (base, dashboard, 3 daftar, 3 form) |
| **API Endpoint** | 16 endpoint |
| **Route URL** | 27 route (19 HTML + 8 API) |
| **Use Case** | 7 use case |
| **Form** | 5 form |
| **Template** | 8 template HTML |
| **Tabel Database** | 3 tabel |
| **Index Database** | 5 index |
| **Trigger Database** | 3 trigger |

### Matriks Kebutuhan vs Realisasi

| No | Kebutuhan Client | Realisasi | Task Terkait |
|----|-----------------|-----------|--------------|
| 1 | Aplikasi catatan harian | ✅ Dirancang dengan Clean Architecture | Task 2, Task 17 |
| 2 | Master data kegiatan | ✅ Ada tabel `kegiatan` dengan CRUD | Task 3, Task 8, Task 9 |
| 3 | Perencanaan harian | ✅ Ada tabel `perencanaan` dengan CRUD | Task 3, Task 8, Task 9 |
| 4 | Catat kegiatan hari ini | ✅ Ada tabel `catatan_harian` dengan CRUD | Task 3, Task 8, Task 9 |
| 5 | Filter by tanggal | ✅ Ada fitur filter di setiap halaman daftar | Task 16 |
| 6 | HTML + Tailwind CSS | ✅ Template HTML dengan Tailwind CSS | Task 12, Task 15 |
| 7 | Responsive HP/Tablet/PC | ✅ 3 breakpoints sesuai custom client | Task 15 |
| 8 | Python backend | ✅ Struktur proyek Python dengan Flask | Task 10 |
| 9 | SQLite database | ✅ DDL script SQLite dengan constraints | Task 7 |
| 10 | API HTTP GET/POST | ✅ REST API endpoint JSON | Task 9 |

### Arsitektur Clean Architecture Layers

```
┌──────────────────────────────────────────────────────────────┐
│                    INTERFACE LAYER                             │
│  ┌──────────────────────────────────────────────────────────┐│
│  │ controllers/ (3 file) + templates/ (8 file)              ││
│  │ Tugas: HTTP handling, render HTML, validasi input        ││
│  └──────────────────────────────────────────────────────────┘│
├──────────────────────────────────────────────────────────────┤
│                    APPLICATION LAYER                           │
│  ┌──────────────────────────────────────────────────────────┐│
│  │ use_cases/ (4 file) + dto/ (3 file)                      ││
│  │ Tugas: Logika bisnis, orchestrasi repository              ││
│  └──────────────────────────────────────────────────────────┘│
├──────────────────────────────────────────────────────────────┤
│                    DOMAIN LAYER                                │
│  ┌──────────────────────────────────────────────────────────┐│
│  │ entities/ (3 file) + repositories/ (3 interface)          ││
│  │ Tugas: Business objects, contract repository              ││
│  └──────────────────────────────────────────────────────────┘│
├──────────────────────────────────────────────────────────────┤
│                    INFRASTRUCTURE LAYER                        │
│  ┌──────────────────────────────────────────────────────────┐│
│  │ database/ (2 file) + repositories/ (3 implementasi)       ││
│  │ Tugas: Koneksi SQLite, query SQL, implementasi repository ││
│  └──────────────────────────────────────────────────────────┘│
└──────────────────────────────────────────────────────────────┘
```

### Daftar File yang Akan Dibuat (Implementasi)

| No | File | Layer | Deskripsi |
|----|------|-------|-----------|
| 1 | `app.py` | Root | Entry point aplikasi Flask |
| 2 | `requirements.txt` | Root | Dependencies: flask, etc |
| 3 | `src/domain/entities/kegiatan.py` | Domain | Entity Kegiatan |
| 4 | `src/domain/entities/perencanaan.py` | Domain | Entity Perencanaan |
| 5 | `src/domain/entities/catatan_harian.py` | Domain | Entity CatatanHarian |
| 6 | `src/domain/repositories/kegiatan_repo.py` | Domain | Interface KegiatanRepository |
| 7 | `src/domain/repositories/perencanaan_repo.py` | Domain | Interface PerencanaanRepository |
| 8 | `src/domain/repositories/catatan_repo.py` | Domain | Interface CatatanRepository |
| 9 | `src/application/use_cases/kelola_kegiatan.py` | Application | Use case kelola kegiatan |
| 10 | `src/application/use_cases/buat_rencana.py` | Application | Use case buat rencana |
| 11 | `src/application/use_cases/catat_harian.py` | Application | Use case catat harian |
| 12 | `src/application/use_cases/lihat_daftar.py` | Application | Use case lihat daftar |
| 13 | `src/infrastructure/database/db_connection.py` | Infrastructure | Koneksi SQLite |
| 14 | `src/infrastructure/database/schema.sql` | Infrastructure | DDL script |
| 15 | `src/infrastructure/repositories/sqlite_kegiatan_repo.py` | Infrastructure | Implementasi repo kegiatan |
| 16 | `src/infrastructure/repositories/sqlite_perencanaan_repo.py` | Infrastructure | Implementasi repo rencana |
| 17 | `src/infrastructure/repositories/sqlite_catatan_repo.py` | Infrastructure | Implementasi repo catatan |
| 18 | `src/interface/controllers/kegiatan_controller.py` | Interface | Controller kegiatan |
| 19 | `src/interface/controllers/rencana_controller.py` | Interface | Controller rencana |
| 20 | `src/interface/controllers/catatan_controller.py` | Interface | Controller catatan |
| 21 | `src/interface/templates/base.html` | Interface | Layout utama |
| 22-28 | `src/interface/templates/*/*.html` | Interface | 8 template HTML |

**Total file: ~28 file Python + HTML**

### Kesimpulan

Dokumen analisa ini telah mencakup seluruh aspek yang diminta oleh client:

1. ✅ **Desain rencana sistem** - Clean Architecture, Use Case, DFD
2. ✅ **ERD Database** - 3 tabel dengan relasi, constraints, index
3. ✅ **Use Case & DFD** - 7 use case, DFD Level 0 dan Level 1
4. ✅ **Struktur sistem** - Clean Architecture 4 layer dengan dependency rule
5. ✅ **Form-form** - 5 desain form dengan validasi lengkap
6. ✅ **API** - 16 REST API endpoint dengan format JSON standar
7. ✅ **Responsive** - 3 breakpoints custom (HP, Tablet, PC)
8. ✅ **Filter** - Filter tanggal, status, kegiatan, dan search

Dokumen ini siap digunakan sebagai **blueprint** untuk tahap implementasi (coding).

---

**📌 END OF DOCUMENT - Analisa Sistem Catatan Harian Kerja**
