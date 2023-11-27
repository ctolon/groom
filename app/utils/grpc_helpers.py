import logging
import grpc
import logging
import traceback

from google.protobuf.json_format import MessageToDict

import json
from typing import Dict, List
from urllib.parse import unquote

def grpc_service_conf_generator(
    list_of_services : List[Dict[str, str]] = [{}],
    timeout="30.0s",
    maxAttempts=5,
    waitForReady=True,
    initialBackoff="0.1s",
    maxBackoff="10s",
    backoffMultiplier=2,
    retryableStatusCodes=["UNAVAILABLE"]
    ) -> str:
    """gRPC Service Configuration Generator function.
    
    References:
    - https://fuchsia.googlesource.com/third_party/grpc/+/HEAD/doc/service_config.md
    - https://www.retinadata.com/blog/configuring-grpc-retries/
    - https://stackoverflow.com/questions/73172112/configuring-retry-policy-for-grpc-request
    - https://stackoverflow.com/questions/75931312/retry-policy-for-python-grpcs
    - github.com/grpc/proposal/blob/master/A6-client-retries.md#retry-policy-capabilities
    - https://chromium.googlesource.com/external/github.com/grpc/grpc/+/HEAD/examples/python/debug/
    

    Args:
        list_of_services (List[Dict[str, str]]): List of {'service': 'pkg.svc'} definitions. Example: [{'service': {'inference.Prediction'}]. Defaults to [{}] and 
            it configures same service confs to all RPCs.
        timeout (str): Timeout. Defaults to '30.0s'
        maxAttempts (int, optional): maxAttempts. Defaults to 5.
        waitForReady (bool): waitForReady. Defaults to True.
        initialBackoff (str, optional): initialBackoff. Defaults to "0.1s".
        maxBackoff (str, optional): maxBackoff. Defaults to "10s".
        backoffMultiplier (int, optional): backoffMultiplier. Defaults to 2.
        retryableStatusCodes (list, optional): List of retryableStatusCodes. Defaults to ['UNAVAILABLE'].

    Returns:
        str: gRPC Service configuration.
    """
    
    return json.dumps(
    {
        "methodConfig": [
            {
                "name": list_of_services,
                "timeout": timeout,
                "waitForReady": waitForReady,
                "retryPolicy": {
                    "maxAttempts": maxAttempts,
                    "initialBackoff": initialBackoff,
                    "maxBackoff": maxBackoff,
                    "backoffMultiplier": backoffMultiplier,
                    "retryableStatusCodes": retryableStatusCodes,
                },
            }
        ]
    }
)
    
def payload_cleaner(kwargs: dict, config: dict):
    """Remove Extra Keys for fixing gRPC payloads."""
    
    keys_to_remove = []       
    for k in kwargs.keys():
        if k not in config.keys():
            print("[WARNING] ", k, " key is not in payload/kwargs dict!")
            keys_to_remove.append(k)
    for i in keys_to_remove:
        del kwargs[i]
    return kwargs

def merge_with_defaults(user_request, default_parameters):
    merged_dict = {**default_parameters, **user_request}

    for key, value in default_parameters.items():
        if key not in user_request:
            merged_dict[key] = value

    return merged_dict

class AttrDict(dict):
    def __getattr__(self, attr):
        if attr in self:
            return self[attr]
        else:
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{attr}'")

    def __setattr__(self, attr, value):
        self[attr] = value
        
def get_ip_port_from_context(context):
    peer = unquote(context.peer())
    ip = peer[peer.find(':')+1:peer.rfind(':')]
    port = peer[peer.rfind(':')+1:]
    return ip, port

# gRPC Interceptors
def _wrap_rpc_behavior(handler, fn):
    if handler is None:
        return None

    if handler.request_streaming and handler.response_streaming:
        behavior_fn = handler.stream_stream
        handler_factory = grpc.stream_stream_rpc_method_handler
    elif handler.request_streaming and not handler.response_streaming:
        behavior_fn = handler.stream_unary
        handler_factory = grpc.stream_unary_rpc_method_handler
    elif not handler.request_streaming and handler.response_streaming:
        behavior_fn = handler.unary_stream
        handler_factory = grpc.unary_stream_rpc_method_handler
    else:
        behavior_fn = handler.unary_unary
        handler_factory = grpc.unary_unary_rpc_method_handler

    return handler_factory(fn(behavior_fn,
                              handler.request_streaming,
                              handler.response_streaming),
                           request_deserializer=handler.request_deserializer,
                           response_serializer=handler.response_serializer)


class TracebackLoggerInterceptor(grpc.ServerInterceptor):

    def intercept_service(self, continuation, handler_call_details):
        def latency_wrapper(behavior, request_streaming, response_streaming):

            def new_behavior(request_or_iterator, servicer_context):
                try:
                    return behavior(request_or_iterator, servicer_context)
                except Exception as err:
                    logging.exception(err, exc_info=True)
            return new_behavior

        return _wrap_rpc_behavior(continuation(handler_call_details),    latency_wrapper)
        
def grpc_exception_handler(
    context,
    ip: str,
    port: str,
    service_name: str,
    method_name: str,
    exc,
    logger: logging.Logger
    ) -> None:
    """gRPC Exception Handler for Debugging. It sends Full Traceback Message to Client from server and exit rpc call w/gracefully."""
    
    logger.info(' {ip}:{port} "RPC::{service_name}()::{method_name}() HTTP/2" UNKNOWN ERROR'.
                format(ip=ip, port=port, service_name=service_name, method_name=method_name))
    logger.exception("Exception in gRPC application \n", exc_info=exc)
    tb_str = traceback.format_exception(etype=type(exc), value=exc, tb=exc.__traceback__)
    tb_str = "".join(tb_str)
    context.set_code(grpc.StatusCode.UNKNOWN)
    context.set_details(tb_str)
    context.abort(grpc.StatusCode.UNKNOWN, tb_str)
    
def client_request_print(request, context, logger: logging.Logger) -> tuple:
    
    
    ip, port = get_ip_port_from_context(context=context)
    
    try:
        request = MessageToDict(request, preserving_proto_field_name=True)
    except Exception as e:
        exc = e
        tb_str = traceback.format_exception(etype=type(exc), value=exc, tb=exc.__traceback__)
        tb_str = "".join(tb_str)
        context.set_code(grpc.StatusCode.UNKNOWN)
        context.set_details(tb_str)
        context.abort(grpc.StatusCode.UNKNOWN, tb_str)
        logger.exception("An Error Occured When calling MessageToDict on 'request' for client request print: \n", exc_info=e)
        context.abort(grpc.StatusCode.UNKNOWN, tb_str)
        
    logger.info("Request Received From {ip}:{port}".format(ip=ip, port=port))
    logger.info('Request Proto:\n' + json.dumps(request, indent=4))
    logger.info(request)
    return ip, port, request

def set_grpc_call_success(request ,ip, port, service_name, method_name ,logger: logging.Logger):


    logger.info('{ip}:{port} gRPC call succeeded  "RPC::{service_name}()::{method_name}() HTTP/2" OK \n proto: {request}'.
                format(ip=ip, port=port, service_name=service_name, method_name=method_name, request=request))

        
        