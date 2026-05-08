from dataclasses import dataclass
from datetime import datetime, date, time
from typing import Optional

@dataclass
class Perencanaan:
    id_rencana: Optional[int]
    id_kegiatan: int
    tanggal: date
    jam_mulai: Optional[time] = None
    jam_selesai: Optional[time] = None
    catatan: Optional[str] = None
    status: str = "direncanakan"
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    # Extra field for display
    nama_kegiatan: Optional[str] = None

    def to_dict(self):
        return {
            "id_rencana": self.id_rencana,
            "id_kegiatan": self.id_kegiatan,
            "nama_kegiatan": self.nama_kegiatan,
            "tanggal": self.tanggal.isoformat() if isinstance(self.tanggal, (date, datetime)) else self.tanggal,
            "jam_mulai": self.jam_mulai.strftime("%H:%M") if self.jam_mulai else None,
            "jam_selesai": self.jam_selesai.strftime("%H:%M") if self.jam_selesai else None,
            "catatan": self.catatan,
            "status": self.status
        }
