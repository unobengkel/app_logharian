from typing import List, Optional
from src.domain.entities.catatan_harian import CatatanHarian
from src.domain.repositories.catatan_repo import CatatanRepository
from datetime import datetime, date, time

class SqliteCatatanRepository(CatatanRepository):
    def __init__(self, db_conn):
        self.db_conn = db_conn

    def ambil_semua(self, filters: dict = None) -> List[CatatanHarian]:
        query = """
            SELECT c.*, k.nama_kegiatan 
            FROM catatan_harian c 
            JOIN kegiatan k ON c.id_kegiatan = k.id_kegiatan 
            WHERE 1=1
        """
        params = []
        if filters:
            if filters.get('tgl_mulai'):
                query += " AND c.tanggal >= ?"
                params.append(filters['tgl_mulai'])
            if filters.get('tgl_selesai'):
                query += " AND c.tanggal <= ?"
                params.append(filters['tgl_selesai'])
            if filters.get('status'):
                query += " AND c.status = ?"
                params.append(filters['status'])
            if filters.get('id_kegiatan'):
                query += " AND c.id_kegiatan = ?"
                params.append(filters['id_kegiatan'])

        query += " ORDER BY c.tanggal DESC, c.jam_mulai ASC"
        
        conn = self.db_conn.get_connection()
        cursor = conn.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        
        return [self._row_to_entity(row) for row in rows]

    def ambil_by_id(self, id_catatan: int) -> Optional[CatatanHarian]:
        conn = self.db_conn.get_connection()
        cursor = conn.execute("""
            SELECT c.*, k.nama_kegiatan 
            FROM catatan_harian c 
            JOIN kegiatan k ON c.id_kegiatan = k.id_kegiatan 
            WHERE id_catatan = ?
        """, (id_catatan,))
        row = cursor.fetchone()
        conn.close()
        return self._row_to_entity(row) if row else None

    def simpan(self, catatan: CatatanHarian) -> CatatanHarian:
        jam_mulai_str = catatan.jam_mulai.strftime("%H:%M") if catatan.jam_mulai else None
        jam_selesai_str = catatan.jam_selesai.strftime("%H:%M") if catatan.jam_selesai else None

        conn = self.db_conn.get_connection()
        cursor = conn.execute(
            """INSERT INTO catatan_harian (id_kegiatan, tanggal, jam_mulai, jam_selesai, deskripsi, status) 
               VALUES (?, ?, ?, ?, ?, ?)""",
            (catatan.id_kegiatan, catatan.tanggal, jam_mulai_str, jam_selesai_str, catatan.deskripsi, catatan.status)
        )
        catatan.id_catatan = cursor.lastrowid
        conn.commit()
        conn.close()
        return catatan

    def update(self, catatan: CatatanHarian) -> CatatanHarian:
        jam_mulai_str = catatan.jam_mulai.strftime("%H:%M") if catatan.jam_mulai else None
        jam_selesai_str = catatan.jam_selesai.strftime("%H:%M") if catatan.jam_selesai else None

        conn = self.db_conn.get_connection()
        conn.execute(
            """UPDATE catatan_harian SET id_kegiatan = ?, tanggal = ?, jam_mulai = ?, jam_selesai = ?, deskripsi = ?, status = ? 
               WHERE id_catatan = ?""",
            (catatan.id_kegiatan, catatan.tanggal, jam_mulai_str, jam_selesai_str, catatan.deskripsi, catatan.status, catatan.id_catatan)
        )
        conn.commit()
        conn.close()
        return catatan

    def hapus(self, id_catatan: int) -> bool:
        conn = self.db_conn.get_connection()
        cursor = conn.execute("DELETE FROM catatan_harian WHERE id_catatan = ?", (id_catatan,))
        success = cursor.rowcount > 0
        conn.commit()
        conn.close()
        return success

    def _row_to_entity(self, row) -> CatatanHarian:
        jam_mulai = None
        if row['jam_mulai']:
            try:
                jam_mulai = datetime.strptime(row['jam_mulai'], "%H:%M").time()
            except ValueError:
                jam_mulai = datetime.strptime(row['jam_mulai'], "%H:%M:%S").time()

        jam_selesai = None
        if row['jam_selesai']:
            try:
                jam_selesai = datetime.strptime(row['jam_selesai'], "%H:%M").time()
            except ValueError:
                jam_selesai = datetime.strptime(row['jam_selesai'], "%H:%M:%S").time()

        tanggal = row['tanggal']
        if isinstance(tanggal, str):
            try:
                tanggal = datetime.strptime(tanggal, "%Y-%m-%d").date()
            except ValueError:
                pass

        return CatatanHarian(
            id_catatan=row['id_catatan'],
            id_kegiatan=row['id_kegiatan'],
            tanggal=tanggal,
            jam_mulai=jam_mulai,
            jam_selesai=jam_selesai,
            deskripsi=row['deskripsi'],
            status=row['status'],
            nama_kegiatan=row['nama_kegiatan'] if 'nama_kegiatan' in row.keys() else None
        )
