import sqlite3
from datetime import datetime


class Order:
    def __init__(self, user_id, device_type, device_name, description, created_at=None):
        self.user_id = user_id
        self.device_type = device_type
        self.device_name = device_name
        self.description = description
        self.created_at = created_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S") # Автоматическое заполнение

    def __repr__(self):
        return f"Order(user_id={self.user_id}, device_type='{self.device_type}', device_name='{self.device_name}', description='{self.description}', created_at='{self.created_at}')"


def create_tables(conn) -> None:
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            device_type TEXT NOT NULL,
            device_name TEXT NOT NULL,
            description TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)
    conn.commit()


def add_order(conn, order) -> None:
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO orders (user_id, device_type, device_name, description, created_at)
        VALUES (?, ?, ?, ?, ?)
    """, (order.user_id, order.device_type, order.device_name, order.description, order.created_at))
    conn.commit()


def get_orders_by_user_id(conn, user_id) -> list[Order]:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM orders WHERE user_id=?", (user_id,))
    rows = cursor.fetchall()
    orders = []
    for row in rows:
        orders.append(Order(row[1], row[2], row[3], row[4], row[5]))
    return orders


def create_connection(db_file) -> sqlite3.Connection:
    """
    Сreate a database connection to the SQLite database specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(e)

    return conn