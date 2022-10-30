# Data Access Objects:
# All of these are meant to be singletons
from DTOs import *


class _Hats:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, hat):
        self._conn.execute("""
               INSERT INTO hats (id, topping, supplier, quantity) VALUES (?, ?, ?, ?)
           """, [hat.hat_id, hat.topping, hat.supplier, hat.quantity])

    def find(self, hat_id):
        c = self._conn.cursor()
        c.execute("""
            SELECT id, topping, supplier, quantity FROM hats WHERE id = ?
        """, [hat_id])

        return Hat(*c.fetchone())

    def findToppingMinSupplierId(self, topping):
        c = self._conn.cursor()
        c.execute("""
            SELECT id, MIN(supplier) FROM hats WHERE topping = ?
        """, [topping])
        hat = c.fetchone()
        return hat[0]

    def executeOrder(self, topping):
        hat_id = self.findToppingMinSupplierId(topping)
        c = self._conn.cursor()
        c.execute("""
            UPDATE hats SET quantity = quantity-1 WHERE id = ? """, [hat_id])
        return hat_id

    def update_hats(self):
        c = self._conn.cursor()
        c.execute("""
            DELETE FROM hats WHERE quantity = 0""")


class _Suppliers:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, supplier):
        self._conn.execute("""
                INSERT INTO suppliers (id, name) VALUES (?, ?)
        """, [supplier.supplier_id, supplier.name])

    def find(self, supplier_id):
        c = self._conn.cursor()
        c.execute("""
                SELECT id,name FROM suppliers WHERE id = ?
            """, [supplier_id])

        return Supplier(*c.fetchone())


class _Orders:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, order):
        self._conn.execute("""
            INSERT INTO orders (id, location, hat) VALUES (?, ?, ?)
        """, [order.order_id, order.location, order.hat_id])

    def find_all(self):
        c = self._conn.cursor()
        all = c.execute("""
            SELECT id, location, hat FROM orders
        """).fetchall()

        return [Order(*row) for row in all]
