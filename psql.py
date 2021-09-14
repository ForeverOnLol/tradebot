import psycopg2
from dotenv import load_dotenv
import os


class Db:
    def __init__(self):
        load_dotenv()
        self.conn = psycopg2.connect(dbname=os.getenv('DBNAME'), user=os.getenv('DBUSER'),
                                     password=os.getenv('DBPASSWORD'), host=os.getenv('DBHOST'))

    def create_tables(self):
        cursor = self.conn.cursor()
        query = f'CREATE TABLE IF NOT EXISTS item(' \
                f'id SERIAL PRIMARY KEY NOT NULL,' \
                f'appid INTEGER,' \
                f'hash_name TEXT NOT NULL);'
        cursor.execute(query)
        query = f'CREATE TABLE IF NOT EXISTS price(' \
                f'item_id integer REFERENCES item(id),' \
                f'time timestamp NOT NULL,' \
                f'price float(4) not NULL,' \
                f'sold integer NOT NULL);'
        cursor.execute(query)
        self.close_cursor(cursor)

    def insert_items(self, data_list):
        cursor = self.conn.cursor()
        query = f'INSERT INTO item (appid, hash_name) VALUES (%s, %s)'
        cursor.executemany(query, data_list)
        self.close_cursor(cursor)

    def get_item_appid_name(self, p_key):
        cursor = self.conn.cursor()
        query = f'SELECT item.id, item.appid, item.hash_name FROM item WHERE item.id = %s'
        cursor.execute(query, [p_key])
        answer = cursor.fetchall()
        self.close_cursor(cursor)
        return answer

    def insert_prices(self, data_list):
        cursor = self.conn.cursor()
        query = f'INSERT INTO price (item_id, time, price, sold) VALUES (%s, %s, %s, %s)'
        cursor.executemany(query, [data_list])
        self.close_cursor(cursor)

    def close_cursor(self, cursor):
        self.conn.commit()
        cursor.close()
