# Aplikasi absensi face recognition dan lbs
 
## Cara menggunakan
1. Clone project dari github
   <br>
   ketikan perintah beikut:
   https://github.com/ArioBara/Aplikasi-absensi-face-recognition-dan-lbs.git
2. masuk ke direktori project
   ketikan perintah berikut
   cd Aplikasi-absensi-face-recognition-dan-lbs
3. Buat virtual environment ketikan perintah berikut:
   - Windows
     python -m venv .venv
     kemudian:
     .venv/Script/active
   - Linux/Mac
     python3 -m venv .venv
     kemudian:
     source .venv/bin/activate
4. Instal modul yang perlukan ketikan perintah berikut:
   pip install -r requirements.txt
5. Import database db_absensi
6. Jalankan aplikasi
   ketikan perintah berikut:
   python app.py
7. Buka browser ketikan url berikut: http://localhost:5000
8. untuk masuk halaman admin ketikan ulr berikut: http://localhost:5000/admin/login
   -username: admin
   -password: admin123

<i>Note :</i>
* perlu cmake dan desktop develompment c++ untuk menginstal modul dlib
