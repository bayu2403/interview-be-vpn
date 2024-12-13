## PREP
1. install dependecies
> pip install -r requirements.txt
2. migrate db
> python manage.py makemigrations && python manage.py migrate 
3. run seed untuk populate db untuk pertamakali run
> python seed.py  
4. generate file proto, pada repo ini hasil generate file proto sudah disertakan
> python -m grpc_tools.protoc --proto_path=./protos --python_out=./ --grpc_python_out=./ ./protos/user_proto/user.proto
5. run grpc server
> python grpc_server_run.py
6. run django menggunakan uvicorn
> uvicorn test1.asgi:application --host 0.0.0.0 --port 8001


## TEST
1. endpoint v1/users/
> curl --location 'http://localhost:8001/api/v1/users/'


![Screenshot](https://github.com/bayu2403/interview-be-vpn/blob/main/soal_1/test1/image/users.png)

2. grpc
- import file .proto di postman, lalu hit dengan postman.
- localhost:50051, GetUsers

![Screenshot](https://github.com/bayu2403/interview-be-vpn/blob/main/soal_1/test1/image/grpc_user.png)


## Code
Struktur code:
```
test1/
├── grpc_server/
│   └── server.py
├── protos/
│   └── user_proto/
│       └── user.proto
├── test1/
│   └── asgi.py
├── user/
│   ├── grpc_service.py
│   ├── models.py
│   ├── serializer.py
│   └── views.py
├── user_proto/
│  ├── user_pb2_grpc.py
│  └── user_pb2.py
├── manage.py
└── seed.py
```

### Penjelasan

- **`grpc_server/`**:.
  - `server.py`: Untuk start gRPC server.

- **`protos/`**: Berisi definisi Protocol Buffers.
  - `user_proto/user.proto`: File proto untuk user.

- **`test1/`**:
  - `asgi.py`: Konfigurasi ASGI untuk aplikasi. Default django menggunakan WSGI, untuk itu dibutuhkan `django.core.asgi import get_asgi_application` untuk menjalankan django dalam ASGI menggunakan **Uvicorn**.

- **`user/`**:
  - `grpc_service.py`: Berisi fungsi gRPC yang digunakan untuk mengembalikan list user.
  - `models.py`: Mendefinisikan model data user.
  - `serializer.py`: Serialisasi data pengguna.

- **`user_proto/`**: Hasil generate dari file user.proto

- **`seed.py`**: Script untuk generate user.
