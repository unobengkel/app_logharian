from abc import ABC, abstractmethod
from typing import List, Optional
from src.domain.entities.kegiatan import Kegiatan

class KegiatanRepository(ABC):
    @abstractmethod
    def ambil_semua(self, search: str = None, status: str = None) -> List[Kegiatan]:
        pass

    @abstractmethod
    def ambil_by_id(self, id_kegiatan: int) -> Optional[Kegiatan]:
        pass

    @abstractmethod
    def simpan(self, kegiatan: Kegiatan) -> Kegiatan:
        pass

    @abstractmethod
    def update(self, kegiatan: Kegiatan) -> Kegiatan:
        pass

    @abstractmethod
    def hapus(self, id_kegiatan: int) -> bool:
        pass
