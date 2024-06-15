# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

import notif_pb2 as notif__pb2

GRPC_GENERATED_VERSION = '1.64.1'
GRPC_VERSION = grpc.__version__
EXPECTED_ERROR_RELEASE = '1.65.0'
SCHEDULED_RELEASE_DATE = 'June 25, 2024'
_version_not_supported = False

try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True

if _version_not_supported:
    warnings.warn(
        f'The grpc package installed is at version {GRPC_VERSION},'
        + f' but the generated code in notif_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
        + f' This warning will become an error in {EXPECTED_ERROR_RELEASE},'
        + f' scheduled for release on {SCHEDULED_RELEASE_DATE}.',
        RuntimeWarning
    )


class exampleStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.unary_unary = channel.unary_unary(
                '/nameko.example/unary_unary',
                request_serializer=notif__pb2.ExampleRequest.SerializeToString,
                response_deserializer=notif__pb2.ExampleReply.FromString,
                _registered_method=True)
        self.unary_stream = channel.unary_stream(
                '/nameko.example/unary_stream',
                request_serializer=notif__pb2.ExampleRequest.SerializeToString,
                response_deserializer=notif__pb2.ExampleReply.FromString,
                _registered_method=True)
        self.stream_unary = channel.stream_unary(
                '/nameko.example/stream_unary',
                request_serializer=notif__pb2.ExampleRequest.SerializeToString,
                response_deserializer=notif__pb2.ExampleReply.FromString,
                _registered_method=True)
        self.stream_stream = channel.stream_stream(
                '/nameko.example/stream_stream',
                request_serializer=notif__pb2.ExampleRequest.SerializeToString,
                response_deserializer=notif__pb2.ExampleReply.FromString,
                _registered_method=True)


class exampleServicer(object):
    """Missing associated documentation comment in .proto file."""

    def unary_unary(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def unary_stream(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def stream_unary(self, request_iterator, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def stream_stream(self, request_iterator, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_exampleServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'unary_unary': grpc.unary_unary_rpc_method_handler(
                    servicer.unary_unary,
                    request_deserializer=notif__pb2.ExampleRequest.FromString,
                    response_serializer=notif__pb2.ExampleReply.SerializeToString,
            ),
            'unary_stream': grpc.unary_stream_rpc_method_handler(
                    servicer.unary_stream,
                    request_deserializer=notif__pb2.ExampleRequest.FromString,
                    response_serializer=notif__pb2.ExampleReply.SerializeToString,
            ),
            'stream_unary': grpc.stream_unary_rpc_method_handler(
                    servicer.stream_unary,
                    request_deserializer=notif__pb2.ExampleRequest.FromString,
                    response_serializer=notif__pb2.ExampleReply.SerializeToString,
            ),
            'stream_stream': grpc.stream_stream_rpc_method_handler(
                    servicer.stream_stream,
                    request_deserializer=notif__pb2.ExampleRequest.FromString,
                    response_serializer=notif__pb2.ExampleReply.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'nameko.example', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('nameko.example', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class example(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def unary_unary(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/nameko.example/unary_unary',
            notif__pb2.ExampleRequest.SerializeToString,
            notif__pb2.ExampleReply.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def unary_stream(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(
            request,
            target,
            '/nameko.example/unary_stream',
            notif__pb2.ExampleRequest.SerializeToString,
            notif__pb2.ExampleReply.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def stream_unary(request_iterator,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.stream_unary(
            request_iterator,
            target,
            '/nameko.example/stream_unary',
            notif__pb2.ExampleRequest.SerializeToString,
            notif__pb2.ExampleReply.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def stream_stream(request_iterator,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.stream_stream(
            request_iterator,
            target,
            '/nameko.example/stream_stream',
            notif__pb2.ExampleRequest.SerializeToString,
            notif__pb2.ExampleReply.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
