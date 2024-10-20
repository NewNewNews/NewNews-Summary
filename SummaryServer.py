from concurrent import futures
from pymongo import MongoClient
import os
from bson.objectid import ObjectId
from concurrent import futures
import grpc
from protos import news_message_pb2
import json
import time
from confluent_kafka import Consumer,Producer, KafkaError
from confluent_kafka.serialization import (
    StringSerializer,
    SerializationContext,
    MessageField,
)
from confluent_kafka.schema_registry.protobuf import ProtobufSerializer, ProtobufDeserializer
from confluent_kafka.serialization import StringDeserializer
from confluent_kafka.schema_registry import SchemaRegistryClient
from protos import summary_pb2_grpc
from protos import summary_pb2
from simpletransformers.t5 import T5Model, T5Args
from dotenv import load_dotenv
from db import SummaryDatabase
import torch

class SummaryService(summary_pb2_grpc.SummaryService) :
    def __init__(self):
        self.db = SummaryDatabase(os.getenv("MONGODB_URI"))

    def SummarizeNews(self, request, context):
        print('request:', request)
        print('url:', request.url)
        summary = self.db.get_summary_from_url(request.url)
        if summary:
            return summary_pb2.SummaryNewsResponse(success=True,summarized_text=summary)
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"Summary for url '{request.url}' not found")
            return summary_pb2.SummaryNewsResponse(success=False,summarized_text='No summary')

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    summary_pb2_grpc.add_SummaryServiceServicer_to_server(SummaryService(), server)
    server.add_insecure_port('[::]:50053')
    server.start()
    print("Server started on port 50053")
    server.wait_for_termination()
    
if __name__ == '__main__':
    load_dotenv()
    db = SummaryDatabase(os.getenv("MONGODB_URI"))
    # find all summary in the database
    print("All summary in the database:")
    for file in db.news_collection.find():
        print(file)
    serve()