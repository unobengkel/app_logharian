from flask import render_template, request, redirect, flash, url_for
from src.application.use_cases.catat_harian import CatatHarian
from src.application.use_cases.kelola_kegiatan import KelolaKegiatan

class CatatanController:
    def __init__(self, use_case: CatatHarian, kegiatan_uc: KelolaKegiatan):
        self.use_case = use_case
        self.kegiatan_uc = kegiatan_uc

    def index(self):
        filters = {
            'tgl_mulai': request.args.get('tgl_mulai'),
            'tgl_selesai': request.args.get('tgl_selesai'),
            'status': request.args.get('status'),
            'id_kegiatan': request.args.get('id_kegiatan')
        }
        data = self.use_case.ambil_semua(filters)
        kegiatan_list = self.kegiatan_uc.ambil_semua(status='aktif')
        return render_template('catatan/daftar.html', data=data, kegiatan=kegiatan_list)

    def create(self):
        kegiatan_list = self.kegiatan_uc.ambil_semua(status='aktif')
        return render_template('catatan/form.html', data=None, kegiatan=kegiatan_list)

    def store(self):
        try:
            data = request.form.to_dict()
            self.use_case.simpan(data)
            flash('Catatan berhasil disimpan!', 'success')
            return redirect(url_for('catatan_index'))
        except Exception as e:
            flash(f'Gagal menyimpan catatan: {str(e)}', 'error')
            kegiatan_list = self.kegiatan_uc.ambil_semua(status='aktif')
            return render_template('catatan/form.html', data=request.form, kegiatan=kegiatan_list)

    def edit(self, id):
        catatan = self.use_case.ambil_by_id(id)
        if not catatan:
            flash('Catatan tidak ditemukan!', 'error')
            return redirect(url_for('catatan_index'))
        kegiatan_list = self.kegiatan_uc.ambil_semua(status='aktif')
        return render_template('catatan/form.html', data=catatan, kegiatan=kegiatan_list)

    def update(self, id):
        try:
            data = request.form.to_dict()
            self.use_case.update(id, data)
            flash('Catatan berhasil diperbarui!', 'success')
            return redirect(url_for('catatan_index'))
        except Exception as e:
            flash(f'Gagal memperbarui catatan: {str(e)}', 'error')
            kegiatan_list = self.kegiatan_uc.ambil_semua(status='aktif')
            return render_template('catatan/form.html', data={'id_catatan': id, **request.form}, kegiatan=kegiatan_list)

    def destroy(self, id):
        if self.use_case.hapus(id):
            flash('Catatan berhasil dihapus!', 'success')
        else:
            flash('Gagal menghapus catatan!', 'error')
        return redirect(url_for('catatan_index'))
