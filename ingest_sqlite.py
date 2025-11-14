# ingest_sqlite.py
# Usage: python ingest_sqlite.py
# Creates ecom.db (SQLite), creates tables and ingests CSV files from generate_data.py

import sqlite3
import csv

DB = 'ecom.db'
conn = sqlite3.connect(DB)
c = conn.cursor()

# drop existing tables (safe for quick iteration)
c.execute('PRAGMA foreign_keys = ON;')

c.executescript('''
DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS reviews;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS customers;

CREATE TABLE products(
  product_id INTEGER PRIMARY KEY,
  name TEXT,
  category TEXT,
  price REAL
);

CREATE TABLE customers(
  customer_id INTEGER PRIMARY KEY,
  first_name TEXT,
  last_name TEXT,
  email TEXT UNIQUE,
  signup_date TEXT
);

CREATE TABLE orders(
  order_id INTEGER PRIMARY KEY,
  customer_id INTEGER,
  order_date TEXT,
  status TEXT,
  total_amount REAL,
  FOREIGN KEY(customer_id) REFERENCES customers(customer_id)
);

CREATE TABLE order_items(
  order_item_id TEXT PRIMARY KEY,
  order_id INTEGER,
  product_id INTEGER,
  quantity INTEGER,
  unit_price REAL,
  FOREIGN KEY(order_id) REFERENCES orders(order_id),
  FOREIGN KEY(product_id) REFERENCES products(product_id)
);

CREATE TABLE reviews(
  review_id INTEGER PRIMARY KEY,
  product_id INTEGER,
  customer_id INTEGER,
  rating INTEGER,
  review_text TEXT,
  review_date TEXT,
  FOREIGN KEY(product_id) REFERENCES products(product_id),
  FOREIGN KEY(customer_id) REFERENCES customers(customer_id)
);
''')
conn.commit()

# helper to bulk load CSV into a table
def load_csv_to_table(path, table, columns):
    with open(path, 'r', encoding='utf-8') as f:
        dr = csv.DictReader(f)
        cols = ','.join(columns)
        q = '(' + ','.join(['?']*len(columns)) + ')'
        to_db = []
        for row in dr:
            # order values according to columns
            vals = [row[col] if row[col] != '' else None for col in columns]
            to_db.append(vals)
    placeholders = ','.join(['?']*len(columns))
    insert_q = f'INSERT OR REPLACE INTO {table} ({cols}) VALUES ({placeholders})'
    conn.executemany(insert_q, to_db)
    conn.commit()

# load each file
load_csv_to_table('products.csv','products',['product_id','name','category','price'])
load_csv_to_table('customers.csv','customers',['customer_id','first_name','last_name','email','signup_date'])
load_csv_to_table('orders.csv','orders',['order_id','customer_id','order_date','status','total_amount'])
load_csv_to_table('order_items.csv','order_items',['order_item_id','order_id','product_id','quantity','unit_price'])
load_csv_to_table('reviews.csv','reviews',['review_id','product_id','customer_id','rating','review_text','review_date'])

print('Data ingested into', DB)
conn.close()