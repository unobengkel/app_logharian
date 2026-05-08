from src.domain.entities.catatan_harian import CatatanHarian
from src.domain.repositories.catatan_repo import CatatanRepository
from datetime import datetime

class CatatHarian:
    def __init__(self, repo: CatatanRepository):
        self.repo = repo

    def ambil_semua(self, filters: dict = None):
        return self.repo.ambil_semua(filters)

    def ambil_by_id(self, id_catatan: int):
        return self.repo.ambil_by_id(id_catatan)

    def simpan(self, data: dict):
        jam_mulai = datetime.strptime(data['jam_mulai'], "%H:%M").time() if data.get('jam_mulai') else None
        jam_selesai = datetime.strptime(data['jam_selesai'], "%H:%M").time() if data.get('jam_selesai') else None
        tanggal = datetime.strptime(data['tanggal'], "%Y-%m-%d").date() if isinstance(data['tanggal'], str) else data['tanggal']

        catatan = CatatanHarian(
            id_catatan=None,
            id_kegiatan=int(data['id_kegiatan']),
            tanggal=tanggal,
            jam_mulai=jam_mulai,
            jam_selesai=jam_selesai,
            deskripsi=data['deskripsi'],
            status=data.get('status', 'selesai')
        )
        return self.repo.simpan(catatan)

    def update(self, id_catatan: int, data: dict):
        catatan = self.repo.ambil_by_id(id_catatan)
        if not catatan:
            return None

        jam_mulai = datetime.strptime(data['jam_mulai'], "%H:%M").time() if data.get('jam_mulai') else None
        jam_selesai = datetime.strptime(data['jam_selesai'], "%H:%M").time() if data.get('jam_selesai') else None
        tanggal = datetime.strptime(data['tanggal'], "%Y-%m-%d").date() if isinstance(data['tanggal'], str) else data['tanggal']

        catatan.id_kegiatan = int(data['id_kegiatan'])
        catatan.tanggal = tanggal
        catatan.jam_mulai = jam_mulai
        catatan.jam_selesai = jam_selesai
        catatan.deskripsi = data['deskripsi']
        catatan.status = data.get('status', 'selesai')
        
        return self.repo.update(catatan)

    def hapus(self, id_catatan: int):
        return self.repo.hapus(id_catatan)
