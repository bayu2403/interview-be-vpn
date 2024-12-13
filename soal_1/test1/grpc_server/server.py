import os
import django
import grpc
from concurrent import futures

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "test1.settings")
django.setup()

from user.grpc_service import UserService
from user_proto import user_pb2_grpc

def start_grpc_server():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    user_pb2_grpc.add_UserServiceServicer_to_server(UserService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("gRPC server started at port 50051...")
    server.wait_for_termination()