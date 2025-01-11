from .models import Order
import sqlite3

import config


DATABASE_NAME = config.DATABASE_NAME 


class Database:
    def __init__(self):
        """Initialize the database connection."""
        self.conn = sqlite3.connect(DATABASE_NAME)
        self.cursor = self.conn.cursor()
    
    def create_tables(self) -> None:
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                device_type TEXT NOT NULL,
                device_name TEXT NOT NULL,
                description TEXT NOT NULL,
                status INTEGER NOT NULL,
                created_at TEXT NOT NULL
            )
        """)
        self.conn.commit()

    def add_order(self, order) -> int:
        self.cursor.execute("""
            INSERT INTO orders (user_id, device_type, device_name, description, status, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (order.user_id, order.device_type, order.device_name, order.description, order.status, order.created_at))
        self.conn.commit()
        return self.cursor.lastrowid  # Return new order ID

    def get_orders(self, user_id=None) -> list[Order]:
        if user_id is not None:
            self.cursor.execute("SELECT * FROM orders WHERE user_id=?", (user_id,))
        else:
            self.cursor.execute("SELECT * FROM orders")
        
        rows = self.cursor.fetchall()
        orders = []
        for row in rows:
            orders.append(
                Order(
                    user_id=row[1],
                    device_type=row[2],
                    device_name=row[3],
                    description=row[4],
                    status=row[5],
                    created_at=row[6],
                    order_id=row[0]
                )
            )
        return orders
    
    def close(self):
        """Close the database connection."""
        self.conn.close()
