# queries.py

CREATE_TABLE_products = """
    CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name_product TEXT,
    category TEXT,
    product_size TEXT,
    price TEXT,
    product_id TEXT,
    photo TEXT
    )
"""

INSERT_products_QUERY = """
    INSERT INTO products (name_product, category, product_size, price, product_id, photo)
    VALUES (?, ?, ?, ?, ?, ?)
"""