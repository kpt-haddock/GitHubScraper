from dotenv import load_dotenv
from read_nodes import read_nodes
import pymongo
import os

load_dotenv()

MONGO_URL = os.getenv('MONGO_URL')
print(MONGO_URL)

mongo_client = pymongo.MongoClient(MONGO_URL)

database = mongo_client['GitHubScraper']
collection = database['Repositories']

print(collection)

nodes = read_nodes()
collection.insert_many(nodes)
