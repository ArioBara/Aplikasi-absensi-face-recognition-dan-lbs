import datetime
import locale

# Atur lokal ke Bahasa Indonesia
locale.setlocale(locale.LC_TIME, 'id_ID')
# Mendapatkan waktu terkini
waktu_sekarang = datetime.datetime.now()
# Mendapatkan hanya bagian jam dari waktu terkini
jam_sekarang = waktu_sekarang.hour
# Menentukan waktu hariannya
if 1 <= jam_sekarang <= 9:
    waktu = "Pagi"
elif 10 <= jam_sekarang <= 15:
    waktu = "Siang"
elif 16 <= jam_sekarang <= 18:
    waktu = "Sore"
else:
    waktu = "Malam"
# mendapatkan jam
jam = waktu_sekarang.strftime("%H:%M:%S")
# Mendapatkan tanggal terkini
tanggal_sekarang = datetime.date.today()
# Menampilkan tanggal terkini dalam format tertentu (contoh: DD/MM/YYYY)
tanggal_terformat = tanggal_sekarang.strftime("%A, %d %B %Y")
# Menentukan tahun
tahun_sekarang = waktu_sekarang.year

bulan = waktu_sekarang.month

# Daftar nama bulan
array_bulan = {
        1: 'Januari',
        2: 'Februari',
        3: 'Maret',
        4: 'April',
        5: 'Mei',
        6: 'Juni',
        7: 'Juli',
        8: 'Agustus',
        9: 'September',
        10: 'Oktober',
        11: 'November',
        12: 'Desember'
    }