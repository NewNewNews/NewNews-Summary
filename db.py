from pymongo import MongoClient

class SummaryDatabase:
    def __init__(self, db_url, db_name="summary"):
        self.client = MongoClient(db_url)
        self.db = self.client[db_name]
        self.news_collection = self.db["news"]  # Collection for storing news summaries

    def get_summary_from_url(self, url):
        file = self.news_collection.find_one({"url": url})
        if file:
            return file['summarized_text']
        return None
    
    def save_summary(self, url, summarized_text):
        # Check if the URL already exists
        if self.news_collection.find_one({"url": url}):
            print(f"Summary for {url} already exists.")
            return
        # Save new summary
        self.news_collection.insert_one({
            "url": url,
            "summarized_text": summarized_text
        })
        print(f"Summary for {url} saved.")
