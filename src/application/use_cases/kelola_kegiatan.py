from src.domain.entities.kegiatan import Kegiatan
from src.domain.repositories.kegiatan_repo import KegiatanRepository

class KelolaKegiatan:
    def __init__(self, repo: KegiatanRepository):
        self.repo = repo

    def ambil_semua(self, search: str = None, status: str = None):
        return self.repo.ambil_semua(search, status)

    def ambil_by_id(self, id_kegiatan: int):
        return self.repo.ambil_by_id(id_kegiatan)

    def tambah(self, data: dict):
        kegiatan = Kegiatan(
            id_kegiatan=None,
            nama_kegiatan=data['nama_kegiatan'],
            deskripsi=data.get('deskripsi'),
            status=data.get('status', 'aktif')
        )
        return self.repo.simpan(kegiatan)

    def update(self, id_kegiatan: int, data: dict):
        kegiatan = self.repo.ambil_by_id(id_kegiatan)
        if not kegiatan:
            return None
        
        kegiatan.nama_kegiatan = data['nama_kegiatan']
        kegiatan.deskripsi = data.get('deskripsi')
        kegiatan.status = data.get('status', 'aktif')
        
        return self.repo.update(kegiatan)

    def hapus(self, id_kegiatan: int):
        return self.repo.hapus(id_kegiatan)
