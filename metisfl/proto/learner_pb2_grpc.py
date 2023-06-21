# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from metisfl.proto import learner_pb2 as metisfl_dot_proto_dot_learner__pb2
from metisfl.proto import service_common_pb2 as metisfl_dot_proto_dot_service__common__pb2


class LearnerServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.EvaluateModel = channel.unary_unary(
                '/projectmetis.LearnerService/EvaluateModel',
                request_serializer=metisfl_dot_proto_dot_learner__pb2.EvaluateModelRequest.SerializeToString,
                response_deserializer=metisfl_dot_proto_dot_learner__pb2.EvaluateModelResponse.FromString,
                )
        self.GetServicesHealthStatus = channel.unary_unary(
                '/projectmetis.LearnerService/GetServicesHealthStatus',
                request_serializer=metisfl_dot_proto_dot_service__common__pb2.GetServicesHealthStatusRequest.SerializeToString,
                response_deserializer=metisfl_dot_proto_dot_service__common__pb2.GetServicesHealthStatusResponse.FromString,
                )
        self.RunTask = channel.unary_unary(
                '/projectmetis.LearnerService/RunTask',
                request_serializer=metisfl_dot_proto_dot_learner__pb2.RunTaskRequest.SerializeToString,
                response_deserializer=metisfl_dot_proto_dot_learner__pb2.RunTaskResponse.FromString,
                )
        self.ShutDown = channel.unary_unary(
                '/projectmetis.LearnerService/ShutDown',
                request_serializer=metisfl_dot_proto_dot_service__common__pb2.ShutDownRequest.SerializeToString,
                response_deserializer=metisfl_dot_proto_dot_service__common__pb2.ShutDownResponse.FromString,
                )


class LearnerServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def EvaluateModel(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetServicesHealthStatus(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def RunTask(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ShutDown(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_LearnerServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'EvaluateModel': grpc.unary_unary_rpc_method_handler(
                    servicer.EvaluateModel,
                    request_deserializer=metisfl_dot_proto_dot_learner__pb2.EvaluateModelRequest.FromString,
                    response_serializer=metisfl_dot_proto_dot_learner__pb2.EvaluateModelResponse.SerializeToString,
            ),
            'GetServicesHealthStatus': grpc.unary_unary_rpc_method_handler(
                    servicer.GetServicesHealthStatus,
                    request_deserializer=metisfl_dot_proto_dot_service__common__pb2.GetServicesHealthStatusRequest.FromString,
                    response_serializer=metisfl_dot_proto_dot_service__common__pb2.GetServicesHealthStatusResponse.SerializeToString,
            ),
            'RunTask': grpc.unary_unary_rpc_method_handler(
                    servicer.RunTask,
                    request_deserializer=metisfl_dot_proto_dot_learner__pb2.RunTaskRequest.FromString,
                    response_serializer=metisfl_dot_proto_dot_learner__pb2.RunTaskResponse.SerializeToString,
            ),
            'ShutDown': grpc.unary_unary_rpc_method_handler(
                    servicer.ShutDown,
                    request_deserializer=metisfl_dot_proto_dot_service__common__pb2.ShutDownRequest.FromString,
                    response_serializer=metisfl_dot_proto_dot_service__common__pb2.ShutDownResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'projectmetis.LearnerService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class LearnerService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def EvaluateModel(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/projectmetis.LearnerService/EvaluateModel',
            metisfl_dot_proto_dot_learner__pb2.EvaluateModelRequest.SerializeToString,
            metisfl_dot_proto_dot_learner__pb2.EvaluateModelResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetServicesHealthStatus(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/projectmetis.LearnerService/GetServicesHealthStatus',
            metisfl_dot_proto_dot_service__common__pb2.GetServicesHealthStatusRequest.SerializeToString,
            metisfl_dot_proto_dot_service__common__pb2.GetServicesHealthStatusResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def RunTask(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/projectmetis.LearnerService/RunTask',
            metisfl_dot_proto_dot_learner__pb2.RunTaskRequest.SerializeToString,
            metisfl_dot_proto_dot_learner__pb2.RunTaskResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ShutDown(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/projectmetis.LearnerService/ShutDown',
            metisfl_dot_proto_dot_service__common__pb2.ShutDownRequest.SerializeToString,
            metisfl_dot_proto_dot_service__common__pb2.ShutDownResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)