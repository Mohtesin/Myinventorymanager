import csv
import datetime


# -------------------- Class Definitions --------------------
class Product:
    def __init__(self, product_id, name, quantity, price):
        self.product_id = product_id
        self.name = name
        self.quantity = int(quantity)
        self.price = float(price)

    def display_info(self):
        print(f"[{self.product_id}] {self.name} - ${self.price:.2f} ({self.quantity} in stock)")

    def update_stock(self, amount):
        self.quantity += amount


class Order:
    def __init__(self, order_id, product_name, quantity, total_price, order_date=None):
        self.order_id = order_id
        self.product_name = product_name
        self.quantity = quantity
        self.total_price = total_price
        self.order_date = order_date or datetime.datetime.now()

    def display_order(self):
        print(f"Order ID: {self.order_id}, Product: {self.product_name}, Qty: {self.quantity}, "
              f"Total: ${self.total_price:.2f}, Date: {self.order_date.strftime('%Y-%m-%d %H:%M')}")


class Customer:
    def __init__(self, customer_id, name):
        self.customer_id = customer_id
        self.name = name
        self.orders = []

    def add_order(self, order):
        self.orders.append(order)

    def view_orders(self):
        print(f"\nOrders for Customer: {self.name}")
        for order in self.orders:
            order.display_order()


# -------------------- Manager Classes --------------------
class InventoryManager:
    def __init__(self):
        self.products = []

    def add_product(self, product):
        self.products.append(product)

    def update_product(self, product_id, quantity_change):
        product = self.get_product_by_id(product_id)
        if product:
            product.update_stock(quantity_change)
            print("Stock updated.")
        else:
            print("Product not found.")

    def delete_product(self, product_id):
        self.products = [p for p in self.products if p.product_id != product_id]

    def view_products(self):
        for p in self.products:
            p.display_info()

    def get_product_by_id(self, product_id):
        for p in self.products:
            if p.product_id == product_id:
                return p
        return None

    def save_inventory(self, filename="inventory.csv"):
        with open(filename, mode='w', newline='') as f:
            writer = csv.writer(f)
            for p in self.products:
                writer.writerow([p.product_id, p.name, p.quantity, p.price])

    def load_inventory(self, filename="inventory.csv"):
        try:
            with open(filename, mode='r') as f:
                reader = csv.reader(f)
                self.products = [Product(*row) for row in reader]
        except FileNotFoundError:
            self.products = []


class OrderManager:
    def __init__(self):
        self.customers = []
        self.order_id_counter = 1

    def register_customer(self, customer):
        self.customers.append(customer)

    def get_customer_by_id(self, customer_id):
        for c in self.customers:
            if c.customer_id == customer_id:
                return c
        return None

    def create_order(self, customer_id, product, quantity):
        customer = self.get_customer_by_id(customer_id)
        if not customer:
            print("Customer not found.")
            return

        if product.quantity >= quantity:
            total = product.price * quantity
            order = Order(self.order_id_counter, product.name, quantity, total)
            product.update_stock(-quantity)
            customer.add_order(order)
            self.order_id_counter += 1
            print("Order placed successfully.")
        else:
            print("Not enough stock.")

    def view_all_orders(self):
        for customer in self.customers:
            customer.view_orders()

    def save_orders(self, filename="orders.txt"):
        with open(filename, "w") as f:
            for customer in self.customers:
                for order in customer.orders:
                    f.write(f"{order.order_id},{customer.customer_id},{customer.name},"
                            f"{order.product_name},{order.quantity},{order.total_price},"
                            f"{order.order_date.strftime('%Y-%m-%d %H:%M')}\n")

    def load_orders(self, filename="orders.txt"):
        try:
            with open(filename, "r") as f:
                for line in f:
                    data = line.strip().split(",")
                    order_id, cust_id, cust_name, product_name, qty, total, date_str = data
                    customer = self.get_customer_by_id(cust_id)
                    if not customer:
                        customer = Customer(cust_id, cust_name)
                        self.register_customer(customer)
                    order_date = datetime.datetime.strptime(date_str, "%Y-%m-%d %H:%M")
                    order = Order(int(order_id), product_name, int(qty), float(total), order_date)
                    customer.add_order(order)
                    self.order_id_counter = max(self.order_id_counter, int(order_id) + 1)
        except FileNotFoundError:
            pass


# -------------------- Menu Interface --------------------
def main():
    inv = InventoryManager()
    ord_mgr = OrderManager()
    inv.load_inventory()
    ord_mgr.load_orders()

    while True:
        print("\n--- Smart Inventory & Customer Order System ---")
        print("1. View Inventory")
        print("2. Add Product")
        print("3. Update Product Stock")
        print("4. Delete Product")
        print("5. Register Customer")
        print("6. Create Order")
        print("7. View All Orders")
        print("8. Save Data")
        print("9. Exit")

        choice = input("Select option: ")

        if choice == '1':
            inv.view_products()

        elif choice == '2':
            pid = input("Product ID: ")
            name = input("Name: ")
            qty = int(input("Quantity: "))
            price = float(input("Price: "))
            inv.add_product(Product(pid, name, qty, price))

        elif choice == '3':
            pid = input("Product ID: ")
            qty_change = int(input("Quantity to add/subtract: "))
            inv.update_product(pid, qty_change)

        elif choice == '4':
            pid = input("Product ID to delete: ")
            inv.delete_product(pid)

        elif choice == '5':
            cid = input("Customer ID: ")
            name = input("Customer Name: ")
            ord_mgr.register_customer(Customer(cid, name))

        elif choice == '6':
            cid = input("Customer ID: ")
            inv.view_products()
            pid = input("Product ID to order: ")
            qty = int(input("Quantity: "))
            product = inv.get_product_by_id(pid)
            if product:
                ord_mgr.create_order(cid, product, qty)
            else:
                print("Product not found.")

        elif choice == '7':
            ord_mgr.view_all_orders()

        elif choice == '8':
            inv.save_inventory()
            ord_mgr.save_orders()
            print("Data saved.")

        elif choice == '9':
            inv.save_inventory()
            ord_mgr.save_orders()
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()