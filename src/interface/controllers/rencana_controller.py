from flask import render_template, request, redirect, flash, url_for
from src.application.use_cases.buat_rencana import BuatRencana
from src.application.use_cases.kelola_kegiatan import KelolaKegiatan

class RencanaController:
    def __init__(self, use_case: BuatRencana, kegiatan_uc: KelolaKegiatan):
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
        return render_template('rencana/daftar.html', data=data, kegiatan=kegiatan_list)

    def create(self):
        kegiatan_list = self.kegiatan_uc.ambil_semua(status='aktif')
        return render_template('rencana/form.html', data=None, kegiatan=kegiatan_list)

    def store(self):
        try:
            data = request.form.to_dict()
            self.use_case.simpan(data)
            flash('Rencana berhasil disimpan!', 'success')
            return redirect(url_for('rencana_index'))
        except Exception as e:
            flash(f'Gagal menyimpan rencana: {str(e)}', 'error')
            kegiatan_list = self.kegiatan_uc.ambil_semua(status='aktif')
            return render_template('rencana/form.html', data=request.form, kegiatan=kegiatan_list)

    def edit(self, id):
        rencana = self.use_case.ambil_by_id(id)
        if not rencana:
            flash('Rencana tidak ditemukan!', 'error')
            return redirect(url_for('rencana_index'))
        kegiatan_list = self.kegiatan_uc.ambil_semua(status='aktif')
        return render_template('rencana/form.html', data=rencana, kegiatan=kegiatan_list)

    def update(self, id):
        try:
            data = request.form.to_dict()
            self.use_case.update(id, data)
            flash('Rencana berhasil diperbarui!', 'success')
            return redirect(url_for('rencana_index'))
        except Exception as e:
            flash(f'Gagal memperbarui rencana: {str(e)}', 'error')
            kegiatan_list = self.kegiatan_uc.ambil_semua(status='aktif')
            return render_template('rencana/form.html', data={'id_rencana': id, **request.form}, kegiatan=kegiatan_list)

    def destroy(self, id):
        if self.use_case.hapus(id):
            flash('Rencana berhasil dihapus!', 'success')
        else:
            flash('Gagal menghapus rencana!', 'error')
        return redirect(url_for('rencana_index'))
