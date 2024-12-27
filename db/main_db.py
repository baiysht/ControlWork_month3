# main_db.py

import sqlite3
from db import queries

db = sqlite3.connect('db/products')
cursor = db.cursor()


async def DataBase_create():
    if db:
        print('База данных подключена!')
    cursor.execute(queries.CREATE_TABLE_products)


async def sql_insert_products(name_product, category, product_size, price, product_id, photo):
    cursor.execute(queries.INSERT_products_QUERY, (
        name_product, category, product_size, price, product_id, photo
    ))
    db.commit()



# CRUD - Read
# =====================================================

# Основное подключение к базе (Для CRUD)
def get_db_connection():
    conn = sqlite3.connect('db/products')
    conn.row_factory = sqlite3.Row
    return conn


def fetch_all_products():
    conn = get_db_connection()
    products = conn.execute("""
    SELECT * from products
    """).fetchall()
    conn.close()
    return products