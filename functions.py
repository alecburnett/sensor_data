from sqlalchemy import create_engine
import psycopg2
import pandas as pd
from connection_params import *

#replaces db table
def replace_db(df, table, engine):
    df.to_sql(table, engine, if_exists='replace', index=False)

#appends db table
def append_db(df, table, engine):
    df.to_sql(table, engine, if_exists='append', index=False)
