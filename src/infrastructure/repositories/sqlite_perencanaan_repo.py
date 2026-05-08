from typing import List, Optional
from src.domain.entities.perencanaan import Perencanaan
from src.domain.repositories.perencanaan_repo import PerencanaanRepository
from datetime import datetime, date, time

class SqlitePerencanaanRepository(PerencanaanRepository):
    def __init__(self, db_conn):
        self.db_conn = db_conn

    def ambil_semua(self, filters: dict = None) -> List[Perencanaan]:
        query = """
            SELECT p.*, k.nama_kegiatan 
            FROM perencanaan p 
            JOIN kegiatan k ON p.id_kegiatan = k.id_kegiatan 
            WHERE 1=1
        """
        params = []
        if filters:
            if filters.get('tgl_mulai'):
                query += " AND p.tanggal >= ?"
                params.append(filters['tgl_mulai'])
            if filters.get('tgl_selesai'):
                query += " AND p.tanggal <= ?"
                params.append(filters['tgl_selesai'])
            if filters.get('status'):
                query += " AND p.status = ?"
                params.append(filters['status'])
            if filters.get('id_kegiatan'):
                query += " AND p.id_kegiatan = ?"
                params.append(filters['id_kegiatan'])

        query += " ORDER BY p.tanggal DESC, p.jam_mulai ASC"
        
        conn = self.db_conn.get_connection()
        cursor = conn.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        
        return [self._row_to_entity(row) for row in rows]

    def ambil_by_id(self, id_rencana: int) -> Optional[Perencanaan]:
        conn = self.db_conn.get_connection()
        cursor = conn.execute("""
            SELECT p.*, k.nama_kegiatan 
            FROM perencanaan p 
            JOIN kegiatan k ON p.id_kegiatan = k.id_kegiatan 
            WHERE id_rencana = ?
        """, (id_rencana,))
        row = cursor.fetchone()
        conn.close()
        return self._row_to_entity(row) if row else None

    def simpan(self, rencana: Perencanaan) -> Perencanaan:
        jam_mulai_str = rencana.jam_mulai.strftime("%H:%M") if rencana.jam_mulai else None
        jam_selesai_str = rencana.jam_selesai.strftime("%H:%M") if rencana.jam_selesai else None
        
        conn = self.db_conn.get_connection()
        cursor = conn.execute(
            """INSERT INTO perencanaan (id_kegiatan, tanggal, jam_mulai, jam_selesai, catatan, status) 
               VALUES (?, ?, ?, ?, ?, ?)""",
            (rencana.id_kegiatan, rencana.tanggal, jam_mulai_str, jam_selesai_str, rencana.catatan, rencana.status)
        )
        rencana.id_rencana = cursor.lastrowid
        conn.commit()
        conn.close()
        return rencana

    def update(self, rencana: Perencanaan) -> Perencanaan:
        jam_mulai_str = rencana.jam_mulai.strftime("%H:%M") if rencana.jam_mulai else None
        jam_selesai_str = rencana.jam_selesai.strftime("%H:%M") if rencana.jam_selesai else None

        conn = self.db_conn.get_connection()
        conn.execute(
            """UPDATE perencanaan SET id_kegiatan = ?, tanggal = ?, jam_mulai = ?, jam_selesai = ?, catatan = ?, status = ? 
               WHERE id_rencana = ?""",
            (rencana.id_kegiatan, rencana.tanggal, jam_mulai_str, jam_selesai_str, rencana.catatan, rencana.status, rencana.id_rencana)
        )
        conn.commit()
        conn.close()
        return rencana

    def hapus(self, id_rencana: int) -> bool:
        conn = self.db_conn.get_connection()
        cursor = conn.execute("DELETE FROM perencanaan WHERE id_rencana = ?", (id_rencana,))
        success = cursor.rowcount > 0
        conn.commit()
        conn.close()
        return success

    def _row_to_entity(self, row) -> Perencanaan:
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

        return Perencanaan(
            id_rencana=row['id_rencana'],
            id_kegiatan=row['id_kegiatan'],
            tanggal=tanggal,
            jam_mulai=jam_mulai,
            jam_selesai=jam_selesai,
            catatan=row['catatan'],
            status=row['status'],
            nama_kegiatan=row['nama_kegiatan'] if 'nama_kegiatan' in row.keys() else None
        )
