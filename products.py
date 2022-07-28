class Product:
    def __init__(self, code, price, name, brand, description, quantity):
        self.code = code
        self.price = price
        self.name = name
        self.brand = brand
        self.description = description
        self.quantity = quantity

    # def __str__(self):
    #     return f'{self.name} - {self.price}'

    def decrease_quantity(self,quantity):
        self.quantity -= quantity

    def reorder(self):
        self.quantity = 20


def initiate_products() -> list:
    """This function will initiate a products list at the start of the program.
    Details of products are stored in the file 'productsFile.txt'.
    Lines in that file are formatted as
    'Code, Price, Name, Manufacturer, Description, Quantity'."""

    products_list = []

    with open('productsFile.txt') as f:
        for line in f:
            args = line.strip().split(', ')
            args[0] = int(args[0])
            args[1] = int(args[1])
            args[-1] = int(args[-1])
            products_list.append(Product(*args))

    return products_list


def view_products():
    print("""
=========================================================
1: Sort A-Z                   2: Sort Z-A
3: Price Highest To Lowest    4: Price Lowest To Highest  
=========================================================""")
    choice = int(input('Select Filter: '))
    item_list = sort_products(choice)
    for element in item_list:
        print(element)


def sort_products(choice: int) -> list:
    """Sorts and returns a list based on the choice of the user

    record = [code,price,name,manufacturer,description,quantity]

    sort functions used
    when referring to record[2] then sorting by name
    when referring to record[1] then sorting by price
    when referring to record[-1] then sorting by quantity    """

    record_list = []

    with open('productsFile.txt') as rf:

        # creating a new list which stores each tuple element
        for i in rf.readlines():
            code, price, name, manufacturer, description, quantity = i.strip().split(', ')
            rec = (eval(code), eval(price),  # (0, 122000, '12S', 'Xiaomi', 'Xiaomi 12S',20)
                   name, manufacturer, description,
                   eval(quantity))

            record_list.append(rec)  # [(..),(..),(..),(..)]

        if choice == 1:
            # A-Z sorted
            record_list.sort(key=lambda record: record[2])

        elif choice == 2:
            # Z - A sorted
            record_list.sort(key=lambda record: record[2], reverse=True)

        elif choice == 3:
            # Price High to Low
            record_list.sort(key=lambda record: record[1], reverse=True)

        elif choice == 4:
            # Price Low to High
            record_list.sort(key=lambda record: record[1])

        elif choice == 5:
            # Quantity High to Low
            record_list.sort(key=lambda record: record[-1], reverse=True)

        elif choice == 6:
            # Quantity Low to High
            record_list.sort(key=lambda record: record[-1])

        return record_list


def quantity_valid(input_quantity: int, product_quantity: int) -> bool:
    """Checks if the quantity of item required is within the range in stock

    product_quantity => the quantity attribute of the product object  """

    if 0 < input_quantity <= product_quantity:
        return True
    else:
        print('Invalid quantity')
        return False


def update_stock(serial_num: int, product_quantity: int):
    """Updates the product file
    product_quantity => the quantity attribute of the product object  """

    with open('productsFile.txt') as rf:
        items_list = rf.readlines()
        record = items_list[serial_num]  # num, price, name, manufacturer, info, quantity
        description = record.split(', ')[:-1]  # separate the quantity
        description.append(str(product_quantity))  # add the updated quantity to the list

        # preparing the record to be written in file
        record = ', '.join(description) + '\n'
        items_list.pop(serial_num)  # remove the record to be changed
        items_list.insert(serial_num, record)  # add the updated record at its original index

        with open('productsFile.txt', 'w') as wf:
            for product in items_list:
                wf.write(product)


