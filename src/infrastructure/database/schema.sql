-- Enable foreign key constraints
PRAGMA foreign_keys = ON;

-- Tabel 1: kegiatan (Master Data Kegiatan)
CREATE TABLE IF NOT EXISTS kegiatan (
    id_kegiatan    INTEGER PRIMARY KEY AUTOINCREMENT,
    nama_kegiatan  VARCHAR(200) NOT NULL,
    deskripsi      TEXT DEFAULT NULL,
    status         VARCHAR(20) NOT NULL DEFAULT 'aktif'
                   CHECK (status IN ('aktif', 'nonaktif')),
    created_at     DATETIME NOT NULL DEFAULT (datetime('now','localtime')),
    updated_at     DATETIME NOT NULL DEFAULT (datetime('now','localtime'))
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_kegiatan_nama ON kegiatan(nama_kegiatan);

-- Tabel 2: perencanaan (Rencana Harian)
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
    
    CONSTRAINT fk_perencanaan_kegiatan
        FOREIGN KEY (id_kegiatan)
        REFERENCES kegiatan(id_kegiatan)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_perencanaan_tanggal ON perencanaan(tanggal);
CREATE INDEX IF NOT EXISTS idx_perencanaan_kegiatan ON perencanaan(id_kegiatan);

-- Tabel 3: catatan_harian (Log Kegiatan Harian)
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
    
    CONSTRAINT fk_catatan_kegiatan
        FOREIGN KEY (id_kegiatan)
        REFERENCES kegiatan(id_kegiatan)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_catatan_tanggal ON catatan_harian(tanggal);
CREATE INDEX IF NOT EXISTS idx_catatan_kegiatan ON catatan_harian(id_kegiatan);

-- Triggers for updated_at
CREATE TRIGGER IF NOT EXISTS trg_kegiatan_updated AFTER UPDATE ON kegiatan
BEGIN
    UPDATE kegiatan SET updated_at = datetime('now','localtime') WHERE id_kegiatan = OLD.id_kegiatan;
END;

CREATE TRIGGER IF NOT EXISTS trg_perencanaan_updated AFTER UPDATE ON perencanaan
BEGIN
    UPDATE perencanaan SET updated_at = datetime('now','localtime') WHERE id_rencana = OLD.id_rencana;
END;

CREATE TRIGGER IF NOT EXISTS trg_catatan_updated AFTER UPDATE ON catatan_harian
BEGIN
    UPDATE catatan_harian SET updated_at = datetime('now','localtime') WHERE id_catatan = OLD.id_catatan;
END;
