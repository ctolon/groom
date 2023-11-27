from concurrent import futures
from enum import Enum
from typing import List

import grpc

from config import settings, logger, GRPCServerTypes
from service.v1 import GroomService
from protos.v1 import groom_pb2_grpc

class GRPCServer(object):
    """GRPC Server Object."""

    @property
    def instance(self):
        return self.__server
    
    @property
    def logger(self):
        return self.__logger

    def __init__(
        self,
        address=settings.GRPC_HOST,
        port=settings.GRPC_PORT,
        max_workers=settings.WORKER,
        options=settings.GRPC_SERVER_OPTS,
        server_type=GRPCServerTypes.ASYNC,
        ):
        self.__address = address
        self.__port = port
        
        # Initialize GRPC Server as Singleton
        self.__logger = logger
        
        # Initialize GRPC Server as Async or Sync
        self.__enums = [e.value for e in GRPCServerTypes]
        self.__logger.info("GRPC Server Type: {server_type}".format(server_type=server_type))
        if server_type not in self.__enums:
            raise TypeError("Invalid GRPC Server Type! Please choose from {enums}".format(enums=self.__enums))
        
        if server_type == GRPCServerTypes.SYNC:
            self.__server = grpc.server(futures.ThreadPoolExecutor(max_workers=max_workers), options=options)
        else:
            self.__server = grpc.aio.server(options=options)


    def serve(self):
        endpoint = '{address}:{port}'.format(
            address=self.__address,
            port=str(self.__port)
        )

        self.logger.info(f'Started GRPC Server at {endpoint}')
        self.logger.info('Serving...')

        self.__server.add_insecure_port(endpoint)
        self.__server.start()
        self.__server.wait_for_termination()
        
    async def aio_serve(self):
        endpoint = '{address}:{port}'.format(
            address=self.__address,
            port=str(self.__port)
        )

        self.logger.info(f'Started GRPC Server at {endpoint}')
        self.logger.info('Serving...')

        self.__server.add_insecure_port(endpoint)
        await self.__server.start()
        await self.__server.wait_for_termination()

    def stop(self):
        self.logger.info("Stopping GRPC Server gracefully")
        self.__server.stop(3)
        
    def add_servicer_to_server(self, servicer_list: List[object]):
        """Servicer List is a list of servicer object.
        
        Example:
        
        servicer_list = [
            groom_pb2_grpc.add_GroomServicer_to_server(GroomService(), server.instance)
            ]
        """
        
        for servicer in servicer_list:
            servicer

def serve(
    address=settings.GRPC_HOST,
    port=settings.GRPC_PORT,
    max_workers=settings.WORKER,
    options=settings.GRPC_SERVER_OPTS,
    ) -> None:
    """GRPC Server Serving as Sync."""
    
    # Initialize GRPC Server  
    server = GRPCServer(address, port, max_workers, options, GRPCServerTypes.SYNC)
    
    # Define Servicer List
    servicer_list = [
        groom_pb2_grpc.add_GroomServicer_to_server(GroomService(), server.instance)
    ]
    
    # Register GRPC Services
    server.add_servicer_to_server(servicer_list)
    
    # Start GRPC Server
    server.serve()
    
async def aio_serve(
    address=settings.GRPC_HOST,
    port=settings.GRPC_PORT,
    options=settings.GRPC_SERVER_OPTS,
    ) -> None:
    """GRPC Server Serving as Async."""
    
    # Initialize GRPC Server  
    server = GRPCServer(address, port, None, options, GRPCServerTypes.ASYNC)
    
    # Define Servicer List
    servicer_list = [
        groom_pb2_grpc.add_GroomServicer_to_server(GroomService(), server.instance)
    ]
    
    # Register GRPC Services
    server.add_servicer_to_server(servicer_list)
    
    #for service in server.instance.state.generic_handlers:
    #    print("Service Name:", service.service_name())
    #    for method in service._method_handlers:
    #        print(4*" " + method)
    
    # Start GRPC Server
    await server.aio_serve()


if __name__ == '__main__':
    
    import argparse
    import asyncio
    
    parser = argparse.ArgumentParser(description="GRPC Server CLI")
    parser.add_argument("--host", "-H", help="GRPC Server Host", type=str, required=False, default=settings.GRPC_HOST)
    parser.add_argument("--port", "-p", help="GRPC Server Port", type=str, required=False, default=settings.GRPC_PORT)
    parser.add_argument("--worker", "-w", help="Num of Workers as Thread in Threadpool for concurrency", type=int, required=False, default=settings.WORKER)
    parser.add_argument("--server-type", "-st", help="GRPC Server Type", type=str.upper, required=False, default=GRPCServerTypes.SYNC.value, choices=list(GRPCServerTypes))
    args = parser.parse_args()
        
    port = args.port
    worker = args.worker
    host = args.host
    server_type = args.server_type
    
    # For gRPC, Workers shouldn't be less than 10
    if worker < 10:
        worker = 10
    
    # Start GRPC Server
    if args.server_type == GRPCServerTypes.SYNC:
        serve(host, port, worker)
    elif args.server_type == GRPCServerTypes.ASYNC:
        logger.info("Workers is not used for Async GRPC Server! (gRPC aio uses asyncio instead of threadpool)")
        asyncio.run(aio_serve(host, port))
