from pymongo import MongoClient
import certifi

client = MongoClient(
    "mongodb+srv://dintananggreini99_db_user:99Cahaya33MenyebutNya@linearregressionapp.2dxxpo1.mongodb.net/?retryWrites=true&w=majority",
    tlsCAFile=certifi.where()
)
print(client.list_database_names())
