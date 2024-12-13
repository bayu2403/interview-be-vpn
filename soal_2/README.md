## PREP
1. install dependecies
> pip install -r requirements.txt
2. migrate db
> python manage.py makemigrations && python manage.py migrate 
3. run docker compose, to run vault and run write_secret to store secret in vault
> docker compose up
> python write_secret.py    
4. hapus .example pada .env.example, untuk digunakan sebagai .env file  
5. run seed.py
> seed.py

## TEST
1. run sso
> cd sso
> python manage.py runserver

2. run client
> cd client_1
> python manage.py runserver 8081

3. generate token
> curl --location 'http://localhost:8000/auth/token/' \
--form 'username="user1"' \
--form 'password="password1"'

![Screenshot](https://github.com/bayu2403/interview-be-vpn/blob/main/soal_2/image/auth_token.png)

4. hit client 1 api
> curl --location --request POST 'http://localhost:8081/validate-jwt/' \
--header 'Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzM0MTU5Mzc2LCJpYXQiOjE3MzQwNzI5NzYsImp0aSI6IjE0NzFjMzUwZGYxNjQ1ZTdhZjE3MDUzYzFkYjBhZGRmIiwidXNlcl9pZCI6MX0.QM3UvyOu8-pUWDLkkUHkDp8ue52ud5SOYSWbdRECyrNJG-vT_wQiizlVlcUa1x5ItlXdfbZ_oo27__-dV6fdUYZJZZPtcLr_MPHdoF2p2_xJ8STpqEnPs53jYD_LCU-Ks7g9uY8MpDUuf6iLs7mUZmXQQdSx24poVcDYcaMBSpVGTBHI5VZVRV_j8KkuhFaNnbLt3FIMqbC3aKZdWQTOXP0h-0TPLT2PYfvOd4SML-mR62XFpul8OR7XxB1QbeJRqs0UOojw6EGg5mJR41282eqjCr9uu0XKmkmXBASKU_dFoSJQUQWgGpKvbHLmWZtPoworusayomRdvUOC0vg82g'

![Screenshot](https://github.com/bayu2403/interview-be-vpn/blob/main/soal_2/image/validate_jwt.png)


5. refresh token
> curl --location 'http://localhost:8000/auth/refresh/' \
--form 'refresh_token="eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczNDY3NzY3MCwiaWF0IjoxNzM0MDcyODcwLCJqdGkiOiJjZjA0NTUxNGNkNTg0N2FmYTQ4OWUyZTk1M2NiNmZkNyIsInVzZXJfaWQiOjF9.B9AruZ9t0RnqMZguGIpDFHlQ_jG5pMWkLFEHVKlEQ6t3qQ2zriQbgP_ambN0r562DeGxpbkQQQ9zGJDEB8LqqptxX03s0M8GEeH7Hlq3LahJ0RaCS_EuNpznxMIJiOlg_dEN5vVgmqGq-E4yOFbNPELdRM4EC5USTNCw4U0UndZ31qQENt3WkEh2ClpDPm8cH2_Lz6d3zvaeOBAvmCGYh9KCPZuUQCFhPEn3dr5bydYgXZTfIPJGnrhmR0HqSzkiP8DTg96BPPpYW4FZGlzzyN_GIjhcuTH2A5ERSQnH61zff73U0t8v2RivGWVbALSmL6F2PNSwtSwfzFlK3xyiMQ"' 

![Screenshot](https://github.com/bayu2403/interview-be-vpn/blob/main/soal_2/image/refresh_token.png)

## Explanation
JWT signed menggunakan private dan public key, untuk menggenerate private dan public key bisa menggunakan
> openssl genrsa -out private.key 2048

> openssl rsa -in private.key -pubout -out public.key

Menggunakan private key dan public key dibandingkan secret key untuk menandatangani JWT dilakukan karena Private key hanya ada di server SSO untuk menandatangani token, sementara public key digunakan layanan lain untuk memvalidasi token. Kalau public key bocor, token tetap aman karena tidak bisa digunakan untuk menandatangani token baru. Sebaliknya, kalau secret key bocor, siapa pun bisa membuat token palsu.

![Screenshot](https://github.com/bayu2403/interview-be-vpn/blob/main/soal_2/image/jwt.png)