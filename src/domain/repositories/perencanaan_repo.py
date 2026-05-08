from abc import ABC, abstractmethod
from typing import List, Optional
from src.domain.entities.perencanaan import Perencanaan

class PerencanaanRepository(ABC):
    @abstractmethod
    def ambil_semua(self, filters: dict = None) -> List[Perencanaan]:
        pass

    @abstractmethod
    def ambil_by_id(self, id_rencana: int) -> Optional[Perencanaan]:
        pass

    @abstractmethod
    def simpan(self, rencana: Perencanaan) -> Perencanaan:
        pass

    @abstractmethod
    def update(self, rencana: Perencanaan) -> Perencanaan:
        pass

    @abstractmethod
    def hapus(self, id_rencana: int) -> bool:
        pass
