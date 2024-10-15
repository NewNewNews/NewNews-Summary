import grpc
from proto import summary_pb2, summary_pb2_grpc

def run():
    # Connect to the gRPC server
    with grpc.insecure_channel('localhost:50051') as channel:
        # Create a stub (client)
        stub = summary_pb2_grpc.SummaryServiceStub(channel)

        # Create a request with the text you want to summarize
        request = summary_pb2.SummaryNewsRequest(text="Your news article content goes here.")

        # Send the request and get the response
        response = stub.SummarizeNews(request)

        # Print the result
        if response.success:
            print(f"Summarized Text: {response.summarized_text}")
        else:
            print("Failed to summarize the text.")

if __name__ == '__main__':
    run()

