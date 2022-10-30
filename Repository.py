# The Repository
import atexit
import sqlite3
from DAOs import _Hats, _Suppliers, _Orders
from DTOs import Hat, Supplier, Order


class _Repository:
    def __init__(self, db_path):
        self._conn = sqlite3.connect(db_path)
        self.hats = _Hats(self._conn)
        self.suppliers = _Suppliers(self._conn)
        self.orders = _Orders(self._conn)
        self.output = ""

    def _close(self):
        self._conn.commit()
        self._conn.close()

    def create_tables(self):
        self._conn.executescript("""
        CREATE TABLE hats (
            id      INT         PRIMARY KEY,
            topping    TEXT        NOT NULL,
            supplier    INT,
            quantity    INT        NOT NULL,
            FOREIGN KEY(supplier) REFERENCES suppliers(id)
        );

        CREATE TABLE suppliers (
            id         INT     PRIMARY KEY,
            name     TEXT    NOT NULL
        );

        CREATE TABLE orders (
            id      INT     PRIMARY KEY,
            location      TEXT     NOT NULL,
            hat        INT,    FOREIGN KEY(hat) REFERENCES hats(id) 
        );
    """)

    def insert_hats(self, hats_list):
        for hat in hats_list:
            curr_hat = Hat(hat[0], hat[1], hat[2], hat[3])
            self.hats.insert(curr_hat)

    def insert_suppliers(self, suppliers_list):
        for supplier in suppliers_list:
            curr_supplier = Supplier(supplier[0], supplier[1])
            self.suppliers.insert(curr_supplier)

    def execute_orders(self, orders_list):
        i = 1
        for order in orders_list:
            hat_id = self.hats.executeOrder(order[1])
            curr_order = Order(i, order[0], hat_id)
            self.orders.insert(curr_order)
            self.output = self.output + str(order[1]) + "," + str(self.suppliers.find(self.hats.find(hat_id).supplier).name) + "," + str(order[0]) + "\n"
            self.hats.update_hats()
            i = i+1

    def close(self):
        self._conn.commit()
        self._conn.close()


def create(db_path):
    repo = _Repository(db_path)
    atexit.register(repo.close)
    return repo

