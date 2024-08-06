from pymongo import MongoClient
from .config import Config

class DocumentDBClient:
    def __init__(self, cluster_endpoint, username, password, database):
        self.cluster_endpoint = cluster_endpoint
        self.username = username
        self.password = password
        self.database = database
        self.client = None
        self.db = None

    def connect(self):
        try:
            self.client = MongoClient(
                self.cluster_endpoint,
                username=self.username,
                password=self.password,
                tls=True,
                tlsAllowInvalidCertificates=True,
                retryWrites=False  # Disable retryable writes
            )
            self.db = self.client[self.database]
            print("Connected to DocumentDB")
        except Exception as e:
            print(f"Error connecting to DocumentDB: {e}")

    def disconnect(self):
        if self.client:
            self.client.close()
            print("Disconnected from DocumentDB")

    def insert_document(self, collection_name, document):
        try:
            collection = self.db[collection_name]
            result = collection.insert_one(document)
            return str(result.inserted_id)
        except Exception as e:
            print(f"Error inserting document: {e}")

    def get_document(self, collection_name, query) -> dict:
        try:
            collection = self.db[collection_name]
            document = collection.find_one(query)
            document = {**document, '_id': str(document['_id'])}
            return document
        except Exception as e:
            print(f"Error getting document: {e}")
        
    def get_documents(self, collection_name, query) -> list:
        try:
            collection = self.db[collection_name]
            documents = collection.find(query)
            documents = [{**doc, '_id': str(doc['_id'])} for doc in documents]
            return documents
        except Exception as e:
            print(f"Error getting documents: {e}")

    def replace_document(self, collection_name, query, document):
        try:
            collection = self.db[collection_name]
            result = collection.replace_one(query, document)
            return result.modified_count
        except Exception as e:
            print(f"Error replacing document: {e}")

    def delete_document(self, collection_name, query):
        try:
            collection = self.db[collection_name]
            result = collection.delete_one(query)
            return result.deleted_count
        except Exception as e:
            print(f"Error deleting document: {e}")


documentDBClient = DocumentDBClient(cluster_endpoint=Config.document_db_cluster_endpoint, 
                                    username=Config.document_db_username, password=Config.document_db_password, 
                                    database=Config.document_db_database)
