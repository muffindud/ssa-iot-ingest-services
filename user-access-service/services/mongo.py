from os import getenv

from pymongo import MongoClient


CLIENT = MongoClient(getenv('MONGO_URI'))
DB = CLIENT[getenv('MONGO_DB_NAME')]
