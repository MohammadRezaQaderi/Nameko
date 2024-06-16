import grpc
import notif_pb2
import notif_pb2_grpc


def run():
    channel = grpc.insecure_channel('localhost:50051')
    stub = notif_pb2_grpc.notifStub(channel)
    if hasattr(stub, 'unary_unary'):
        try:
            response = stub.unary_unary(notif_pb2.ExampleRequest(value='test', multiplier=1))
            print("Response from unary_unary: ", response)
        except grpc.RpcError as e:
            print("RPC failed: ", e)
    else:
        print("Method unary_unary does not exist on notifStub")

    users = [
        notif_pb2.User(name='John Doe', national_id='123456789', phone='09216272502'),
        notif_pb2.User(name='Jane Doe', national_id='987654321', phone='09122985393')
    ]
    request = notif_pb2.MessageToUsersRequest(message='Hello, users!', users=users)
    response = stub.SendMessageToUsers(request)
    print("Response from SendMessageToUsers: ", response.response)

    # request to get users
    national_id = '12346789'
    request = notif_pb2.NationalIdRequest(national_id=national_id)
    response = stub.GetUsersByNationalId(request)
    print("Response from GetUsersByNationalId: ", response.users)


if __name__ == '__main__':
    run()
