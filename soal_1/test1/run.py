import threading
from grpc_server_run import start_grpc_server  # Fungsi untuk memulai gRPC server
from uvicorn import run as uvicorn_run

def start_uvicorn():
    uvicorn_run("test1.asgi:application", host="0.0.0.0", port=8001)

if __name__ == "__main__":
    grpc_thread = threading.Thread(target=start_grpc_server)
    uvicorn_thread = threading.Thread(target=start_uvicorn)

    grpc_thread.start()
    uvicorn_thread.start()

    grpc_thread.join()
    uvicorn_thread.join()
