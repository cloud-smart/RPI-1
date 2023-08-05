from pymongo import MongoClient
from datetime import datetime

# datetime object containing current date and time
now = datetime.now()

# Set up the MongoDB connection
username = 'cloudsmartlab'
password = 'cloudsmartlab'
cluster_name = 'cluster0.aj9ylxk'
database_name = 'Motion_Data'

# Construct the connection string
connection_string = f"mongodb+srv://{username}:{password}@{cluster_name}.mongodb.net/{database_name}?retryWrites=true&w=majority"

# Create a MongoDB client
client = MongoClient(connection_string)

db = client[database_name]

# Access a collection within the database
collection = db['Motion_detected']

#collection.delete_many({"Place": "SCIS backside"})

mydict = { "Place": "At High Rocks", "Time": now.strftime("%d/%m/%Y %H:%M:%S") }

x = collection.insert_one(mydict)

print(x.inserted_id)
