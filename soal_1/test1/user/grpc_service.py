from user_proto import user_pb2
from user.models import User
from user_proto import user_pb2_grpc
from datetime import datetime

class UserService(user_pb2_grpc.UserServiceServicer):
    def GetUsers(self, request, context):
        print(f"{datetime.now().isoformat()} - there is a gRPC request")
        users = User.objects.all()
        user_list = [
            user_pb2.User(
                id=user.id,
                firstname=user.firstname,
                lastname=user.lastname,
                nickname=user.nickname,
                date_of_birth=str(user.date_of_birth),
                is_active=user.is_active,
            )
            for user in users
        ]
        return user_pb2.UserList(users=user_list)