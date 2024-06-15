import grpc
import notif_pb2
import notif_pb2_grpc

def run():
    channel = grpc.insecure_channel('localhost:50051')
    stub = notif_pb2_grpc.exampleStub(channel)
    response = stub.unary_unary(notif_pb2.ExampleRequest(value='test', multiplier=1))
    print("Response from unary_unary: ", response)

    responses = stub.unary_stream(notif_pb2.ExampleRequest(value='test', multiplier=1))
    print("Responses from unary_stream:")
    for response in responses:
        print(response)
    def request_iterator():
        for i in range(3):
            yield notif_pb2.ExampleRequest(value=f'test {i}', multiplier=i)

    response = stub.stream_unary(request_iterator())
    print("Response from stream_unary: ", response)

    responses = stub.stream_stream(request_iterator())
    print("Responses from stream_stream:")
    for response in responses:
        print(response)

    users = [
        notif_pb2.User(name='John Doe', nationalid='123456789'),
        notif_pb2.User(name='Jane Doe', nationalid='987654321')
    ]
    request = notif_pb2.MessageToUsersRequest(message='Hello, users!', users=users)

    # Call the SendMessageToUsers method
    response = stub.SendMessageToUsers(request)
    print("Response from SendMessageToUsers: ", response.status)
if __name__ == '__main__':
    run()
