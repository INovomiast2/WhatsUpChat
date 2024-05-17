# DBManager - Version 1.0
import connect as connectDB
import manipulate as manipulateDB
import json
import re
import os
import argparse

class DBManager:
    def __init__(self):
        self.db = connectDB.connectDB()
        self.manipulate = manipulateDB
        
    def createCollection(self, collectionName):
        self.manipulate.create_collection(collectionName)
    
    def insertDocument(self, collectionName, document):
        self.manipulate.insert_document(collectionName, document)
        
    def findDocument(self, collectionName, query):
        return self.manipulate.find_document(collectionName, query)
    
def main():
    arguments = argparse.ArgumentParser(add_help=True, description='DBManager - Version 1.0', epilog='Developed by: INovomiast2', prog='DBManager', usage='%(prog)s -h for help')
    arguments.add_argument('--create-collection', type=str, help='Create a new collection in the database')
    arguments.add_argument('--insert-document', type=str, help='Insert a new document in the database', nargs=2, metavar=('collection', 'document'))
    arguments.add_argument('--find-document', type=str, help='Find a document in the database', metavar=('collection', 'query'), nargs=2)
    arguments.add_argument('--add-admin', type=str, help='Add an admin to the database', nargs=2, metavar=('username', 'password'))
    arguments.add_argument('-v', '--version', action='version', version='%(prog)s 1.0')
    
    args = arguments.parse_args()
    
    if args.create_collection:
        db = DBManager()
        db.createCollection(args.create_collection)
    elif args.insert_document:
        db = DBManager()
        db.insertDocument(args.insert_document[0], json.loads(args.insert_document[1]))
    elif args.find_document:
        db = DBManager()
        print(db.findDocument(args.find_document[0], json.loads(args.find_document[1])))
    else:
        print('Invalid arguments')
        arguments.print_usage()

if __name__ == '__main__':
    main()