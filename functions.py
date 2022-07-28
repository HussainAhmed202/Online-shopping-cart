def about():
    print("""
THE SHOPPING CART

Authors of the Project:
GroupID: 7
Hussain Ahmed CS-92\tUsman Mujeeb CS-93\tAiman Naveed CS-77\tHafsa Habib CS-81

Please Note
At the start of the program you will not be able to login as there are no users. All user are stored in pickle files 
named adminInstances and customerInstances. And these files are not created initially

These files store the objects that is adminInstances file stores Admin objects and customerInstances file stores 
both Standard and Gold objects

So if you are running it for the first time then first signup as either Admin or Customer. The object will be stored

If you signup as Admin user, next time when you run the code you would see
adminInstances file contains list: [<__main__.Admin object at 0x000002474AAC5070>] 
note: address may vary

If you signup as Standard user, next time when you run the code you would see
customerInstances file contains list: [<__main__.Standard object at 0x000002474AA980A0>] 
note: address may vary

If you signup as Gold user, next time when you run the code you would see
customerInstances file contains list: [<__main__.Gold object at 0x000002474AA98DF0>]] 
note: address may vary

If you have done all of the above, next time when you run the code you would see
adminInstances file contains list: [<__main__.Admin object at 0x000002474AAC5070>]
customerInstances file contains list: [[<__main__.Standard object at 0x000002474AA980A0>, <__main__.Gold object at 0x000002474AA98DF0>]
""")


def view_complaints():
    try:
        with open('customer_complaints.txt') as rf:
            print('''
    =============================================
                  
                  CUSTOMER COMPLAINTS
                  
    =============================================\n''')
            for i in rf.readlines():
                print(i.strip())
    except FileNotFoundError:
        print('No Complaints')


def remove_complaint(customer_id: int):
    found = False  # flag to identity if record found

    with open('customer_complaints.txt') as rf:
        complaint_list = rf.readlines()
        for rec in complaint_list:
            complaint = rec  # 701, this is a test complaint
            complaint_id = complaint.split(', ')[0]  # 701
            if eval(complaint_id) == customer_id:
                complaint_list.remove(complaint)
                found = True  # record found
                break
        else:
            print('Record Not Found')

    if found:
        with open('customer_complaints.txt', 'w') as f:
            for rec in complaint_list:
                f.write(rec)


def nextID(filename: str) -> int:
    """It returns the ID number for the new object to be stored in
     the file passed as argument"""

    with open(filename) as f:
        for code in f.readlines():
            number = int(code.split(', ')[0])
        number += 1
    return number


def complaint_found(uid: int) -> bool:
    """Checks if complaint exists based on the ID received"""

    try:
        with open('customer_complaints.txt') as rf:
            complaint_list = rf.readlines()
            for complaint in complaint_list:
                complaint_id = eval(complaint.strip().split(', ')[0])
                if complaint_id == uid:
                    return True
            else:
                return False

    except FileNotFoundError:
        return False


def remove_customer(uid: int):
    customers_list = []

    with open('standard_customer_info.txt') as rf:
        rf.seek(0)
        for customer in rf.readlines():
            customerID = eval(customer.strip().split(', ')[0])
            if customerID != uid:
                customers_list.append(customer)

    with open('standard_customer_info.txt', 'w') as wf:
        for customer in customers_list:
            wf.write(customer)


def name_valid(s: str) -> bool:
    return not any([char.isdigit() for char in s])
