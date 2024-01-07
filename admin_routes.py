from flask import Flask, render_template, request, redirect, session, url_for, Response, flash
from werkzeug.utils import secure_filename
from main import app
from get_data import *
import hashlib
import config


#halaman login
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Menggunakan hashlib untuk menghash password dengan MD5
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        # Lakukan query ke database untuk mencari user dengan username dan password tertentu
        query = "SELECT * FROM admin WHERE username = %s AND password = %s"
        config.db_cursor.execute(query, (username, hashed_password))
        user = config.db_cursor.fetchone()

        if user:
            # Ambil nilai id_users dari hasil kueri
            id_admin = user['id_admin']
            nama = user['nama']
            session['id_admin'] = id_admin
            session['nama'] = nama
            return redirect(url_for('dashboard'))
        else:
            error='Username atau password salah. Silahkan coba lagi.'
    return render_template('admin/login.html', error=error)

# Halaman logout
@app.route('/admin_logout')
def admin_logout():
    session.pop('username', None)
    return redirect(url_for('admin_login'))

@app.route('/admin/dashboard')
def dashboard():
    if 'id_admin' in session:
        id_admin = session.get('id_admin')
        nama = session.get('nama')
        karyawan = get_employees_count()
        jabatan = get_position_count()
        jam_kerja = get_shift_count()
        cuty = get_cuty_count()
    else:
        return redirect(url_for('admin_login'))
    return render_template('admin/index.html', nama=nama, karyawan=karyawan, jabatan=jabatan, jam_kerja=jam_kerja, cuty=cuty)

@app.route('/admin/karyawan')
def karyawan():
    if 'id_admin' in session:
        id_admin = session.get('id_admin')
        nama = session.get('nama')
        employees = get_employees_data()
        
        positions = get_positions()
        shifts = get_shift()
    else:
        return redirect(url_for('admin_login'))
    return render_template('admin/karyawan.html', nama=nama, employees=employees, positions=positions, shifts=shifts)

@app.route('/admin/update-karyawan', methods=['GET', 'POST'])
def update_karyawan():
    if request.method == 'POST':
        try:
            id_employees = request.form['id_employees']
            name = request.form['name']
            position = request.form['id_position']
            shift = request.form['id_shift']

            query = "UPDATE employees SET name=%s, id_position=%s, id_shift=%s WHERE id_employees=%s"
            config.db_cursor.execute(query, (name, position, shift, id_employees))
            config.db_connection.commit()
            flash('Update data berhasil', 'success')
            return redirect(url_for('karyawan'))
        except Exception as e:
            print(f'ini error: {str(e)}')
            config.db_connection.rollback()  # Rollback perubahan jika ada kesalahan dalam query
            flash(f'Gagal memperbarui data: {str(e)}', 'error')
            return redirect(url_for('karyawan'))
    return redirect(url_for('karyawan'))

@app.route('/admin/jabatan')
def jabatan():
    if 'id_admin' in session:
        id_admin = session.get('id_admin')
        nama = session.get('nama')
        positions = get_positions()
    else:
        return redirect(url_for('admin_login'))
    return render_template('admin/jabatan.html', nama=nama, positions=positions)

@app.route('/admin/tambah-jabatan', methods=['GET', 'POST'])
def tambah_jabatan():
    if request.method == 'POST':
        try:
            position_name = request.form['nama']
            query = "INSERT INTO position (position_name) VALUE (%s)"
            config.db_cursor.execute(query, (position_name,))
            config.db_connection.commit()
            flash('Tambah data berhasil', 'success')
            return redirect(url_for('jabatan'))
        except Exception as e:
            print(f'ini error: {str(e)}')
            config.db_connection.rollback()
            flash(f'Gagal menambah data: {str(e)}', 'error')
            return redirect(url_for('jabatan'))
    return redirect(url_for('jabatan'))

@app.route('/admin/update-jabatan', methods=['GET', 'POST'])
def update_jabatan():
    if request.method == 'POST':
        try:
            id_position = request.form['id_position']
            position_name = request.form['nama']
            query = "UPDATE position SET position_name = %s WHERE id_position = %s"
            config.db_cursor.execute(query, (position_name, id_position))
            config.db_connection.commit()
            flash('Update data berhasil', 'success')
            return redirect(url_for('jabatan'))
        except Exception as e:
            print(f'ini error: {str(e)}')
            config.db_connection.rollback()
            flash(f'Gagal memperbarui data: {str(e)}', 'error')
            return redirect(url_for('jabatan'))
    return redirect(url_for('jabatan'))

@app.route('/admin/hapus-jabatan', methods=['GET', 'POST'])
def delete_jabatan():
    if request.method == 'POST':
        try:
            id_position = request.form['id_position']
            query = "DELETE FROM position WHERE id_position = %s"
            config.db_cursor.execute(query, (id_position,))
            config.db_connection.commit()
            flash('Hapus data berhasil', 'success')
            return redirect(url_for('jabatan'))
        except Exception as e:
            print(f'ini error: {str(e)}')
            config.db_connection.rollback()
            flash(f'Gagal menghapus data: {str(e)}', 'error')
            return redirect(url_for('jabatan'))
    return redirect(url_for('jabatan'))

@app.route('/admin/shift')
def shift():
    if 'id_admin' in session:
        id_admin = session.get('id_admin')
        nama = session.get('nama')
        jam_kerja = get_shift()
    else:
        return redirect(url_for('admin_login'))
    return render_template('admin/shift.html', nama=nama, jam_kerja=jam_kerja)

@app.route('/admin/tambah-shift', methods=['GET', 'POST'])
def tambah_shift():
    if request.method == 'POST':
        try:
            shift_name = request.form['nama']
            time_in = request.form['time_in']
            time_out = request.form['time_out']
            query = "INSERT INTO shift (shift_name, time_in, time_out) VALUE (%s, %s, %s)"
            config.db_cursor.execute(query, (shift_name, time_in, time_out))
            config.db_connection.commit()
            flash('Tambah data berhasil', 'success')
            return redirect(url_for('shift'))
        except Exception as e:
            print(f'ini error: {str(e)}')
            config.db_connection.rollback()
            flash(f'Gagal menambah data: {str(e)}', 'error')
            return redirect(url_for('shift'))
    return redirect(url_for('shift'))

@app.route('/admin/update-shift', methods=['GET', 'POST'])
def update_shift():
    if request.method == 'POST':
        try:
            id_shift = request.form['id_shift']
            shift_name = request.form['nama']
            time_in = request.form['time_in']
            time_out = request.form['time_out']
            query = "UPDATE shift SET shift_name = %s, time_in = %s, time_out = %s WHERE id_shift = %s"
            config.db_cursor.execute(query, (shift_name, time_in, time_out, id_shift))
            config.db_connection.commit()
            flash('Update data berhasil', 'success')
            return redirect(url_for('shift'))
        except Exception as e:
            print(f'ini error: {str(e)}')
            config.db_connection.rollback()
            flash(f'Gagal memperbarui data: {str(e)}', 'error')
            return redirect(url_for('shift'))
    return redirect(url_for('shift'))

@app.route('/admin/hapus-shift', methods=['GET', 'POST'])
def delete_shift():
    if request.method == 'POST':
        try:
            id_shift = request.form['id_shift']
            query = "DELETE FROM shift WHERE id_shift = %s"
            config.db_cursor.execute(query, (id_shift,))
            config.db_connection.commit()
            flash('Hapus data berhasil', 'success')
            return redirect(url_for('shift'))
        except Exception as e:
            print(f'ini error: {str(e)}')
            config.db_connection.rollback()
            flash(f'Gagal menghapus data: {str(e)}', 'error')
            return redirect(url_for('shift'))
    return redirect(url_for('shift'))

@app.route('/admin/admin_cuty')
def admin_cuty():
    if 'id_admin' in session:
        id_admin = session.get('id_admin')
        nama = session.get('nama')
        cutys = get_employees_cuty_admin()
        employees = get_employees()
    else:
        return redirect(url_for('admin_login'))
    return render_template('admin/cuty.html', nama=nama, cutys=cutys, employees=employees)

@app.route('/admin/tambah-cuty', methods=['GET', 'POST'])
def tambah_admin_cuty():
    if request.method == 'POST':
        try:
            id_employees = request.form['id_employees']
            cuty_start = request.form['cuty_start']
            cuty_end = request.form['cuty_end']
            date_work = request.form['date_work']
            cuty_description = request.form['cuty_desc']
            status = request.form['status']
            query = "INSERT INTO cuty (id_employees, cuty_start, cuty_end, date_work, cuty_description, cuty_status) VALUE (%s, %s, %s, %s, %s, %s)"
            config.db_cursor.execute(query, (id_employees, cuty_start, cuty_end, date_work, cuty_description, status))
            config.db_connection.commit()
            flash('Tambah data berhasil', 'success')
            return redirect(url_for('admin_cuty'))
        except Exception as e:
            print(f'ini error: {str(e)}')
            config.db_connection.rollback()
            flash(f'Gagal menambah data: {str(e)}', 'error')
            return redirect(url_for('admin_cuty'))
    return redirect(url_for('admin_cuty'))

@app.route('/admin/update-cuty', methods=['GET', 'POST'])
def update_admin_cuty():
    if request.method == 'POST':
        try:
            id_cuty = request.form['id_cuty']
            status = request.form['status']
            query = "UPDATE cuty SET cuty_status = %s WHERE id_cuty = %s"
            config.db_cursor.execute(query, (status, id_cuty))
            config.db_connection.commit()
            flash('Update data berhasil', 'success')
            return redirect(url_for('admin_cuty'))
        except Exception as e:
            print(f'ini error: {str(e)}')
            config.db_connection.rollback()
            flash(f'Gagal memperbarui data: {str(e)}', 'error')
            return redirect(url_for('admin_cuty'))
    return redirect(url_for('admin_cuty'))

@app.route('/admin/hapus-cuty', methods=['GET', 'POST'])
def delete_admin_cuty():
    if request.method == 'POST':
        try:
            id_cuty = request.form['id_cuty']
            query = "DELETE FROM cuty WHERE id_cuty = %s"
            config.db_cursor.execute(query, (id_cuty,))
            config.db_connection.commit()
            flash('Hapus data berhasil', 'success')
            return redirect(url_for('admin_cuty'))
        except Exception as e:
            print(f'ini error: {str(e)}')
            config.db_connection.rollback()
            flash(f'Gagal menghapus data: {str(e)}', 'error')
            return redirect(url_for('admin_cuty'))
    return redirect(url_for('admin_cuty'))

@app.route('/admin/admin_absen')
def admin_absen():
    if 'id_admin' in session:
        id_admin = session.get('id_admin')
        nama = session.get('nama')
        presences = get_presence_admin()
        employees = get_employees()
        presents = get_presence_status()
    else:
        return redirect(url_for('admin_login'))
    return render_template('admin/absen.html', nama=nama, presences=presences, employees=employees, presents=presents)

@app.route('/admin/tambah-absen', methods=['GET', 'POST'])
def tambah_admin_absen():
    if request.method == 'POST':
        try:
            id_employees = request.form['id_employees']
            date = request.form['date']
            query_check = "SELECT * FROM presence WHERE id_employees = %s AND presence_date = %s"
            config.db_cursor.execute(query_check, (id_employees, date))
            existing_presence = config.db_cursor.fetchone()
            
            if existing_presence:
                flash('Data Absensi untuk karyawan pada tanggal tersebut sudah ada', 'info')
                return redirect(url_for('admin_absen'))
            
            time_in = request.form['time_in']
            time_out = request.form['time_out']
            keterangan = request.form['keterangan']
            status = request.form['status']
            
            query_insert = "INSERT INTO presence (id_employees, presence_date, time_in, time_out, keterangan, id_present) VALUES (%s, %s, %s, %s, %s, %s)"
            config.db_cursor.execute(query_insert, (id_employees, date, time_in, time_out, keterangan, status))
            config.db_connection.commit()
            
            flash('Tambah data berhasil', 'success')
            return redirect(url_for('admin_absen'))
        except Exception as e:
            print(f'ini error: {str(e)}')
            config.db_connection.rollback()
            flash(f'Gagal menambah data: {str(e)}', 'error')
            return redirect(url_for('admin_absen'))
    return redirect(url_for('admin_absen'))

@app.route('/admin/update-absen', methods=['GET', 'POST'])
def update_admin_absen():
    if request.method == 'POST':
        try:
            id_presence = request.form['id_presence']
            status = request.form['status']
            query = "UPDATE presence SET id_present = %s WHERE id_presence = %s"
            config.db_cursor.execute(query, (status, id_presence))
            config.db_connection.commit()
            flash('Update data berhasil', 'success')
            return redirect(url_for('admin_absen'))
        except Exception as e:
            print(f'ini error: {str(e)}')
            config.db_connection.rollback()
            flash(f'Gagal memperbarui data: {str(e)}', 'error')
            return redirect(url_for('admin_absen'))
    return redirect(url_for('admin_absen'))

@app.route('/admin/hapus-absen', methods=['GET', 'POST'])
def delete_admin_absen():
    if request.method == 'POST':
        try:
            id_presence = request.form['id_presence']
            query = "DELETE FROM presence WHERE id_presence = %s"
            config.db_cursor.execute(query, (id_presence,))
            config.db_connection.commit()
            flash('Hapus data berhasil', 'success')
            return redirect(url_for('admin_absen'))
        except Exception as e:
            print(f'ini error: {str(e)}')
            config.db_connection.rollback()
            flash(f'Gagal menghapus data: {str(e)}', 'error')
            return redirect(url_for('admin_absen'))
    return redirect(url_for('admin_absen'))

@app.route('/admin/akun')
def akun():
    if 'id_admin' in session:
        id_admin = session.get('id_admin')
        nama = session.get('nama')
        admins = get_admin()
    else:
        return redirect(url_for('admin_login'))
    return render_template('admin/akun.html', nama=nama, admins=admins)

@app.route('/admin/tambah-admin', methods=['GET', 'POST'])
def tambah_admin():
    if request.method == 'POST':
        try:
            nama = request.form['nama']
            username = request.form['username']
            password1 = request.form['password1']
            password2 = request.form['password2']
            if password1 == password2:
                password = hashlib.sha256(password1.encode()).hexdigest()
                query = "INSERT INTO admin (nama, username, password) VALUE (%s, %s, %s)"
                config.db_cursor.execute(query, (nama, username, password))
                config.db_connection.commit()
                flash('Tambah data berhasil', 'error')
                return redirect(url_for('akun'))
            else:
                flash('Tambah data gagal', 'error')
                return redirect(url_for('akun'))
        except Exception as e:
            print(f'ini error: {str(e)}')
            config.db_connection.rollback()
            flash(f'Gagal menambah data: {str(e)}', 'error')
            return redirect(url_for('akun'))
    return redirect(url_for('akun'))


@app.route('/admin/update-admin', methods=['GET', 'POST'])
def update_admin():
    if request.method == 'POST':
        try:
            id_admin = request.form['id_admin']
            nama = request.form['nama']
            username = request.form['username']
            query = "UPDATE admin SET nama = %s, username = %s WHERE id_admin = %s"
            config.db_cursor.execute(query, (nama, username, id_admin))
            config.db_connection.commit()
            flash('Update data berhasil', 'success')
            return redirect(url_for('akun'))
        except Exception as e:
            print(f'ini error: {str(e)}')
            config.db_connection.rollback()
            flash(f'Gagal memperbarui data: {str(e)}', 'error')
            return redirect(url_for('akun'))
    return redirect(url_for('akun'))

@app.route('/admin/hapus-admin', methods=['GET', 'POST'])
def delete_admin():
    if request.method == 'POST':
        try:
            id_admin = request.form['id_admin']
            query = "DELETE FROM admin WHERE id_admin = %s"
            config.db_cursor.execute(query, (id_admin,))
            config.db_connection.commit()
            flash('Hapus data berhasil', 'success')
            return redirect(url_for('akun'))
        except Exception as e:
            print(f'ini error: {str(e)}')
            config.db_connection.rollback()
            flash(f'Gagal menghapus data: {str(e)}', 'error')
            return redirect(url_for('akun'))
    return redirect(url_for('akun'))