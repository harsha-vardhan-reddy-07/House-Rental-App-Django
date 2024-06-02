from django.db import models

from db_connection import db

users_collection = db['users']

applications_collection = db['applications']

properties_collection = db['properties']
