from pymongo import MongoClient
from datetime import datetime
import sys
from getGPS import getCoords

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

#collection.delete_many({})
timee = str(sys.argv[1]) + now.strftime("\t %d/%m/%Y %H:%M:%S")
s = getCoords()
mydict = { "Place": "SCIS front-side", "Time": timee, "Coordinates" : s}

x = collection.insert_one(mydict)

print("Human detected! Alert sent" + x.inserted_id)

