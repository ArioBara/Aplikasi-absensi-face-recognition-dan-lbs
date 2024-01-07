import mysql.connector

# Konfigurasi koneksi ke MySQL
db_connection = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',  # Isi dengan password database Anda
    database='db_absensi'
)

# Buat kursor untuk melakukan operasi database
db_cursor = db_connection.cursor(dictionary=True)
