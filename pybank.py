#Py Bank Script 
#Author: Endrit Basha
#Online Banking Simulator with a MongoDB Database for account management and Password Encryption with Ceasers Cipher


import maskpass 
import pymongo
from pymongo import MongoClient



client = pymongo.MongoClient("mongodb+srv://diti85:1234@cluster0.e0iwbyw.mongodb.net/?retryWrites=true&w=majority")
db = client.test
collection = db["test"]


def account_menu(account):
    first_name = account["first_name"]
    last_name = account["last_name"]
    id  = account["_id"]
    print(f"Hi {first_name}, What would you like to do?")
    while True:
        print("Choose from one of the following options:")
        print("1. View your balance ")
        print("2. Make a deposit ")
        print("3. Make a withdrawal")
        print("4. Log out")
        choice = input()
        if (choice.isdigit):
            choice = int(choice)
            if choice == 1:
                account = collection.find_one({"_id": id})
                balance = account["balance"]
                print(f"Current account balance is ${balance}")#makeDeposit
            elif choice == 2:
                deposit = input("Enter the amount you would like to deposit $\n")
                if (deposit.isdigit):
                    deposit = int(deposit)
                    account = collection.update_one({"_id": id}, {"$inc":{"balance":deposit}})
                    print("Deposit was successful")
                else:
                    print("Please enter a valid numerical amount")
            elif choice == 3:
                withdraw = input("Enter the amount you would like to withdraw $\n")
                if (withdraw.isdigit):
                    withdraw = int(withdraw) * -1
                    account = collection.update_one({"_id": id}, {"$inc":{"balance": withdraw}})
                    print("Withdrawal was successful")
            elif choice == 4:
                    main_menu()
                    break
            else:
                print("Please choose between option 1-4.")


def login():
    while True:
        id = input("Please enter your unique User ID:\n")
        if collection.find_one({"_id": id}) != None:
            print("Please enter your password:")
            password = maskpass.askpass(mask="*")
            encrypted_password = encryption(password, "encrypt")
            results = collection.find_one({"_id": id})
            if results["password"] == encrypted_password:
                print("Log in was a success.")
                account_menu(results)
            else:
                print("Incorrect password, please try again.")



def main_menu():
    while True:
        print("Press 1 to log in to your existing account.")
        print("Press 2 to create a new account.")
        print("Press 3 to exit.")
        choice = input()
        if choice.isdigit():
            choice = int(choice)
            if 1 <= choice <= 3:
                if choice == 1:
                    return login()
                if choice == 2:
                    return create_account()
                if choice == 3:
                    print("Thank you for banking with PyBank. Goodbye")
                    quit()
            else:
                print('Please enter a number between 1-3')
        else:
            print("Please enter a number")





def create_account():
    while True:
        first_name = input("Please enter your first name\n")
        if first_name.isdigit():
            print("Invalid entry. No numbers allowed")
            create_account()
            break

        last_name = input("Please enter your last name\n")
        if last_name.isdigit():
            print("Invalid entry. No numbers allowed")
            create_account()
            break

        age = input("Please enter your age\n")
        valid_age = False
        while valid_age == False:
            if age.isdigit() == False:
                age = input("Please enter a valid age\n") 
            else:
                age = int(age)
                break
                

        id = input("Please enter a unique user ID\n")
        users_file = open("users.txt", "a")
        # file_exists = os.path.exists('users.txt')
        # if(file_exists == False):
        #     open("users.txt", "x")
        if (collection.find_one({"_id": id}) != None):
            print("An account with that User ID already exists")
            return main_menu()
        else:
            print("Please enter a unique password")
            password = maskpass.askpass(mask="*")
            encrypted_password = encryption(password, 'encrypt')
            post = {"_id": id, "first_name": first_name, "last_name": last_name, "age": age, "password": encrypted_password, "balance": 0}
            collection.insert_one(post)
            break
            

        
# Using ceasers cipher to encrypt password
def encryption(input,mode):
    key = 5
    ledger = 'abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ `!@#$%^&*()_+|{/}><?\,|.1234567890'
    output_text = ''

    for char in input:
        input_index = ledger.find(char)

        if mode == 'encrypt':
            output_index = (input_index + key )
        elif mode == 'decrypt':
            output_index = (input_index - key )
        #handling wraparound    
        if output_index >= len(ledger):
            output_index = output_index - len(ledger)
        elif output_index < 0:
            output_index = output_index + len(ledger)
        output_text += ledger[output_index]

    return output_text





print("-----------------")
print("Welcome to PyBank")
print("-----------------")
main_menu()
