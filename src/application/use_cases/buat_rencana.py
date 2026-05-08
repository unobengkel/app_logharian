from src.domain.entities.perencanaan import Perencanaan
from src.domain.repositories.perencanaan_repo import PerencanaanRepository
from datetime import datetime

class BuatRencana:
    def __init__(self, repo: PerencanaanRepository):
        self.repo = repo

    def ambil_semua(self, filters: dict = None):
        return self.repo.ambil_semua(filters)

    def ambil_by_id(self, id_rencana: int):
        return self.repo.ambil_by_id(id_rencana)

    def simpan(self, data: dict):
        jam_mulai = datetime.strptime(data['jam_mulai'], "%H:%M").time() if data.get('jam_mulai') else None
        jam_selesai = datetime.strptime(data['jam_selesai'], "%H:%M").time() if data.get('jam_selesai') else None
        tanggal = datetime.strptime(data['tanggal'], "%Y-%m-%d").date() if isinstance(data['tanggal'], str) else data['tanggal']
        
        rencana = Perencanaan(
            id_rencana=None,
            id_kegiatan=int(data['id_kegiatan']),
            tanggal=tanggal,
            jam_mulai=jam_mulai,
            jam_selesai=jam_selesai,
            catatan=data.get('catatan'),
            status=data.get('status', 'direncanakan')
        )
        return self.repo.simpan(rencana)

    def update(self, id_rencana: int, data: dict):
        rencana = self.repo.ambil_by_id(id_rencana)
        if not rencana:
            return None
            
        jam_mulai = datetime.strptime(data['jam_mulai'], "%H:%M").time() if data.get('jam_mulai') else None
        jam_selesai = datetime.strptime(data['jam_selesai'], "%H:%M").time() if data.get('jam_selesai') else None
        tanggal = datetime.strptime(data['tanggal'], "%Y-%m-%d").date() if isinstance(data['tanggal'], str) else data['tanggal']

        rencana.id_kegiatan = int(data['id_kegiatan'])
        rencana.tanggal = tanggal
        rencana.jam_mulai = jam_mulai
        rencana.jam_selesai = jam_selesai
        rencana.catatan = data.get('catatan')
        rencana.status = data.get('status', 'direncanakan')
        
        return self.repo.update(rencana)

    def hapus(self, id_rencana: int):
        return self.repo.hapus(id_rencana)
