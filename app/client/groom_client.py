import json
import inspect
from typing import Tuple, List, Dict

import grpc
from google.protobuf.json_format import MessageToJson, MessageToDict
from google.protobuf.timestamp_pb2 import Timestamp


from protos.v1 import groom_pb2_grpc, groom_pb2
from config import settings

# Default gRPC Channel Configuration
GRPC_DNS = settings.GRPC_HOST + ":" + str(settings.GRPC_PORT)
CHANNEL  = grpc.insecure_channel(settings.GRPC_HOST + ":" + str(settings.GRPC_PORT))

#async def AIO_CHANNEL():
#    return await grpc.aio.insecure_channel(settings.GRPC_HOST + ":" + str(settings.GRPC_PORT))

class GRoomClient:
    """GRPC Client Abstraction for ner api."""
    
    @staticmethod
    def room_registration(
        room_name: str,
        timeout=10,
        channel=CHANNEL,
        ):
        
     
        try:
            grpc.channel_ready_future(channel).result(timeout=timeout)
        except grpc.FutureTimeoutError:
            raise grpc.FutureTimeoutError('Error connecting to server: {GRPC_DNS}'.format(GRPC_DNS=GRPC_DNS))
        else:
            stub = groom_pb2_grpc.GroomStub(channel)
            
        # print(inspect.stack()[0][3] ,"json payload: ", payload)
        req = groom_pb2.RoomRegistrationRequest(room_name=room_name)
        res = stub.RoomRegistration(req)
        return groom_pb2.RoomRegistrationResponse(room_id=res.room_id)
    
    @staticmethod
    async def send_news_flash(
        req_string_list: List[Dict[str, str]],
        #news_time,
        #news_item,
        #timeout=10,
        # channel=AIO_CHANNEL,
    ):
        
        #try:
        #    await grpc.aio.insecure_channel(GRPC_DNS).channel_ready()
        #except grpc.FutureTimeoutError:
        #    raise grpc.FutureTimeoutError('Error connecting to server: {GRPC_DNS}'.format(GRPC_DNS=GRPC_DNS))
        #else:
        #    stub = groom_pb2_grpc.GroomStub(channel)
        # except grpc.aio.AioRpcError as e  
        # single_request = groom_pb2.NewsFlash(news_time=news_time, news_item=news_item) 
        
        # request_list = [
        #     groom_pb2.NewsFlash(news_time=news_time, news_item=news_item),
        #     groom_pb2.NewsFlash(news_time=news_time, news_item=news_item),
        #     groom_pb2.NewsFlash(news_time=news_time, news_item=news_item),
        #     ]
        # request_iterator = iter(request_list)  
        # res: grpc.aio._call.StreamUnaryCall = stub.SendNewsFlash(pb_req_list.__iter__())
        # call = await res  
        async with grpc.aio.insecure_channel(GRPC_DNS) as channel:
            
            print("Channel: ", GRPC_DNS)
            stub = groom_pb2_grpc.GroomStub(channel)
            
            news_time = Timestamp(seconds=10)
            news_item = "test news item"
            pb_req_list = []
            
            for request in req_string_list:
                news_time = request["news_time"]
                news_item = request["news_item"]
                pb_req_list.append(groom_pb2.NewsFlash(news_time=news_time, news_item=news_item))
                
            request_iterator = iter(pb_req_list)
            print("Sending News Flash...")
            res: grpc.aio._call.StreamUnaryCall = stub.SendNewsFlash(request_iterator)
            call = await res
            print("Response From Stream: ", call.success)
            return call.success
                            
            #  MetaData
            print(res)
            print(res.cancelled())
            print(await res.code())
            print(await res.details())
            print(await res.debug_error_string())
            print(await res.initial_metadata())
            print(await res.trailing_metadata())
            # print(await res.write())
            print(call)
                                                                
            # Direct read from the stub                
            # while True:
            #     response = await res.read()
            #     if response == grpc.aio.EOF:
            #         break
            #     print(
            #         "Greeter client received from direct read: " + response.message
            #     )
        
if __name__ == "__main__":
    
    import asyncio
    
    def run_room_registration():
        res = GRoomClient.room_registration(room_name="test room")
        return res
    
    async def run_send_news_flash():
        news_time = Timestamp(seconds=10)
        news_item = "test news item"
        res = await GRoomClient.send_news_flash(news_time=news_time, news_item=news_item)
    
    # print(run_room_registration())
    news_time = Timestamp(seconds=10)
    req_str_list = [{"news_time": Timestamp(seconds=1), "news_item": "item1"}, {"news_time": Timestamp(seconds=2), "news_item": "item2"}]
    asyncio.run(GRoomClient.send_news_flash(req_str_list))