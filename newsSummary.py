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
import torch

class SummaryService(summary_pb2_grpc.SummaryService) :
    def __init__(self):
        mongo_uri = os.environ.get("MONGO_URI", "mongodb://localhost:27017/")
        # kafka_broker = os.environ.get("KAFKA_BROKER", "localhost:9092")

        # MongoDB connection setup
        self.mongo_client = MongoClient(mongo_uri)
        self.db = self.mongo_client["example_database"]
        self.collection = self.db["example_collection"]
        print(f"Connected to MongoDB at: {mongo_uri}")

    def SummarizeNews(self, request, context):
        # Search MongoDB collection using the provided URL
        news_document = self.collection.find_one({"url": request.url})
        if news_document:
            # Get the text to summarize from the 'data' field of the document
            summarize = news_document.get("summarize", "")
            response = summary_pb2.SummaryNewsResponse()
            if summarize:
                response.success = True
                response.summarized_text = summarize
            else:
                response = summary_pb2.SummaryNewsResponse()
                response.success = False
                response.summarized_text = "No Summarize"
            return response
        else:
            # Return a failure response if no document found
            response = summary_pb2.SummaryNewsResponse()
            response.success = False
            response.summarized_text = "No news found for the given URL."
            return response

    # def UpdateNews(self, request, context):
    #     # Find the news document in MongoDB by URL
    #     news_document = self.collection.find_one({"url": request.url})

    #     if news_document:
    #         # Prepare the fields to update
    #         update_fields = {}
    #         if request.data:
    #             update_fields["data"] = request.data
    #         if request.date:
    #             update_fields["date"] = request.date
    #         if request.publisher:
    #             update_fields["publisher"] = request.publisher
    #         if request.category:
    #             update_fields["category"] = request.category

    #         # Only proceed if there are fields to update
    #         if update_fields:
    #             update_result = self.collection.update_one(
    #                 {"url": request.url},  # Filter by URL
    #                 {"$set": update_fields}  # Set the new values
    #             )

    #             response = summary_pb2.UpdateNewsResponse()
    #             if update_result.modified_count > 0:
    #                 # Successfully updated the document
    #                 response.success = True
    #             else:
    #                 # The document was found but nothing was updated (e.g., if the data was identical)
    #                 response.success = True

    #             return response
    #         else:
    #             # Return a failure response if no valid fields were provided for update
    #             response = summary_pb2.SummaryNewsResponse()
    #             response.success = False
    #             return response
    #     else:
    #         # Return a failure response if no document found with the provided URL
    #         response = summary_pb2.SummaryNewsResponse()
    #         response.success = False
    #         return response
    
    # def DeleteNews(self, request, context):
    #     # Find and delete the news document in MongoDB by URL
    #     delete_result = self.collection.delete_one({"url": request.url})

    #     response = summary_pb2.DeleteNewsResponse()

    #     if delete_result.deleted_count > 0:
    #         # If a document was deleted, return success
    #         response.success = True
    #     else:
    #         # No document was found with the given URL
    #         response.success = False

    #     return response

if __name__ == '__main__' :
    # Create an instance of the service
    service = SummaryService()
    
    # Set up the gRPC server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    summary_pb2_grpc.add_SummaryServiceServicer_to_server(service, server)
    
    # Define the port to listen on
    port = os.environ.get("GRPC_PORT", "50051")
    server.add_insecure_port(f"[::]:{port}")
    print(f"Starting gRPC server on port {port}...")
    
    # Start the server
    server.start()
    
    try:
        # This keeps the server running indefinitely
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        print("Shutting down server...")
        server.stop(0)