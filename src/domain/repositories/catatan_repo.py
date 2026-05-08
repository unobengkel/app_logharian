from abc import ABC, abstractmethod
from typing import List, Optional
from src.domain.entities.catatan_harian import CatatanHarian

class CatatanRepository(ABC):
    @abstractmethod
    def ambil_semua(self, filters: dict = None) -> List[CatatanHarian]:
        pass

    @abstractmethod
    def ambil_by_id(self, id_catatan: int) -> Optional[CatatanHarian]:
        pass

    @abstractmethod
    def simpan(self, catatan: CatatanHarian) -> CatatanHarian:
        pass

    @abstractmethod
    def update(self, catatan: CatatanHarian) -> CatatanHarian:
        pass

    @abstractmethod
    def hapus(self, id_catatan: int) -> bool:
        pass
