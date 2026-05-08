from flask import render_template, request, redirect, flash, url_for
from src.application.use_cases.kelola_kegiatan import KelolaKegiatan

class KegiatanController:
    def __init__(self, use_case: KelolaKegiatan):
        self.use_case = use_case

    def index(self):
        search = request.args.get('search')
        status = request.args.get('status')
        data = self.use_case.ambil_semua(search, status)
        return render_template('kegiatan/daftar.html', data=data)

    def create(self):
        return render_template('kegiatan/form.html', data=None)

    def store(self):
        try:
            data = request.form.to_dict()
            self.use_case.tambah(data)
            flash('Kegiatan berhasil ditambahkan!', 'success')
            return redirect(url_for('kegiatan_index'))
        except Exception as e:
            flash(f'Gagal menambahkan kegiatan: {str(e)}', 'error')
            return render_template('kegiatan/form.html', data=request.form)

    def edit(self, id):
        kegiatan = self.use_case.ambil_by_id(id)
        if not kegiatan:
            flash('Kegiatan tidak ditemukan!', 'error')
            return redirect(url_for('kegiatan_index'))
        return render_template('kegiatan/form.html', data=kegiatan)

    def update(self, id):
        try:
            data = request.form.to_dict()
            self.use_case.update(id, data)
            flash('Kegiatan berhasil diperbarui!', 'success')
            return redirect(url_for('kegiatan_index'))
        except Exception as e:
            flash(f'Gagal memperbarui kegiatan: {str(e)}', 'error')
            return render_template('kegiatan/form.html', data={'id_kegiatan': id, **request.form})

    def destroy(self, id):
        if self.use_case.hapus(id):
            flash('Kegiatan berhasil dihapus!', 'success')
        else:
            flash('Gagal menghapus kegiatan!', 'error')
        return redirect(url_for('kegiatan_index'))
