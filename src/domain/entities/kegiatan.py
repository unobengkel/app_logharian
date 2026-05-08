from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Kegiatan:
    id_kegiatan: Optional[int]
    nama_kegiatan: str
    deskripsi: Optional[str] = None
    status: str = "aktif"
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def to_dict(self):
        return {
            "id_kegiatan": self.id_kegiatan,
            "nama_kegiatan": self.nama_kegiatan,
            "deskripsi": self.deskripsi,
            "status": self.status,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S") if self.created_at else None,
            "updated_at": self.updated_at.strftime("%Y-%m-%d %H:%M:%S") if self.updated_at else None
        }
