from typing import List, Optional
from src.domain.entities.kegiatan import Kegiatan
from src.domain.repositories.kegiatan_repo import KegiatanRepository
from datetime import datetime

class SqliteKegiatanRepository(KegiatanRepository):
    def __init__(self, db_conn):
        self.db_conn = db_conn

    def ambil_semua(self, search: str = None, status: str = None) -> List[Kegiatan]:
        query = "SELECT * FROM kegiatan WHERE 1=1"
        params = []
        if search:
            query += " AND nama_kegiatan LIKE ?"
            params.append(f"%{search}%")
        if status:
            query += " AND status = ?"
            params.append(status)
        query += " ORDER BY created_at DESC"
        
        conn = self.db_conn.get_connection()
        cursor = conn.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        
        return [self._row_to_entity(row) for row in rows]

    def ambil_by_id(self, id_kegiatan: int) -> Optional[Kegiatan]:
        conn = self.db_conn.get_connection()
        cursor = conn.execute("SELECT * FROM kegiatan WHERE id_kegiatan = ?", (id_kegiatan,))
        row = cursor.fetchone()
        conn.close()
        return self._row_to_entity(row) if row else None

    def simpan(self, kegiatan: Kegiatan) -> Kegiatan:
        conn = self.db_conn.get_connection()
        cursor = conn.execute(
            "INSERT INTO kegiatan (nama_kegiatan, deskripsi, status) VALUES (?, ?, ?)",
            (kegiatan.nama_kegiatan, kegiatan.deskripsi, kegiatan.status)
        )
        kegiatan.id_kegiatan = cursor.lastrowid
        conn.commit()
        conn.close()
        return kegiatan

    def update(self, kegiatan: Kegiatan) -> Kegiatan:
        conn = self.db_conn.get_connection()
        conn.execute(
            "UPDATE kegiatan SET nama_kegiatan = ?, deskripsi = ?, status = ? WHERE id_kegiatan = ?",
            (kegiatan.nama_kegiatan, kegiatan.deskripsi, kegiatan.status, kegiatan.id_kegiatan)
        )
        conn.commit()
        conn.close()
        return kegiatan

    def hapus(self, id_kegiatan: int) -> bool:
        conn = self.db_conn.get_connection()
        cursor = conn.execute("DELETE FROM kegiatan WHERE id_kegiatan = ?", (id_kegiatan,))
        success = cursor.rowcount > 0
        conn.commit()
        conn.close()
        return success

    def _row_to_entity(self, row) -> Kegiatan:
        return Kegiatan(
            id_kegiatan=row['id_kegiatan'],
            nama_kegiatan=row['nama_kegiatan'],
            deskripsi=row['deskripsi'],
            status=row['status'],
            created_at=datetime.strptime(row['created_at'], "%Y-%m-%d %H:%M:%S") if row['created_at'] else None,
            updated_at=datetime.strptime(row['updated_at'], "%Y-%m-%d %H:%M:%S") if row['updated_at'] else None
        )
