from flask import Flask, render_template, request, redirect, session, url_for, Response, flash
from werkzeug.utils import secure_filename
from main import app
from get_data import *
import hashlib
import os
import date
import face_utils
import config
import cv2

@app.route('/')
def index():
    return render_template('user/login.html')

# Halaman login
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Menggunakan hashlib untuk menghash password dengan MD5
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        # Lakukan query ke database untuk mencari user dengan username dan password tertentu
        query = "SELECT * FROM users WHERE username = %s AND password = %s"
        config.db_cursor.execute(query, (username, hashed_password))
        user = config.db_cursor.fetchone()

        if user:
            # Ambil nilai id_users dari hasil kueri
            id_users = user['id_users']
            session['id_users'] = id_users
            flash('Berhasil Login', 'success')
            return redirect(url_for('home'))
        else:
            error='Username atau Password salah'

    return render_template('user/login.html', error=error)


# Halaman pertama registrasi untuk informasi umum pengguna
@app.route('/register', methods=['GET', 'POST'])
def register():
    positions = get_positions()
    shifts = get_shift()
    if request.method == 'POST':
        employees_code = request.form['employees_code']
        name = request.form['name']
        email = request.form['employees_email']
        id_position = request.form['id_position']
        id_shift = request.form['id_shift']
        username = request.form['username']
        password = request.form['password']

        
        if employees_code and name and email and id_position and id_shift and username and password:
            session['employees_code'] = employees_code
            session['name'] = name
            session['employees_email'] = email
            session['id_position'] = id_position
            session['id_shift'] = id_shift
            session['username'] = username
            session['password'] = password

            return redirect(url_for('face_register'))  # Redirect ke proses pendaftaran wajah

    return render_template('user/register.html', positions=positions, shifts=shifts)

@app.route('/forgot')
def forgot():
    return render_template('user/forgot.html')

# Halaman logout
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

# Halaman home setelah login berhasil
@app.route('/home')
def home():
    if 'id_users' in session:
        id_users = session.get('id_users')

        # Lakukan kueri ke database untuk mendapatkan nama dan id_employees dari tabel employees
        query = "SELECT * FROM employees WHERE id_users = %s"
        config.db_cursor.execute(query, (id_users,))
        result = config.db_cursor.fetchone()

        if result:
            name = result['name']
            id_employees = result['id_employees']
            employees_code = result['employees_code']
            photo = result['photo']
            today = date.tanggal_sekarang
            presence = get_one_presence(id_employees, today)

            #jangan merubah ini
            sql = "SELECT * FROM presence WHERE id_employees = %s ORDER BY id_presence DESC LIMIT 6"
            config.db_cursor.execute(sql, (id_employees,))
            rekaps = config.db_cursor.fetchall()

            return render_template('user/home.html', name=name, employees_code=employees_code, photo=photo, salam=date.waktu, tahun=date.tahun_sekarang, presence=presence, array_bulan=date.array_bulan, bulan=date.bulan, rekaps=rekaps)
        else:
            presence = None  # Atur presence menjadi None jika tidak ada data absen
            
            return render_template('user/home.html', name="", employees_code="", salam="", tahun="", presence=presence, array_bulan="", bulan="")

    else:
        return redirect(url_for('login'))


@app.route('/video_feed')
def video_feed():
    return Response(face_utils.generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/capture', methods=['POST'])
def capture():
    if 'id_users' in session:
        id_users = session.get('id_users')

        # Ambil informasi karyawan dari database
        query = "SELECT id_employees, name FROM employees WHERE id_users = %s"
        config.db_cursor.execute(query, (id_users,))
        result = config.db_cursor.fetchone()

        if result:
            name = result['name']
            id_employees = result['id_employees']
            success, frame = face_utils.camera.read()

            if request.method == 'POST':
                presence_date = date.tanggal_sekarang
                time = request.form.get('time')
                koordinat = request.form.get('koordinat')

                if success:
                    upload_path = os.path.join('static', 'uploads')
                    image_filename = f"{name}_{date.tanggal_sekarang}_{date.waktu}.jpg"
                    image_path = os.path.join(upload_path, image_filename)

                    try:
                        cv2.imwrite(image_path, frame)
                        person_name = face_utils.detect_and_recognize_faces(image_path)

                        if person_name != name:
                            flash("Absen gagal!", "error")
                        else:
                            sql = "SELECT id_employees, time_in, time_out FROM presence WHERE id_employees=%s AND presence_date=%s"
                            config.db_cursor.execute(sql, (id_employees, presence_date,))
                            result_absen = config.db_cursor.fetchone()

                            if result_absen:
                                if result_absen['time_out'] != "00:00:00":
                                    # Sudah absen masuk dan absen pulang
                                    flash(f"Anda sudah melakukan absen masuk dan pulang hari ini {person_name}!", "warning")
                                else:
                                    # Sudah absen masuk tetapi belum absen pulang
                                    update_query = "UPDATE presence SET time_out = %s, picture_out = %s, koordinat_out = %s WHERE id_employees = %s AND presence_date = %s"
                                    config.db_cursor.execute(update_query, (time, image_path, koordinat, id_employees, presence_date,))
                                    # Commit perubahan ke database
                                    config.db_connection.commit()
                                    flash(f"Absen Pulang berhasil {person_name}!", "success")
                            else:
                                # Belum absen masuk
                                check_existing_query = "SELECT * FROM presence WHERE id_employees = %s AND presence_date = %s"
                                config.db_cursor.execute(check_existing_query, (id_employees, presence_date,))
                                existing_result = config.db_cursor.fetchone()

                                if existing_result:
                                    # Sudah ada data absen tapi kosong (kasus yang tidak seharusnya terjadi)
                                    flash("Data absen kosong", "error")
                                else:
                                    # Absen masuk
                                    add_in = "INSERT INTO presence (id_employees, presence_date, time_in, time_out, picture_in, id_present, koordinat_in) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                                    config.db_cursor.execute(add_in, (id_employees, presence_date, time, '00:00:00', image_path, '1', koordinat,))
                                    # Commit perubahan ke database
                                    config.db_connection.commit()
                                    flash(f"Absen Masuk berhasil {person_name}!", "success")

                            return redirect(url_for('home'))


                        # Commit perubahan ke database
                        # config.db_connection.commit()
                    except Exception as e:
                        print(f'error: {str(e)}')
                        flash(f"Error: {str(e)}", "error")
                        # Lakukan penanganan kesalahan, seperti rollback transaksi atau log kesalahan
                        config.db_connection.rollback()
                else:
                    flash("Gagal mengambil gambar", "errorr")
            else:
                flash("Metode Permintaan Tidak Valid", "errorr")
        else:
            flash("Informasi Karyawan Tidak Ditemukan", "errorr")

    return redirect(url_for('absen'))




@app.route('/face_register', methods=['GET', 'POST'])
def face_register():
    error = None
    if 'name' in session:
        employees_code = session.get('employees_code')
        name = session.get('name')
        email = session.get('employees_email')
        id_position = session.get('id_position')
        id_shift = session.get('id_shift')
        username = session.get('username')
        password = session.get('password')

        if request.method == 'POST':
            try:
                success, frame = face_utils.camera.read()
                if success:
                    upload_path = os.path.join('static', 'uploads')
                    image_filename = f"{name}_{date.tanggal_sekarang}.jpg"
                    image_path = os.path.join(upload_path, image_filename)
                    cv2.imwrite(image_path, frame)

                    # Lakukan operasi database untuk menyimpan data pengguna ke tabel users
                    insert_user_query = "INSERT INTO users (email, username, password) VALUES (%s, %s, %s)"
                    config.db_cursor.execute(insert_user_query, (email, username, hashlib.sha256(password.encode()).hexdigest()))
                    config.db_connection.commit()

                    # Ambil id_users yang baru saja dimasukkan (gunakan lastrowid)
                    id_users = config.db_cursor.lastrowid

                    # Simpan informasi karyawan ke dalam tabel employees menggunakan id_users yang telah ada
                    insert_employee_query = "INSERT INTO employees (id_users, employees_code, name, id_position, id_shift) VALUES (%s, %s, %s, %s, %s)"
                    config.db_cursor.execute(insert_employee_query, (id_users, employees_code, name, id_position, id_shift))
                    config.db_connection.commit()

                    id_employees = config.db_cursor.lastrowid
                    face_utils.detect_faces(image_path, id_employees)

                    session['id_users'] = id_users
                    # # Flash message ketika data berhasil disimpan
                    # flash('Data berhasil disimpan!')
                    return redirect(url_for('home'))

            except Exception as e:
                # Jika terjadi kesalahan saat penyimpanan data
                error = f'Gagal menyimpan data: {str(e)}'
                # Lakukan penanganan kesalahan, seperti rollback transaksi atau log kesalahan
                config.db_connection.rollback()
                # Kembali ke halaman yang sama atau halaman lain yang sesuai dengan aplikasi Anda
                # return redirect(url_for('register'))

    return render_template('user/face.html', error=error)


@app.route('/absen', methods=['GET', 'POST'])
def absen():
    if 'id_users' in session:
        id_users = session.get('id_users')

        # Lakukan kueri ke database untuk mendapatkan nama dan id_employees dari tabel employees
        query = "SELECT * FROM employees WHERE id_users = %s"
        config.db_cursor.execute(query, (id_users,))
        result = config.db_cursor.fetchone()

        if result:
            name = result['name']
            employees_code = result['employees_code']
            photo = result['photo']

            return render_template('user/absent.html', tanggal=date.tanggal_terformat, name=name, employees_code=employees_code, photo=photo, salam=date.waktu)
        else:
            # Jika nama tidak ditemukan, beri respons yang sesuai
            return "Name not found in database"
    else:
        return redirect(url_for('login'))

    

@app.route('/cuty', methods=['GET', 'POST'])
def cuty():
    if 'id_users' in session:
        id_users = session.get('id_users')

        query = "SELECT * FROM employees WHERE id_users = %s"
        config.db_cursor.execute(query, (id_users,))
        result = config.db_cursor.fetchone()
        if result:
            name = result['name']
            employees_code = result['employees_code']
            id_employees = result['id_employees']
            photo = result['photo']
            cutys = get_employees_cuty(id_employees)
            if request.method == 'POST':
                start_date = request.form.get('start_date')
                end_date = request.form.get('end_date')

                # Jika start_date kosong, isi dengan tanggal_sekarang
                if not start_date:
                    start_date = date.tanggal_sekarang

                if 'clear_button' in request.form:  # Tombol 'Clear' ditekan
                    # Ambil semua data presensi tanpa filter tanggal
                    cutys = get_employees_cuty(id_employees)
                else:  # Tombol 'Tampilkan' ditekan
                    cutys = get_date_cuty(id_employees, start_date, end_date)

                return render_template('user/cuty.html', name=name, id_employees=id_employees, photo=photo, tanggal_sekarang=date.tanggal_sekarang, employees_code=employees_code, cutys=cutys)

            # Jika method GET, tampilkan semua data presensi tanpa filter tanggal
            cutys = get_employees_cuty(id_employees)
            tanggal_sekarang = date.tanggal_sekarang
            return render_template('user/cuty.html', name=name, id_employees=id_employees, photo=photo, tanggal_sekarang=tanggal_sekarang, employees_code=employees_code, cutys=cutys)
        return render_template('user/cuty.html')
    else:
        return redirect(url_for('login'))

@app.route('/add-cuty', methods=['GET', 'POST'])
def add_cuty():
    if request.method == 'POST':
        try:
            id_employees = request.form['id_employees']
            cuty_start = request.form['cuty_start']
            cuty_end = request.form['cuty_end']
            date_work = request.form['date_work']
            cuty_description = request.form['cuty_desc']

            query = "INSERT INTO cuty (id_employees, cuty_start, cuty_end, date_work, cuty_description, cuty_status) VALUES (%s, %s, %s, %s, %s, 'menunggu')"
            config.db_cursor.execute(query, (id_employees, cuty_start, cuty_end, date_work, cuty_description))
            config.db_connection.commit()
            flash('Berhasil menambahkan cuti', 'success')
            return redirect(url_for('cuty'))
        except Exception as e:
            config.db_connection.rollback()
            flash(f'Gagal menambah cuti {str(e)}', 'error')
            return redirect(url_for('cuty'))
    
    return redirect(url_for('cuty'))

@app.route('/update-cuty', methods=['POST'])
def update_cuty():
    if request.method == 'POST':
        try:
            id_cuty = request.form['id_cuty']
            id_employees = request.form['id_employees']
            cuty_start = request.form['cuty_start']
            cuty_end = request.form['cuty_end']
            date_work = request.form['date_work']
            cuty_description = request.form['cuty_desc']

            # Debugging: Periksa nilai-nilai yang akan digunakan dalam query
            print(f'id_cuty: {id_cuty}, id_employees: {id_employees}, cuty_start: {cuty_start}, cuty_end: {cuty_end}, date_work: {date_work}, cuty_description: {cuty_description}')

            # Pastikan koneksi ke database telah diinisialisasi dengan benar sebelum menjalankan query
            query = "UPDATE cuty SET cuty_start = %s, cuty_end = %s, date_work = %s, cuty_description = %s WHERE id_cuty = %s AND id_employees = %s"
            config.db_cursor.execute(query, (cuty_start, cuty_end, date_work, cuty_description, id_cuty, id_employees))
            config.db_connection.commit()

            flash('Berhasil memperbarui cuti', 'success')
            return redirect(url_for('cuty'))
        except Exception as e:
            config.db_connection.rollback()
            print(f'error : {str(e)}')
            flash(f'Gagal memperbarui cuti {str(e)}', 'error')
            return redirect(url_for('cuty'))

    # Jika permintaan bukan POST, redirect ke halaman cuty
    return redirect(url_for('cuty'))


@app.route('/history', methods=['GET', 'POST'])
def history():
    if 'id_users' in session:
        id_users = session.get('id_users')

        # Lakukan kueri ke database untuk mendapatkan informasi pengguna
        query = "SELECT * FROM employees WHERE id_users = %s"
        config.db_cursor.execute(query, (id_users,))
        result = config.db_cursor.fetchone()
        if result:
            name = result['name']
            employees_code = result['employees_code']
            id_employees = result['id_employees']
            photo = result['photo']
            presence_status = get_presence_status()

            # Jika method POST (saat tombol 'Tampilkan' atau 'Clear' ditekan)
            if request.method == 'POST':
                start_date = request.form.get('start_date')
                end_date = request.form.get('end_date')

                # Jika start_date kosong, isi dengan tanggal_sekarang
                if not start_date:
                    start_date = date.tanggal_sekarang

                if 'clear_button' in request.form:  # Tombol 'Clear' ditekan
                    # Ambil semua data presensi tanpa filter tanggal
                    presences = get_presence_employees(id_employees)
                else:  # Tombol 'Tampilkan' ditekan
                    presences = get_date_presence(id_employees, start_date, end_date)

                return render_template('user/history.html', tanggal_sekarang=date.tanggal_sekarang, name=name, photo=photo, employees_code=employees_code, presence_status=presence_status, presences=presences)

            # Jika method GET, tampilkan semua data presensi tanpa filter tanggal
            presences = get_presence_employees(id_employees)
            tanggal_sekarang = date.tanggal_sekarang
            return render_template('user/history.html', tanggal_sekarang=tanggal_sekarang, name=name, photo=photo, employees_code=employees_code, presence_status=presence_status, presences=presences)

        return render_template('user/history.html')
    else:
        return redirect(url_for('login'))



@app.route('/history-update', methods=['GET', 'POST'])
def history_update():
    if request.method == 'POST':
        id_presence = request.form['id_presence']
        present = request.form['id_present']
        keterangan = request.form['keterangan']
        try:
            query = 'UPDATE presence SET id_present = %s, keterangan = %s WHERE id_presence = %s'
            config.db_cursor.execute(query, (present, keterangan, id_presence))
            config.db_connection.commit()
            flash('Berhasil update absen', 'success')
            return redirect(url_for('history'))
        except Exception as e:
            config.db_connection.rollback()
            flash(f'Gagal update absen {str(e)}', 'error')
            return redirect(url_for('history'))
    return redirect(url_for('history'))

@app.route('/profile')
def profile():
    if 'id_users' in session:
        id_users = session.get('id_users')
        query = "SELECT * FROM employees WHERE id_users = %s"
        config.db_cursor.execute(query, (id_users,))
        result = config.db_cursor.fetchone()

        if result:
            id_employees = result['id_employees']
            employees_code = result['employees_code']
            name = result['name']
            photo = result['photo']
            id_position = get_position_name(id_employees)
            positions = get_positions()
            id_shift = get_shift_name(id_employees)
            shifts = get_shift()
            return render_template('user/profile.html',id_users=id_users, id_employees=id_employees, employees_code=employees_code, name=name, photo=photo, positions=positions, id_position=id_position, shifts=shifts, id_shift=id_shift)
    else:
        return redirect(url_for('login'))
    
@app.route('/update-profile', methods=['GET', 'POST'])
def update_profile():
    if request.method == 'POST':
        try:
            id_employees = request.form['id_employees']
            code = request.form['code']
            name = request.form['name']
            position = request.form['id_position']
            shift = request.form['id_shift']

            query = "UPDATE employees SET employees_code=%s, name=%s, id_position=%s, id_shift=%s WHERE id_employees=%s"
            config.db_cursor.execute(query, (code, name, position, shift, id_employees))
            config.db_connection.commit()
            flash('Update data berhasil', 'success')
            return redirect(url_for('profile'))
        except Exception as e:
            print(f'ini error: {str(e)}')
            config.db_connection.rollback()  # Rollback perubahan jika ada kesalahan dalam query
            flash(f'Gagal memperbarui data: {str(e)}', 'error')
            return redirect(url_for('profile'))
    return redirect(url_for('profile'))  # Menggunakan url_for() untuk melakukan redirect ke endpoint 'profile'

    
@app.route('/update-foto', methods=['GET', 'POST'])
def update_foto():
    if request.method == 'POST':
        try:
            id_employees = request.form['id_employees']
            picture = request.files['file']

            if picture.filename != '':
                filename = secure_filename(picture.filename)
                picture.save(os.path.join('static/photo', f"{id_employees}.png"))  # Simpan gambar dengan nama sesuai id_employees

                query = "UPDATE employees SET photo = %s WHERE id_employees = %s"
                config.db_cursor.execute(query, (f"{id_employees}.png", id_employees))
                config.db_connection.commit()
                flash('Berhasil Update Foto', 'success')
                return redirect(url_for('profile'))
            else:
                flash('Tidak ada file yang diunggah', 'error')
        except Exception as e:
            print(f'Error: {str(e)}')
            config.db_connection.rollback()
            flash(f'Gagal memperbarui foto: {str(e)}', 'error')

    return redirect(url_for('profile'))

@app.route('/update-password', methods=['GET', 'POST'])
def update_password():
    if request.method == 'POST':
        try:
            id_users = request.form['id_users']
            new_password = request.form['new_password']
            query = 'UPDATE users SET password = %s WHERE id_users = %s'
            config.db_cursor.execute(query,(hashlib.sha256(new_password.encode()).hexdigest(), id_users))
            config.db_connection.commit()
            flash('Berhasil memperbarui password', 'success')
            return redirect(url_for('profile'))
        except Exception as e:
            config.db_connection.rollback()
            flash(f'Gagal memperbarui password {str(e)}', 'error')
    return redirect(url_for('profile'))