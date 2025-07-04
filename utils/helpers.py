from pymongo import MongoClient
from datetime import datetime

class OADMensalidade:
    def __init__(self, uri: str, db_name: str = "rotary", collection_name: str = "mensalidades"):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def inserer(self, doc):
        doc["data_transacao"] = datetime.now()
        return self.collection.insert_one(doc)

    def obtenir_tous(self):
        return list(self.collection.find())

    def supprimer(self, doc_id):
        from bson.objectid import ObjectId
        return self.collection.delete_one({"_id": ObjectId(doc_id)})

    def modifier(self, doc_id, update):
        from bson.objectid import ObjectId
        return self.collection.update_one({"_id": ObjectId(doc_id)}, {"$set": update})
