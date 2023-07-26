import sqlite3
import sys

class Hotel:
    def __init__(self):
        self.connection = sqlite3.connect("Hotel.db")
        print("database connected")
        self.cursor = self.connection.cursor()
        self.create_table()
        self.tables_in_hotel = 50
        self.reserved_tables = []
        self.menu = {  # Move the menu dictionary to class level
            "Burger": 55.99,
            "Pizza": 125.99,
            "Pasta": 136.49,
            "Biryani": 187.25,
            "Salad": 100.00,
            "Chicken fry": 200.00,
            "Chilli chicken": 250.00,
            "Coke": 95.00,
            # Add more items here
        }

    def create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS HOTEL (
                               table_no INTEGER,
                               item TEXT ,
                               bill REAL ,
                               orders TEXT  )''')
        print("table created")
        self.connection.commit()

    def Reserve_table(self, table_no):
        if table_no >= self.tables_in_hotel:
            print("Sorry...table does not exist.")
            return

        if table_no in self.reserved_tables:
            print("Your table already reserved.. Pls select another table...")
            return

        self.reserved_tables.append(table_no)
        self.cursor.execute("INSERT INTO HOTEL (table_no) VALUES(?)", (table_no,))
        self.connection.commit()
        print(f"Your Table {table_no} is reserved.")
        print(self.reserved_tables)

    def Order_food(self, table_no, order):
        if table_no not in self.reserved_tables:
            print("Table not reserved. Please reserve a table first.")
            return

        # Convert food items to title case
        order = [item.strip().title() for item in order]

        # Check if all the items are available in the menu
        unavailable_items = [item for item in order if item not in self.menu]
        if unavailable_items:
            print(f"Sorry! {', '.join(unavailable_items)} items are not available here ..")
            print("Please select the order from the menu.")
            return

        # Assuming 'order' is a list containing food items
        for item in order:
            self.cursor.execute("INSERT INTO HOTEL (table_no, item) VALUES (?, ?)", (table_no, item,))
            self.connection.commit()
        print("Food order placed successfully!")    
    def Bill_amt(self, table_no):
    # Assuming you have a menu dictionary with item and price mapping
        menu = {
            "Burger": 45.99,
            "Pizza": 98.99,
            "Pasta": 136.49,
            "Biryani": 187.25,
            "Salad": 100.00,
            "Chicken fry": 200.00,
            "Chilli chicken": 250.00,
            "Coke": 95.00,
            # Add more items here
        }

        self.cursor.execute("SELECT item FROM HOTEL WHERE table_no=?", (table_no,))
        order_items = self.cursor.fetchall()

        if not order_items:
            print(f"No order found for Table {table_no}. Please place an order first...")
            return

        total_amount = 0
        print("Your bill:")
        for item in order_items:
            if item[0] is not None:  # Check if the item is not None
                item_title_case = item[0].title()  # Convert to title case
                if item_title_case in menu:
                    price = menu[item_title_case]
                    print(f"{item_title_case}: ${price}")
                    total_amount += price
                else:
                    print(f"Invalid item '{item_title_case}' in the order for Table {table_no}.")

        self.cursor.execute("UPDATE HOTEL SET bill=? WHERE table_no=?", (total_amount, table_no,))
        self.connection.commit()

        print(f"Total amount for Table {table_no}: ${total_amount}")
        print("Thank you for ordering!")

    def close_connection(self):
        self.cursor.close()
        self.connection.close()

h = Hotel()

while True:
    print("\n Welcome to 'Food Courz'")
    print("1. Reserve the table")
    print("2. Order food")
    print("3. Bill amount")
    print("4. Quit")

    choice = input("Enter your choice(1-4): ")

    if choice == "1":
        table_no = int(input("Enter table_no to reserve: "))
        h.Reserve_table(table_no)

    elif choice == "2":
        table_no = int(input("Enter table_no to order food: "))
        menu = {
            "Burger": 45.99,
            "Pizza": 98.99,
            "Pasta": 136.49,
            "Biryani": 187.25,
            "Salad": 100.00,
            "Chicken fry": 200.00,
            "Chilli chicken": 250.00,
            "coke": 95.00,
            # Add more items here
        }
        print(" MENU :   ")
        for item, price in menu.items():
            print(f"{item}: ${price}")
        order = input("Enter the food items (comma-separated): ").split(',')
        if not order :
            print("This kind of food not available")
            print("Select the order from menu")
        h.Order_food(table_no, order)

    elif choice == "3":
        table_no = int(input("Enter table_no to generate the bill: "))
        h.Bill_amt(table_no)

    elif choice == "4":
        print("Thank you for coming. Visit again...")
        h.close_connection()
        sys.exit()

    else:
        print("Select correct option.")
