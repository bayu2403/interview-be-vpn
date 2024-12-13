## PREP
1. install dependecies
> pip install -r requirements.txt
2. migrate db
> python manage.py makemigrations && python manage.py migrate 
3. run docker compose, to run vault and run write_secret to store secret in vault
> docker compose up
> python write_secret.py    
4. hapus .example pada .env.example, untuk digunakan sebagai .env file  

## Test
1. run django service
> python manage.py runserver
2. create user first
> curl --location 'http://localhost:8000/user/v1/create-user/' \
--header 'Content-Type: application/json' \
--data '{
    "username":"user3",
    "password":"pass3",
    "project_name":"PROJECT_2"
}'

![Screenshot](https://github.com/bayu2403/interview-be-vpn/blob/main/soal_3/sso/image/create_user.png)

response
```
{"status": "success", "message": "User created successfully."}
```

3. validate user 
> curl --location 'http://localhost:8000/user/v1/validate-user/' \
--header 'Content-Type: application/json' \
--data '{
    "username":"user3",
    "password":"pass3",
    "project_name":"PROJECT_2"
}'

![Screenshot](https://github.com/bayu2403/interview-be-vpn/blob/main/soal_3/sso/image/validate_user.png)

response
```
{
    "status": "success",
    "message": "Password validated successfully."
}
```

## Explanation
### Save user ke table
Table `CustomUser` menambahkan kolom baru `project_name`, untuk membedakan password user tersebut di hash menggunakan secret key dari project yang mana.

Endpoint `create-user` membutuhkan field `project_name` sebagai referensi secret key yang akan digunakan untuk `hash` password.

Sedangkan endpoint `validate-user` membutuhkan field `project_name` sebagai referensi secret key yang akan digunakan untuk `validasi` hash password.

### Vault (hashicorp/vault)
Secret key disimpan di dalam ***Vault***, di mana ***Vault*** berperan sebagai tempat penyimpanan secret key yang terpusat dan aman.

Ketika membuat user dan menyimpan atau memverifikasi password, fungsi CustomPBKDF2PasswordHasher akan mengambil secret dari Vault dan meng-hash password sebelum disimpan dan sebelum dibandingkan (compare).

Menggunakan ***Vault*** dibandingkan dengan .env biasa memberikan beberapa keuntungan:

- Keamanan yang Lebih Tinggi: ***Vault*** mengenkripsi data secara otomatis dan menyediakan kontrol akses yang lebih ketat, mengurangi risiko kebocoran rahasia jika dibandingkan dengan file .env yang dapat diakses siapa saja yang memiliki akses ke server.

- Manajemen Terpusat: ***Vault*** memungkinkan pengelolaan secret key secara terpusat untuk seluruh aplikasi.

- Audit dan Pelacakan: Vault menyediakan audit logs untuk melacak akses dan perubahan rahasia, memastikan bahwa semua aktivitas tercatat dengan baik, yang tidak dapat dilakukan oleh .env.

Selain menggunakan ***Vault*** juga dapat menggunakan ***AWS Secret***.

### Penjelasan Cara Kerja Hash Password dan Penggunaan PBKDF2

Proses hashing password adalah cara untuk mengubah password asli menjadi bentuk yang tidak dapat dibaca (hashed). Hashing ini dilakukan untuk memastikan bahwa data password yang disimpan di database tidak mudah diakses atau dihack. Ketika user membuat akun atau mengubah password, sistem akan melakukan hashing pada password yang dimasukkan menggunakan algoritma tertentu, seperti PBKDF2. Hasil dari hashing ini adalah nilai yang disebut dengan "hash", yang disimpan di database. Saat pengguna mencoba login, password yang dimasukkan akan di-hash kembali dan dibandingkan dengan hash yang tersimpan di database. Jika keduanya cocok, maka pengguna dianggap berhasil login.

Alasan penggunaan PBKDF2 (Password-Based Key Derivation Function 2) pada sistem Anda adalah karena PBKDF2 dirancang untuk memperlambat proses hashing password dengan menggunakan sejumlah besar iterasi. Hal ini membuat serangan brute force atau serangan lainnya menjadi lebih sulit dilakukan. PBKDF2 bekerja dengan cara mengulangi proses hashing password dengan menggunakan salt (nilai acak yang ditambahkan pada password) berulang kali. Semakin banyak iterasi yang digunakan, semakin kuat dan sulit untuk membongkar password yang di-hash tersebut. Selain itu, PBKDF2 memiliki keunggulan dalam hal kompatibilitas dan dukungan luas di banyak platform dan bahasa pemrograman. Akan sangat sulit bagi penyerang (hacker) untuk membalikkan hash tersebut kembali menjadi password asli.

