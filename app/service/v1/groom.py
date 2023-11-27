import random
import json
from typing import Iterable, AsyncIterable

import grpc
from google.protobuf.json_format import MessageToDict

from protos.v1 import groom_pb2_grpc, groom_pb2
from config import logger
from utils import (
    grpc_exception_handler,
    client_request_print,
    set_grpc_call_success,
    merge_with_defaults,
    AttrDict
    )

"""
def create_state_response(
    call_state: groom_pb2.CallState.State,
) -> groom_pb2.NewsStreamStatus:
    response = groom_pb2.StreamCallResponse()
    response.call_state.state = call_state
    return response
"""


class GroomService(groom_pb2_grpc.GroomServicer):
    def RoomRegistration(self, request, context):
        
        method_name = "RoomRegistration"
        service_name = self.__class__.__name__
        ip, port, request = client_request_print(request, context, logger)
        
        room_no = random.randint(1, 100)
        logger.info("Room no: {room_no}".format(room_no=room_no))
        """
        try:
            result = nc.ner(req=req, sent=request['sent'], DocName=request['DocName'], text=request['text'],
                            model=request['model'], version=request['v'], annotate=request['annotate'],
                            summary_only=request['summary_only'], out_format=request['out_format'],
                            use_cache=request['use_cache'], sentencizer=request['sentencizer'],
                            overwrite_cache=request["overwrite_cache"])
        except Exception as e:
            grpc_exception_handler(context, ip, port, service_name, method_name, e, logger)

        set_grpc_call_success(request, ip, port, service_name, method_name, logger)
        del nc
        return ner_pb2.NerResponse(prediction=json.dumps(result))
        """
        resp = groom_pb2.RoomRegistrationResponse(
            room_id=room_no
        )
        
        set_grpc_call_success(request, ip, port, service_name, method_name, logger)
        return resp
    

    async def SendNewsFlash(
        self,
        request_iterator: AsyncIterable[groom_pb2.NewsFlash],
        context: grpc.aio.ServicerContext
        ):
        
        method_name = "SendNewsFlash"
        service_name = self.__class__.__name__
                
        # Get Request form request_iterator
        async for request in request_iterator:
            try:
                ip, port, request_iterator = client_request_print(request, context, logger)
                client_request_print(request, context, logger)
                set_grpc_call_success(request, ip, port, service_name, method_name, logger)
            except Exception as e:
                grpc_exception_handler(context, ip, port, service_name, method_name, e, logger)
            
        set_grpc_call_success(request_iterator, ip, port, service_name, method_name, logger)
        return groom_pb2.NewsStreamStatus(success=True)
        
    
    