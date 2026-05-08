from flask import Flask, render_template, redirect, url_for
from src.infrastructure.database.db_connection import DBConnection
from src.infrastructure.repositories.sqlite_kegiatan_repo import SqliteKegiatanRepository
from src.infrastructure.repositories.sqlite_perencanaan_repo import SqlitePerencanaanRepository
from src.infrastructure.repositories.sqlite_catatan_repo import SqliteCatatanRepository
from src.application.use_cases.kelola_kegiatan import KelolaKegiatan
from src.application.use_cases.buat_rencana import BuatRencana
from src.application.use_cases.catat_harian import CatatHarian
from src.interface.controllers.kegiatan_controller import KegiatanController
from datetime import datetime

app = Flask(__name__, 
            template_folder='src/interface/templates',
            static_folder='src/interface/static')
app.secret_key = 'super-secret-key-for-catatan-harian'

# Dependency Injection
db_conn = DBConnection()
kegiatan_repo = SqliteKegiatanRepository(db_conn)
rencana_repo = SqlitePerencanaanRepository(db_conn)
catatan_repo = SqliteCatatanRepository(db_conn)

kelola_kegiatan_uc = KelolaKegiatan(kegiatan_repo)
buat_rencana_uc = BuatRencana(rencana_repo)
catat_harian_uc = CatatHarian(catatan_repo)

kegiatan_ctrl = KegiatanController(kelola_kegiatan_uc)
from src.interface.controllers.rencana_controller import RencanaController
from src.interface.controllers.catatan_controller import CatatanController
rencana_ctrl = RencanaController(buat_rencana_uc, kelola_kegiatan_uc)
catatan_ctrl = CatatanController(catat_harian_uc, kelola_kegiatan_uc)

# Dashboard
@app.route('/')
def dashboard():
    today = datetime.now().strftime("%Y-%m-%d")
    stats = {
        "total_kegiatan": len(kegiatan_repo.ambil_semua(status='aktif')),
        "rencana_hari_ini": len(rencana_repo.ambil_semua({'tgl_mulai': today, 'tgl_selesai': today})),
        "catatan_hari_ini": len(catatan_repo.ambil_semua({'tgl_mulai': today, 'tgl_selesai': today, 'status': 'selesai'}))
    }
    return render_template('dashboard.html', stats=stats)

# Kegiatan Routes
@app.route('/kegiatan')
def kegiatan_index():
    return kegiatan_ctrl.index()

@app.route('/kegiatan/tambah')
def kegiatan_create():
    return kegiatan_ctrl.create()

@app.route('/kegiatan', methods=['POST'])
def kegiatan_store():
    return kegiatan_ctrl.store()

@app.route('/kegiatan/<int:id>/edit')
def kegiatan_edit(id):
    return kegiatan_ctrl.edit(id)

@app.route('/kegiatan/<int:id>/update', methods=['POST'])
def kegiatan_update(id):
    return kegiatan_ctrl.update(id)

@app.route('/kegiatan/<int:id>/hapus', methods=['POST'])
def kegiatan_destroy(id):
    return kegiatan_ctrl.destroy(id)

# Rencana Routes
@app.route('/rencana')
def rencana_index():
    return rencana_ctrl.index()

@app.route('/rencana/tambah')
def rencana_create():
    return rencana_ctrl.create()

@app.route('/rencana', methods=['POST'])
def rencana_store():
    return rencana_ctrl.store()

@app.route('/rencana/<int:id>/edit')
def rencana_edit(id):
    return rencana_ctrl.edit(id)

@app.route('/rencana/<int:id>/update', methods=['POST'])
def rencana_update(id):
    return rencana_ctrl.update(id)

@app.route('/rencana/<int:id>/hapus', methods=['POST'])
def rencana_destroy(id):
    return rencana_ctrl.destroy(id)

# Catatan Routes
@app.route('/catatan')
def catatan_index():
    return catatan_ctrl.index()

@app.route('/catatan/tambah')
def catatan_create():
    return catatan_ctrl.create()

@app.route('/catatan', methods=['POST'])
def catatan_store():
    return catatan_ctrl.store()

@app.route('/catatan/<int:id>/edit')
def catatan_edit(id):
    return catatan_ctrl.edit(id)

@app.route('/catatan/<int:id>/update', methods=['POST'])
def catatan_update(id):
    return catatan_ctrl.update(id)

@app.route('/catatan/<int:id>/hapus', methods=['POST'])
def catatan_destroy(id):
    return catatan_ctrl.destroy(id)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
