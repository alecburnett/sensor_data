import psycopg2
from sqlalchemy import create_engine

# connection parameters
hostname = ''
username = ''
password = ''
database = ''
dialect  = ''

#engine for alechemy
engine = dialect + "://" + username + ":" + password +"@" + hostname + "/" + database

#string for psycopg2
conn = psycopg2.connect( host=hostname, user=username, password=password, dbname=database )
