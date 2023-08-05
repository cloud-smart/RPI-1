from flask import Flask, render_template
from pymongo import MongoClient
from bson import json_util
import json

app = Flask(__name__)

# Configure MongoDB connection
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

# Route for rendering the webpage
@app.route('/')
def index():
    data = list(collection.find())
    return render_template('index.html', length=len(list(collection.find())))

# Route for serving the new data via AJAX request
@app.route('/get_new_data')
def get_new_data():
    # Retrieve the latest document from MongoDB
    data = list(collection.find())
    return json.loads(json_util.dumps(data))

if __name__ == '__main__':
    app.run(debug=True)
