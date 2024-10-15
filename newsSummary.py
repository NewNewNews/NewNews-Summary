from concurrent import futures
from pymongo import MongoClient
import os
from bson.objectid import ObjectId
from concurrent import futures
import grpc
from proto import news_message_pb2
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
from proto import summary_pb2_grpc
from proto import summary_pb2
from simpletransformers.t5 import T5Model, T5Args
import torch

class SummaryService(summary_pb2_grpc.SummaryService) :
    def __init__(self):
        mongo_uri = os.environ.get("MONGO_URI", "mongodb://localhost:27017/")
        kafka_broker = os.environ.get("KAFKA_BROKER", "localhost:9092")

        # MongoDB connection setup
        self.mongo_client = MongoClient(mongo_uri)
        self.db = self.mongo_client["news_db"]
        self.collection = self.db["news"]
        print(f"Connected to MongoDB at: {mongo_uri}")

        # Kafka Consumer configuration
        consumer_conf = {
            "bootstrap.servers": kafka_broker,
            "group.id": "news_group",  # Consumer group ID
            "auto.offset.reset": "earliest",  # Start from the earliest message if no offset is set
        }
        self.consumer = Consumer(consumer_conf)
        self.consumer.subscribe(["scraped-news"])  # Subscribing to Kafka topic

        # Set up deserializers
        self.protobuf_deserializer = ProtobufDeserializer(
            news_message_pb2.NewsMessage,
            conf={"use.deprecated.format": True},
        )
        self.string_deserializer = StringDeserializer("utf_8")

        self.model = T5Model("t5", "thanathorn/mt5-cpe-kmutt-thai-sentence-sum", use_cuda=torch.cuda.is_available())

        # self.protobuf_serializer = ProtobufSerializer(
        #     news_message_pb2.NewsMessage,
        #     self.schema_registry_client,
        #     conf={"use.deprecated.format": True},
        # )
        self.string_serializer = StringSerializer("utf8")
    
    def SummarizeNews(self, request, context):
        sentence = "simplify: " + request.text
        simplifytext = self.model.predict([sentence])

        response = summary_pb2.SummaryNewsResponse()
        response.success = True
        response.summarized_text = simplifytext[0]  # Use the first item from the list returned by predict
        return response

    def consume_messages(self):
        try:
            while True:
                msg = self.consumer.poll(1.0)  # Poll with a timeout of 1 second
                if msg is None:
                    continue  # No message to consume

                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        continue  # End of partition event
                    else:
                        print(f"Consumer error: {msg.error()}")
                        break

                # Deserialize key and message value
                key = self.string_deserializer(
                    msg.key(), SerializationContext(msg.topic(), MessageField.KEY)
                )
                news_message = self.protobuf_deserializer(
                    msg.value(), SerializationContext(msg.topic(), MessageField.VALUE)
                )

                if news_message is not None:
                    print(f"Consumed record with key {key}: {news_message}")
                    
                    # Optionally process the news message (e.g., save it to MongoDB)
                    self.collection.insert_one({
                        "data": news_message.data,
                        "category": news_message.category,
                        "date": news_message.date,
                        "publisher": news_message.publisher,
                        "url": news_message.url
                    })
        except KeyboardInterrupt:
            pass
        finally:
            self.consumer.close()  # Ensure the consumer is closed on shutdown

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