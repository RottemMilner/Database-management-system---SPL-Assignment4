class Hat:
    def __init__(self, hat_id, topping, supplier, quantity):
        self.hat_id = hat_id
        self.topping = topping
        self.supplier = supplier
        self.quantity = quantity


class Supplier:
    def __init__(self, supplier_id, name):
        self.supplier_id = supplier_id
        self.name = name


class Order:
    def __init__(self, order_id, location, hat_id):
        self.order_id = order_id
        self.location = location
        self.hat_id = hat_id
