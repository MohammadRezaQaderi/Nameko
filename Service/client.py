from nameko.standalone.rpc import ClusterRpcProxy
from datetime import datetime


class ServiceClient:
    def __init__(self, config):
        self.config = config

    def call_hello(self, phone):
        with ClusterRpcProxy(self.config) as rpc:
            result = rpc.service1.hello(phone)
            print("Hello Result:", result)

    def call_create(self, phone, status):
        data = {
            'phone': phone,
            'status': status,
            'create_date_time': datetime.utcnow().isoformat(),
            'edit_date_time': datetime.utcnow().isoformat()
        }
        with ClusterRpcProxy(self.config) as rpc:
            result = rpc.service1.create(data)
            print("Create Result:", result)


if __name__ == "__main__":
    config = {
        'AMQP_URI': "pyamqp://guest:guest@rabbitmq"
    }
    client = ServiceClient(config)
    client.call_hello('1234567890')  # Example phone number
    client.call_create('9876543210', 'success')  # Example phone number and status
