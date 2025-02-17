import os

## MongoDB Configs
MongoDBUrl = os.getenv("MONGODB_URL_KEY","mongodb://root:rootpass@localhost:27017/?authSource=admin")
MongoDBName = os.getenv("MONGODB_DB_NAME","US_VISA")
MongoDBCollection = os.getenv("MONGO_DB_COLLECTION","visa_data")