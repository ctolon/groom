# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from protos.v1 import groom_pb2 as protos_dot_v1_dot_groom__pb2


class GroomStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.RoomRegistration = channel.unary_unary(
                '/groom.Groom/RoomRegistration',
                request_serializer=protos_dot_v1_dot_groom__pb2.RoomRegistrationRequest.SerializeToString,
                response_deserializer=protos_dot_v1_dot_groom__pb2.RoomRegistrationResponse.FromString,
                )
        self.SendNewsFlash = channel.stream_unary(
                '/groom.Groom/SendNewsFlash',
                request_serializer=protos_dot_v1_dot_groom__pb2.NewsFlash.SerializeToString,
                response_deserializer=protos_dot_v1_dot_groom__pb2.NewsStreamStatus.FromString,
                )


class GroomServicer(object):
    """Missing associated documentation comment in .proto file."""

    def RoomRegistration(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SendNewsFlash(self, request_iterator, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_GroomServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'RoomRegistration': grpc.unary_unary_rpc_method_handler(
                    servicer.RoomRegistration,
                    request_deserializer=protos_dot_v1_dot_groom__pb2.RoomRegistrationRequest.FromString,
                    response_serializer=protos_dot_v1_dot_groom__pb2.RoomRegistrationResponse.SerializeToString,
            ),
            'SendNewsFlash': grpc.stream_unary_rpc_method_handler(
                    servicer.SendNewsFlash,
                    request_deserializer=protos_dot_v1_dot_groom__pb2.NewsFlash.FromString,
                    response_serializer=protos_dot_v1_dot_groom__pb2.NewsStreamStatus.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'groom.Groom', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Groom(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def RoomRegistration(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/groom.Groom/RoomRegistration',
            protos_dot_v1_dot_groom__pb2.RoomRegistrationRequest.SerializeToString,
            protos_dot_v1_dot_groom__pb2.RoomRegistrationResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SendNewsFlash(request_iterator,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.stream_unary(request_iterator, target, '/groom.Groom/SendNewsFlash',
            protos_dot_v1_dot_groom__pb2.NewsFlash.SerializeToString,
            protos_dot_v1_dot_groom__pb2.NewsStreamStatus.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
