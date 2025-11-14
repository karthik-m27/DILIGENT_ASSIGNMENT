# generate_data.py
# Usage: python generate_data.py
# Produces: products.csv, customers.csv, orders.csv, order_items.csv, reviews.csv

from faker import Faker
import csv
import random
from datetime import datetime, timedelta

fake = Faker()
FOLDERS = []
NUM_PRODUCTS = 50
NUM_CUSTOMERS = 100
NUM_ORDERS = 200
MAX_ITEMS_PER_ORDER = 5

# products.csv
with open('products.csv','w',newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['product_id','name','category','price'])
    for pid in range(1, NUM_PRODUCTS+1):
        name = fake.unique.word().title() + ' ' + fake.color_name()
        category = random.choice(['shirts','electronics','home','sports','beauty','toys'])
        price = round(random.uniform(5, 500), 2)
        writer.writerow([pid, name, category, price])

# customers.csv
with open('customers.csv','w',newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['customer_id','first_name','last_name','email','signup_date'])
    for cid in range(1, NUM_CUSTOMERS+1):
        p = fake.simple_profile()
        signup = fake.date_between(start_date='-2y', end_date='today').isoformat()
        writer.writerow([cid, p['name'].split()[0], p['name'].split()[-1], p['mail'], signup])

# orders.csv and order_items.csv
order_id = 1
with open('orders.csv','w',newline='', encoding='utf-8') as fo, open('order_items.csv','w',newline='', encoding='utf-8') as fi:
    w_orders = csv.writer(fo)
    w_items = csv.writer(fi)
    w_orders.writerow(['order_id','customer_id','order_date','status','total_amount'])
    w_items.writerow(['order_item_id','order_id','product_id','quantity','unit_price'])

    for _ in range(NUM_ORDERS):
        cid = random.randint(1, NUM_CUSTOMERS)
        od = fake.date_between(start_date='-1y', end_date='today')
        status = random.choice(['pending','shipped','delivered','cancelled'])
        num_items = random.randint(1, MAX_ITEMS_PER_ORDER)
        total = 0.0
        items = []
        for _i in range(num_items):
            pid = random.randint(1, NUM_PRODUCTS)
            qty = random.randint(1,4)
            unit_price = round(random.uniform(5, 500),2)
            total += unit_price * qty
            items.append((pid, qty, unit_price))
        w_orders.writerow([order_id, cid, od.isoformat(), status, round(total,2)])
        for idx, it in enumerate(items, start=1):
            w_items.writerow([f"{order_id}-{idx}", order_id, it[0], it[1], it[2]])
        order_id += 1

# reviews.csv (optional)
with open('reviews.csv','w',newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['review_id','product_id','customer_id','rating','review_text','review_date'])
    rid = 1
    for _ in range(int(NUM_PRODUCTS * 1.5)):
        pid = random.randint(1, NUM_PRODUCTS)
        cid = random.randint(1, NUM_CUSTOMERS)
        rating = random.randint(1,5)
        review_text = fake.sentence(nb_words=12)
        review_date = fake.date_between(start_date='-1y', end_date='today').isoformat()
        writer.writerow([rid, pid, cid, rating, review_text, review_date])
        rid += 1

print('CSV files generated: products.csv, customers.csv, orders.csv, order_items.csv, reviews.csv')