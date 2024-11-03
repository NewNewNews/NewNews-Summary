from confluent_kafka import Consumer, KafkaError
from confluent_kafka.schema_registry.protobuf import ProtobufDeserializer
from confluent_kafka.serialization import (
    StringDeserializer,
    SerializationContext,
    MessageField,
)
from protos import news_message_pb2, summary_pb2  # generated from .proto
import os
from db import SummaryDatabase
from dotenv import load_dotenv
from simpletransformers.t5 import T5Model, T5Args
import torch

# from confluent_kafka.schema_registry import SchemaRegistryClient

# model = T5Model("t5", "thanathorn/mt5-cpe-kmutt-thai-sentence-sum", use_cuda=torch.cuda.is_available())

def create_summary(url, content):
    print('processing url:', url)
    sentence = "simplify: " + content
    # simplifytext = model.predict([sentence])
    db.save_summary(url=url,summarized_text=content[0:100])
    
def main():
    # schema_registry_conf = {
    #     "url": "http://localhost:8081"
    # }  # Change to your schema registry URL
    # schema_registry_client = SchemaRegistryClient(schema_registry_conf)

    protobuf_deserializer = ProtobufDeserializer(
        news_message_pb2.NewsMessage,
        # schema_registry_client,
        conf={"use.deprecated.format": True},
    )
    string_deserializer = StringDeserializer("utf_8")

    consumer_conf = {
        "bootstrap.servers": os.environ.get("KAFKA_BROKER", "localhost:9092"),
        "group.id": "news_group",
        "auto.offset.reset": "earliest",
    }

    consumer = Consumer(consumer_conf)
    consumer.subscribe(["news_topic"])

    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue

        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                continue
            else:
                print(msg.error())
                break

        key = string_deserializer(
            msg.key(), SerializationContext(msg.topic(), MessageField.KEY)
        )
        news_message = protobuf_deserializer(
            msg.value(), SerializationContext(msg.topic(), MessageField.VALUE)
        )
        
        if news_message is not None:
            print(f"Consumed record with key: {key}")
            print('news_message:', news_message)
            
        create_summary(news_message.url, news_message.data)

    consumer.close()


if __name__ == "__main__":
    load_dotenv()
    model = T5Model("t5", "thanathorn/mt5-cpe-kmutt-thai-sentence-sum", use_cuda=torch.cuda.is_available())
    db = SummaryDatabase(os.getenv("MONGODB_URI"))
    main()