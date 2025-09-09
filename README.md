Nama: Jenisa Bunga
NPM: 2406431334
Kelas: PBP F

Link Aplikasi PWS: https://pbp.cs.ui.ac.id/jenisa.bunga/stymart

Deskripsi Aplikasi:
Apk ini merupakan Football Shop sederhana bernama stymart(Shin Tae Yong mart) yang dibuat menggunakan framework Django. Apk memungkinkan pengguna untuk melihat daftar produk dengan atribut seperti nama, harga, deskripsi, kategori, gambar item dan status unggulan item.

Soal 1: Jelaskan bagaimana cara kamu mengimplementasikan checklist di atas secara step-by-step:

1. Membuat Direktori dan Mengaktifkan Virtual Environment

Buat direktori baru dengan nama STYmart dan masuk ke dalamnya

Buka CMD lalu buat virtual environment

Konfigurasi enviroment variables dan proyek -> menjalankan server -> menghentikan dan menonaktifkan

2. Buat repostiori Github bernama STYmart

Hubungkan repositori lokal dengan repositori GitHub yang telah dibuat.
Buat branch utama bernama master. Lakukan add, commit, dan push dari direktori repositori lokal. 

 Membuat Proyek Django baru

Django adalah tempat utama yang menampung seluruh aplikasi dan konfigurasi, jadi kita terlebih dahulu meng-install django dan membuat project baru

settings.py = konfigurasi utama project
urls.py = URL routing tingkat project
manage.py = command line utility untuk berinteraksi dengan project

2. Membuat aplikasi Main

Aplikasi django adalah modul yang menangani fitur spesifik dalam project

models.py = definisi struktur data
views.py = logic pemrosesan request
urls.py = URL routing tingkat app (perlu dibuat manual)

3. routing project ke aplikasi main

Routing menghubungkan URL dengan fungsi yang akan menanganinya

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
]

include memungkinkan modularitas - setiap app mengelola URL-nya sendiri

4. Membuat model product

Model adalah representasi struktur data dalam database menggunakan ORM Django

isi setiap field (characternya apa, maksimalnya berapa)
CharField = teks dengan panjang terbatas
IntegerField = Angka bilangan bulat
TextField = Teks panjang tanpa batasan
URLField = Validasi format URL otomatis
BooleanField = True/False dengan default value

5. Membuat fungsi di views.py

Views adalah controller yang memproses request dan mengembalikan response.

def show_main(request):
    context = {
        'name': 'Jenisa Bunga',
        'class': 'PBP F'
    }

    return render(request, "main.html", context)

context adalah dictionary data yang dikirim ke template
render() menggabungkan template dengan data context

6. PWS deployment 

Deployment adalah proses membawa aplikasi dari development ke production environment. 

Soal 2: Buatlah bagan yang berisi request client ke web aplikasi berbasis Django beserta responnya dan jelaskan pada bagan tersebut kaitan antara urls.py, views.py, models.py, dan berkas html.

![PBP](https://github.com/user-attachments/assets/6762644f-f0f5-440f-87e9-c514e91c519e)


Soal 3: Jelaskan peran settings.py dalam proyek Django!

settings.py adalah file konfigurasi utama dalam proyek Django yang mengatur jalannya aplikasi. Di dalamnya terdapat pengaturan penting seperti database (misalnya SQLite untuk development dan PostgreSQL untuk production), daftar aplikasi aktif (INSTALLED_APPS), middleware, template HTML, static files, timezone, bahasa, hingga aspek keamanan seperti SECRET_KEY, DEBUG, dan ALLOWED_HOSTS. Dengan adanya settings.py, Django dapat berjalan konsisten sesuai kebutuhan environment yang digunakan.


Soal 4: Bagaimana cara kerja migrasi database di Django?

Migrasi di Django adalah proses menyamakan struktur database dengan model yang didefinisikan di models.py. Setiap kali ada perubahan model, Django akan membuat file migrasi dengan perintah python manage.py makemigrations, lalu perubahan tersebut diterapkan ke database melalui python manage.py migrate. Dengan cara ini, developer tidak perlu menulis SQL manual karena Django otomatis mengelola perubahan skema, menyimpan riwayat migrasi, serta memastikan database selalu konsisten dengan model aplikasi.


Soal 5: Menurut Anda, dari semua framework yang ada, mengapa framework Django dijadikan permulaan pembelajaran pengembangan perangkat lunak?

Django dipilih sebagai permulaan pembelajaran pengembangan perangkat lunak karena lengkap, terstruktur, dan ramah pemula. Framework ini sudah menyediakan banyak fitur bawaan sehingga pemula bisa langsung fokus pada logika aplikasi. Ditambah lagi, Django berbasis Python yang sintaksnya sudah dipelajari sebelumnya, sehingga memudahkan proses belajar.



