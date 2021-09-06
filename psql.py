import psycopg2
from dotenv import load_dotenv
import os


class Db:
    def __init__(self):
        self.conn = psycopg2.connect(dbname=os.getenv('DBNAME'), user=os.getenv('DBUSER'),
                                     password=os.getenv('DBPASSWORD'), host=os.getenv('DBHOST'))

    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute(f'DROP TABLE IF EXISTS item')
        query = f'CREATE TABLE item(' \
                f'id SERIAL PRIMARY KEY NOT NULL,' \
                f'appid INTEGER,' \
                f'hash_name TEXT NOT NULL);'
        cursor.execute(query)
        self.close_cursor(cursor)

    def insert_items(self, data_list):
        cursor = self.conn.cursor()
        query = f'INSERT INTO item (appid, hash_name) VALUES (%s, %s)'
        cursor.executemany(query, data_list)
        self.close_cursor(cursor)

    def close_cursor(self, cursor):
        self.conn.commit()
        cursor.close()
