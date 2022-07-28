# Online-shopping-cart
Online shopping cart 

Author of the Project:
Hussain Ahmed. Currently first year student at NEDUET


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
