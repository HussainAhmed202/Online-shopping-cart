from abc import ABCMeta, abstractmethod
from platform import system
import products
import functions
from datetime import datetime
import pickle
import os.path


class User(metaclass=ABCMeta):

    @abstractmethod
    def dashboard(self):
        pass


class Admin(User):
    def __init__(self, firstname=None, lastname=None, username=None, password=None):
        self.__firstname = firstname
        self.__lastname = lastname
        self.__name = firstname + ' ' + lastname
        self.__username = username
        self.__password = password

        try:
            self.__id = functions.nextID('admin_info.txt')
        except FileNotFoundError:
            self.__id = 101

    def __str__(self):
        return f'{self.__id}, {self.__firstname}, {self.__lastname},  {self.__name}, {self.__username}, {self.__password}'

    @staticmethod
    def stock_dashboard():
        print( """
                 PRODUCTS IN STORE 
======================================================================================
1: Add item\t 2: Remove item\t 3: Edit item\t 4: View stock\t 5: Back to Dashboard    
====================================================================================== """)

    def dashboard(self):
        """ All features and functions that an administrator can perform are shown here """

        while True:
            print(f'\nWelcome Back,\n{self.__name}')
            print('''
    ==========================================================================
    1: Stock    2: Complaints Center    3:Monitor Activities    4: Sign Out
    ==========================================================================
            ''')

            choice = int(input(f'{self.__firstname}{self.__id}@{system()}:'))
            if choice == 1:
                self.stock_dashboard()
                command_dict = {1: self.add_item, 2: self.remove_item, 3: self.edit_item, 4: self.view_stock, 5:self.dashboard}
                while True:
                    choice = int(input(f'{self.__firstname}' + f'{self.__id}@{system()}:'))
                    try:
                        command_dict[choice]()
                        if choice == 5:
                            break

                    except KeyError:
                        print('Wrong input. Please select from the given options')

            elif choice == 3:
                self.monitor_activity()

            elif choice == 2:
                self.answer_complaints()

            elif choice == 4:
                interface('admin')
                return

    def view_stock(self):
        print("""
================================================================
1: Sort A-Z                     2: Sort Z-A
3: Price Highest To Lowest      4: Price Lowest To Highest 
5: Quantity Highest To Lowest   6: Quantity Lowest To Highest 
================================================================""")
        choice = int(input('Select Filter: '))
        item_list = products.sort_products(choice)
        for element in item_list:
            print(element)
        self.stock_dashboard()

    def add_item(self):
        while True:
            choice = input('Do you want to add item to stock \n1.Yes \n2.No\n')
            choice = choice.capitalize()
            if choice == 'No' or choice == '2':
                break
            else:
                product_code = functions.nextID('productsFile.txt')
                price = input('Write price of the product you want to add to stock: Rs ')
                name = input('Write name of the product you want to add to stock: ')
                name = name.title()
                manufacturer = input("Write Product's manufacturer:")
                manufacturer = manufacturer.title()
                description = input("Write description about Product: ")
                description = description.capitalize()
                quantity = input('How many are available in stock')
                add_item = f'{str(product_code)}, {price}, {name}, {manufacturer}, {description}, {quantity}\n'
                print('Item Added Successfully')

                outfile = open('productsFile.txt', 'a')
                outfile.write(add_item)
                outfile.close()

        self.stock_dashboard()

    def remove_item(self):
        num = int(input('Enter the code of the item you want to remove'))
        found = False

        with open('productsFile.txt', 'r+') as rf:
            item_list = rf.readlines()

            for record in item_list:
                item_code = record.split(', ')[0]
                if num == eval(item_code):
                    # item found
                    found = True
                    item_list.remove(record)
                    print('Item Removed')
                    break
            else:
                # item not found
                print('Item Not found')

            if found:  # check to make sure this part runs only if it needs to
                rf.seek(0)  # move to start of file
                rf.truncate(0)  # reduce file size to 0B / remove all content
                for item in item_list:
                    rf.write(item)
            self.stock_dashboard()

    def edit_item(self):
        item_code = int(input('Enter the code of item you want to edit: '))

        with open('productsFile.txt') as rf:
            item_list = rf.readlines()  # [record0,record1,record2]
            for code, line in enumerate(item_list):
                if item_code == code:  # item found
                    quantity = input('enter the new quantity')

                    record_list = line.strip().split(', ')
                    # ['0', '122000', '12S', 'Xiaomi', 'Xiaomi 12S', '12']

                    # replace quantity
                    record_list.pop()
                    record_list.append(quantity + '\n')
                    # ['0', '122000', '12S', 'Xiaomi', 'Xiaomi 12S', '14\n']

                    newline = ', '.join(record_list)
                    item_list.remove(line)
                    item_list.insert(code, newline)
                    break
            else:
                print('not found')

        with open('productsFile.txt', 'w') as wf:
            for _ in item_list:
                wf.write(_)
        self.stock_dashboard()


    def monitor_activity(self):
        username = input("Enter customer's username to view shopping history:")
        with open('customerInfo.txt') as rf:
            for record in rf.readlines():  # record => 0, sd@gmail.com, jackle
                serialNumber = int(record.split(', ')[0])
                uname = record.strip().split(', ')[1]
                if uname == username:
                    userToBeMonitored = customerInstances[serialNumber]
                    userToBeMonitored.view_shopping_history()
            else:
                print('User Not Found')


    def answer_complaints(self):
        while True:
            functions.view_complaints()
            customer_id = int(input('Answer which customer. Enter ID'))
            if functions.complaint_found(customer_id):
                answer = input('Answer Complaint..\n')
                with open('complaints_answered.txt', 'a') as af:
                    af.write(str(customer_id) + ', ' + answer + f', {datetime.now()}\n')
                functions.remove_complaint(customer_id)
                choice = input('Do you want to exit\n1.yes\nPress any key to continue')
                if choice == '1' or choice == 'yes':
                    break

            else:
                print('ID not found')
                break


class Customer(User):
    def __init__(self, firstname=None, lastname=None, username=None, password=None):
        self.firstname = firstname
        self.lastname = lastname
        self.name = firstname + ' ' + lastname
        self.username = username
        self.password = password
        self.cart = Cart(self)
        self.shoppingHistoryList = []

    def __str__(self):
        return f'{self.id}, {self.firstname}, {self.lastname},  {self.name}, {self.username}, {self.password}'

    def complaint_center(self):
        print('''
=======================================================
               
               THE COMPLAINT CENTER
      
1: Launch Complaint         2: Check Complaint Status

=======================================================''')
        choice = int(input())
        if choice == 1:
            # launching complaint
            print('Please verify your personal information')
            print(f'Full Name: {self.name}\nUserName: {self.username}\nUserID: {self.id}')
            choice = input('Confirm\n1.Yes \n2.No\n')
            choice = choice.capitalize()
            if choice == 'No' or choice == '2':
                return
            else:
                complaint = input('Please specify your complaint. Keep under 200 words')
                with open('customer_complaints.txt', 'a') as af:
                    af.write(str(self.id) + ', ' + complaint + '\n')

        elif choice == 2:
            # check complaint status
            found = False
            answered_complaints = []

            try:
                with open('complaints_answered.txt') as rf:
                    for i in rf.readlines():
                        if self.id == eval(i.strip().split(', ')[0]):
                            found = True
                            answered_complaints.append(i.strip().split(', ')[1:])
                if not found:
                    print('In Process')
                if found:
                    for _ in answered_complaints:
                        print(_[0] + ', ' + _[1])

            except FileNotFoundError:
                print('No complaint registered')

    def view_shopping_history(self):
        for log in self.shoppingHistoryList:
            log.displayInfo()
            self.dashboard()

    def shop(self):
        while True:
            # display list of products
            products.view_products()

            # ask user to select product
            productCode = int(input('Enter the product code'))

            product = productsList[productCode]

            # ask user to select quantity
            productQuantity = int(input('Enter the product quantity'))

            if products.quantity_valid(productQuantity, product.quantity):
                product.decrease_quantity(productQuantity)
                # add product to user's cart
                self.cart.addToCart(product, productQuantity)
                products.update_stock(productCode, product.quantity)
                if product.quantity == 0:
                    product.reorder()  # automatic reorder that item to avoid item starvation
                    products.update_stock(productCode, product.quantity)
                choice = input("Do you want to add another item? Y/N: ")
                if choice.upper() == "N":
                    self.dashboard()
                    break
                elif choice.upper() != "Y":
                    print("Invalid input!")


class Gold(Customer):
    customer_type = 'Gold'

    # future implementation
    # discount_rate = 0.4

    def __init__(self, firstname, lastname, username, password, wallet=40000):
        super().__init__(firstname, lastname, username, password)
        self.wallet = wallet
        try:
            self.id = functions.nextID('gold_customer_info.txt')
        except FileNotFoundError:
            self.id = 701

    def check_wallet(self):
        print(f'Wallet Status\n{self.wallet}')

    def checkout(self):
        """Creates new shopping history object, adds all items to that object, object is appended to shopping history
        list. """

        print('Checking out...')
        now = datetime.now()
        purchaseTime = now.strftime("%d/%m/%Y %H:%M:%S")
        shoppingHistoryLog = ShoppingHistoryLog(self.cart.items, self.cart.total, purchaseTime)
        self.wallet = int(self.cart.total * 0.10)
        self.shoppingHistoryList.append(shoppingHistoryLog)
        self.cart.items = []
        self.cart.emptyCart()
        print('Check out complete!')
        input('Press Enter to continue')
        self.dashboard()

    def dashboard(self):
        """ The gold customer dashboard """

        print(f'\nWelcome Back,\n{self.name}')
        print('''
===========================================================================================
        1: Shop    2: View Cart     3: Checkout        4: Complaints Center    
        
        5: View Shopping History    6: Check Wallet    7:Sign Out     8:Remove Product
===========================================================================================
                ''')

        command_dict = {1: self.shop, 2: self.cart.viewCart, 3: self.checkout, 4: self.complaint_center,
                        5: self.view_shopping_history, 6: self.check_wallet, 8: self.cart.removeFromCart}
        while True:
            choice = int(input('Select operation:'))
            try:
                if choice == 7:
                    interface('customer')
                    return
                else:
                    command_dict[choice]()
                break
            except KeyError:
                print('Wrong input. Please select from the given options')


class Standard(Customer):
    customer_type = 'Standard'

    def __init__(self, firstname, lastname, username, password):
        super().__init__(firstname, lastname, username, password)

        try:
            self.id = functions.nextID('standard_customer_info.txt')
        except FileNotFoundError:
            self.id = 801

    def upgrade_to_gold(self):
        print('You have been upgraded to Gold')
        with open('customerInfo.txt') as rf:
            for record in rf.readlines():  # record => 0, sd@gmail.com, jackle
                serialNumber = int(record.split(', ')[0])
                uname = record.strip().split(', ')[1]
                if uname == self.username:
                    cart = self.cart
                    fname = self.firstname
                    lname = self.lastname
                    username = self.username
                    pwd = self.password
                    shoppingHistoryList = self.shoppingHistoryList
                    user = Gold(fname, lname, username, pwd)
                    user.cart = cart
                    user.shoppingHistoryList = shoppingHistoryList

                    #  replace the standard customer object with the upgraded gold customer object
                    customerInstances.pop(serialNumber)
                    customerInstances.insert(serialNumber, user)
                    save_customers()

                    # remove customer from standard_customer_info.txt
                    functions.remove_customer(self.id)

                    # append to gold_customer_info.txt
                    with open('gold_customer_info.txt', 'a') as af:
                        af.write(user.__str__() + '\n')
                    user.dashboard()

    def checkout(self):
        """creates new shopping history object, adds all items to that object, object is appended to shopping history
        list. """

        print('Checking out...')
        now = datetime.now()
        purchaseTime = now.strftime("%d/%m/%Y %H:%M:%S")
        shoppingHistoryLog = ShoppingHistoryLog(self.cart.items, self.cart.total, purchaseTime)
        self.shoppingHistoryList.append(shoppingHistoryLog)
        self.cart.items = []
        self.cart.emptyCart()
        print('Check out complete!')
        input('Press Enter to continue')
        self.dashboard()

    def dashboard(self):
        """ The standard customer dashboard """

        print(f'\nWelcome Back,\n{self.name}')
        print('''
===========================================================================================
        1: Shop    2: View Cart     3: Checkout          4: Complaints Center    
        
        5: View Shopping History    6: Upgrade to gold   7: Sign Out    8: Remove Product
============================================================================================
                ''')

        command_dict = {1: self.shop, 2: self.cart.viewCart, 3: self.checkout, 4: self.complaint_center,
                        5: self.view_shopping_history, 6: self.upgrade_to_gold, 8: self.cart.removeFromCart}
        while True:
            choice = int(input('Select operation'))
            try:
                if choice == 7:
                    interface('customer')
                    return
                else:
                    command_dict[choice]()
                break
            except KeyError:
                print('Wrong input. Please select from the given options')


class Cart:

    def __init__(self, user):
        self.items = dict()
        self.total = 0
        self.user = user

    def updateTotal(self):
        self.total = 0
        for item, quantity in self.items.items():
            self.total += item.price * quantity
            save_customers()

    def addToCart(self, item, quantity):
        if item in self.items:
            self.items[item] = self.items[item] + quantity
        else:
            self.items[item] = quantity
            self.updateTotal()

    def removeFromCart(self):
        print("Cart: ")
        i = 1
        for item, quantity in self.items.items():
            print(str(i) + ": " + str(item.name) + ": " + str(quantity))
            i += 1
        print("Total: " + str(self.total))
        print("Products List:")

        products.view_products()
        productCode = int(input('Enter the product code to remove product:'))

        # verifies that the product to be removed exists in cart
        for product_obj in self.items.keys():   # items = {product object: quantity}
            if productCode == product_obj.code:
                product = productsList[productCode]
            else:
                print('This products does not exist in cart')
                return self.user.dashboard()

        # ask user to select quantity
        productQuantity = int(input('Enter the number of products to remove'))
        if productQuantity > self.items[product]:
            print('Invalid input. Not enough items in cart')
        else:
            self.items[product] = self.items[product] - productQuantity
        if self.items[product] == 0:
            del self.items[product]
        self.updateTotal()
        self.user.dashboard()


    def emptyCart(self):
        """deletes all items from cart"""

        self.items = {}
        self.total = 0
        save_customers()

    def viewCart(self):
        """displays cart contents and price"""

        print("Cart: ")
        i = 1
        for item, quantity in self.items.items():
            print(str(i) + ": " + str(item.name) + ": " + str(quantity))
            i += 1
        print("Total: " + str(self.total))
        input("Press Enter to continue...")
        self.user.dashboard()


class ShoppingHistoryLog:
    def __init__(self, items, total, purchaseTime):
        self.items = items
        self.total = total
        self.purchaseTime = purchaseTime

    def displayInfo(self):
        print("----------------------------------------------------------------------")
        for item, quantity in self.items.items():
            print(str(item.name) + ": " + str(quantity))
        print("Total: " + str(self.total))
        print("Time: " + str(self.purchaseTime))
        print("----------------------------------------------------------------------")


def save_customers():
    """Saving Customer Objects"""

    with open('customerInstances', 'wb') as customerInstancesFile:
        pickle.dump(customerInstances, customerInstancesFile)


def save_admin():
    """Saving Admin Objects"""

    with open('adminInstances', 'wb') as adminInstancesFile:
        pickle.dump(adminInstances, adminInstancesFile)


def interface(userType):
    if userType == 'admin':
        print('''
THE ADMIN INTERFACE

Type 'Login' to LOGIN
Type 'Signup' to CREATE NEW ADMIN ACCOUNT
''')
        choice = input()
        if choice.capitalize() == 'Login':
            while True:
                user = login('admin')
                return user

        elif choice.capitalize() == 'Signup':
            user = signup('admin')
            return user

    elif userType == 'customer':
        print("""
THE CUSTOMER INTERFACE

We Have Missed You
Type 'Shop' to SIGN IN 

Seeing Us for the first time? Lets start shopping 
Type 'Today' to SIGN UP""")

        choice = input()
        if choice.capitalize() == 'Shop':
            while True:
                user = login('customer')
                return user

        elif choice.capitalize() == 'Today':
            user = signup('customer')
            return user


def login(userType):
    """ Verifies the username and password for customer """

    username = input("Enter your username: ")

    if userType == 'admin':
        try:
            with open('adminInfo.txt') as rf:
                for record in rf.readlines():  # record => 0, jsmith@email.com, pop
                    serialNumber = int(record.split(', ')[0])
                    uname, pswd = record.strip().split(', ')[1:]
                    if uname == username:
                        print('Username matched')
                        while True:
                            password = input("Enter your password: ")
                            if pswd == password:
                                print('Password matched')
                                user = adminInstances[serialNumber]
                                return user
                            else:
                                print('Password incorrect')
                else:
                    print('User Not Found')
        except FileNotFoundError:
            print('Hello there. You must be running this for the first time')
            functions.about()
            return False

    elif userType == 'customer':
        try:
            with open('customerInfo.txt') as rf:
                for record in rf.readlines():  # record => 0, sd@gmail.com, jackle
                    serialNumber = int(record.split(', ')[0])
                    uname, pswd = record.strip().split(', ')[1:]
                    if uname == username:
                        print('Username matched')
                        while True:
                            password = input("Enter your password: ")
                            if pswd == password:
                                print('Password matched')
                                user = customerInstances[serialNumber]
                                return user
                            else:
                                print('Password incorrect')
                else:
                    print('User Not Found')

        except FileNotFoundError:
            print('Hello there. You must be running this for the first time')
            functions.about()


def signup(userType):
    """ Creates new account"""

    while True:
        firstname = input("Enter your firstname: ").strip().title()
        if functions.name_valid(firstname):
            break
        else:
            print('Name cannot have numbers')

    while True:
        lastname = input("Enter your lastname: ").strip().title()
        if functions.name_valid(lastname):
            break
        else:
            print('Name cannot have numbers')

    username = input("Enter your username: ").strip()
    password = input("Enter your password: ").strip()

    if userType == 'admin':
        # create new admin object
        user = Admin(firstname, lastname, username, password)
        serialNumber = len(adminInstances)

        adminInstances.append(user)

        # append to adminInfo.txt
        line = (str(serialNumber) + ', ' + username + ', ' + password + '\n')
        outfile = open('adminInfo.txt', 'a')
        outfile.write(line)
        outfile.close()

        # append to admin_info.txt
        with open('admin_info.txt', 'a') as af:
            af.write(user.__str__() + '\n')

        save_admin()
        return user

    if userType == 'customer':
        accountType = input("Enter your account type:\n1.standard\n2.gold(Paid)\n...")

        # append to customerInfo.txt
        serialNumber = len(customerInstances)

        line = (str(serialNumber) + ', ' + username + ', ' + password + '\n')
        outfile = open('customerInfo.txt', 'a')
        outfile.write(line)
        outfile.close()

        # create new customer object based on account type
        if accountType == "standard" or accountType == "1":
            user = Standard(firstname, lastname, username, password)
            customerInstances.append(user)
            save_customers()

            # append to standard_customer_info.txt
            with open('standard_customer_info.txt', 'a') as af:
                af.write(user.__str__() + '\n')
            return user

        elif accountType == "gold" or accountType == "2":
            print('Our gold service brings exclusive discounts')
            print('To avail these discounts it is going to cost 40000')
            yes = input('Type yes to confirm')
            # implement dummy payment method
            user = Gold(firstname, lastname, username, password)
            customerInstances.append(user)
            save_customers()

            # append to gold_customer_info.txt
            with open('gold_customer_info.txt', 'a') as af:
                af.write(user.__str__() + '\n')
            return user


def main():
    print("""
          =======
                 \ 
                  \_______________________
                   \                    /
                    \       THE        /
                     \    SHOPPING    /
                      \     CART     /
                       \____________/
                         O        O
    """)

    global productsList  # List containing product objects will be created
    productsList = products.initiate_products()

    global adminInstances  # List containing admin objects will be created
    adminInstances = []
    global customerInstances  # List containing customer objects will be created
    customerInstances = []

    # This function will initiate users at the start of the program.
    if os.path.exists('adminInstances'):
        with open('adminInstances', 'rb') as adminInstancesFile:
            adminInstances = pickle.load(adminInstancesFile)

        print(f'adminInstances file contains list: {adminInstances}')

    if os.path.exists('customerInstances'):
        with open('customerInstances', 'rb') as customerInstancesFile:
            customerInstances = pickle.load(customerInstancesFile)

        print(f'customerInstances file contains list: {customerInstances}')

    choice = int(input('''
Type 1 to go to the admin page
Type 2 to go to the customer page '''))
    if choice == 1:
        user = interface('admin')
    elif choice == 2:
        user = interface('customer')
    else:
        print('Wrong input')

    if type(user) == Admin or type(user) == Standard or type(user) == Gold:
        user.dashboard()


if __name__ == '__main__':
    main()
