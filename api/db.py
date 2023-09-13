'''
Name: DB.py
Description: Database connection manager for
'''

from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

user = os.getenv("MONGO_USER")

pwd = os.getenv("MONGO_PASS")

host = os.getenv("MONGO_HOST")

connection = f"mongodb+srv://{user}:{pwd}@{host}/"

class DatabaseManager:
    def __init__(self, db_name):
        self.client = MongoClient(connection)
        self.db = self.client[db_name]
        print(f'Connected to {db_name} database') 
        self.manga = self.db['Manga'] # Get the Manga collection from the database

    def query(self, collection_name, query):
        collection = self.db[collection_name]
        return collection.find_one(query)

    def insert(self, collection_name, document):
        collection = self.db[collection_name]
        collection.insert_one(document)
        #result = collection.insert_one(document)
        #return result.inserted_id

    def __del__(self):
        self.client.close()
        


    def addManga(self, manga): # Cretes a new manga in the database - CREATE
        if self.exists('Manga', manga): # Query the database to see if the manga already exists
            self.updateManga(manga) # If it does, update the manga
            print(f"Updated manga: {manga['title']} from {manga['source']}")
        else:
            self.manga.insert_one(manga)  # If it doesn't, add the manga
            print(f"Added manga: {manga['title']} from {manga['source']}")


    def getManga(query): # Gets a manga from the database - READ
        manga = self.manga.query('Manga',query)
        print(f"Found manga: {manga['title']}")
        return manga


    def updateManga(self, manga): # Updates a manga in the database - UPDATE
        # if cover is different or number of chapters is different, update
        self.manga.update_one({'id': manga['id']}, {'$set': manga})
        print(f"Updated manga: {manga['title']} from {manga['source']}")


    def deleteManga(self, manga): # Deletes a manga from the database - DELETE
        self.manga.delete_one({'_id': manga['_id']})
        print(f"Deleted manga: {manga['title']} from {manga['source']}")



    def exists(self, collection_name, query): # Checks if a document exists in the database, return boolean
        collection = self.db[collection_name]
        return collection.find_one(query) != None
