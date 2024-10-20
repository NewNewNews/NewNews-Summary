import grpc
import protos.summary_pb2 as summary_pb2
import protos.summary_pb2_grpc as summary_pb2_grpc

def run():
    with grpc.insecure_channel('localhost:50053') as channel:
        stub = summary_pb2_grpc.SummaryServiceStub(channel)
        
        # Send news content
        url = input("Enter the news url: ")
        
        # Retrieve audio file
        print('url:', url)
        input("Press Enter to retrieve the summary...")
        response = stub.SummarizeNews(summary_pb2.SummaryNewsRequest(url=url))
        print(response)

if __name__ == '__main__':
    run()