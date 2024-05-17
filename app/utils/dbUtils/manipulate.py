import pymongo
from pymongo import MongoClient
import dotenv
import os
from .connect import *
from .chatUtils import _utils_

def get_collection(collection_name):
    client = connectDB()
    collection = client.get_collection(collection_name)
    return collection

def insert_document(collection_name, document):
    collection = get_collection(collection_name)
    collection.insert_one(document)
    
def find_document(collection_name, query):
    collection = get_collection(collection_name)
    document = collection.find_one(query)
    return document

def create_collection(collection_name):
    client = connectDB()
    collection = client.create_collection(collection_name)
    return collection

def insert_field(collection_name, query, field):
    collection = get_collection(collection_name)
    collection.update_one(query, {'$set': field})
    
def delete_field(collection, query, field):
    collection = get_collection(collection)
    # Delete the field from the document
    collection.update_one(query, {'$unset': {field: 1}})
    
def update_field(collection_name, query, field):
    collection = get_collection(collection_name)
    collection.update_one(query, {'$set': field})
    
chatUtils = _utils_()