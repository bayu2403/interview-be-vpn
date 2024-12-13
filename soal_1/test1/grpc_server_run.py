from concurrent import futures
from grpc_server.server import start_grpc_server

def main():
    """Manually start the gRPC server."""
    print("Starting the gRPC server manually...")
    
    start_grpc_server()

if __name__ == "__main__":
    main()
