import sqlite3
import hashlib
from openpyxl import Workbook
from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import Table


conn = sqlite3.connect("MiniBank.db")
cursor = conn.cursor()

logged_in = False
current_role = ""
current_account = ""




def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

while True:

    print("\n========================================")
    print("          MINI BANK SYSTEM")
    print("========================================")

    print("1. Create Account")
    print("2. View All Accounts")
    print("3. Search Account")
    print("4. Deposit")
    print("5. Withdraw")
    print("6. Transfer Money")
    print("7. Delete Account")
    print("8. Transaction History")
    print("9. Login")
    print("0. Exit")
    print("10. Sort By Balance")
    print("11. Export To Excel")
    print("12. Export To PDF")

    choice = input("\nEnter your choice: ")


# ================= Login & Role =================

    if not logged_in:

     if choice not in ["1", "9", "0"]:

        print("\nPlease Login First!")
        continue

    else:

     if current_role == "Customer":

        if choice not in ["4", "5", "6", "8", "0"]:

            print("\nAccess Denied!")
            continue

     elif current_role == "Admin":

        if choice not in ["1", "2", "3", "7", "10", "11", "12", "0"]:

            print("\nAccess Denied!")
            continue
 


    if choice == "1":

        print("\nCreate Account")

        account_number = input("Enter Account Number: ")
        customer_name = input("Enter Customer Name: ")
        phone_number = input("Enter Phone Number: ")
        password = input("Enter Password: ")

        password = hash_password(password)

        balance = float(input("Enter Initial Balance: "))

        print("\nChoose Role")
        print("1. Admin")
        print("2. Customer")

        role_choice = input("Enter Choice: ")

        if role_choice == "1":
            role = "Admin"
        else:
            role = "Customer"

        cursor.execute("""
            INSERT INTO Customers
            (AccountNumber, CustomerName, PhoneNumber, Password, Balance, Role)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            account_number,
            customer_name,
            phone_number,
            password,
            balance,
            role
        ))

        conn.commit()

        print("Account Created Successfully")



    elif choice == "2":

        cursor.execute("SELECT * FROM Customers")

        customers = cursor.fetchall()

        if len(customers) == 0:

            print("No Account Found")

        else:

            print("\n------ All Accounts ------")

            for customer in customers:

                print("-------------------------")
                print("Customer ID    :", customer[0])
                print("Account Number :", customer[1])
                print("Customer Name  :", customer[2])
                print("Phone Number   :", customer[3])
                print("Balance        :", customer[5])
                print("Role           :", customer[6])


    elif choice == "3":

        account_number = input("Enter Account Number: ")

        cursor.execute(
            "SELECT * FROM Customers WHERE AccountNumber = ?",
            (account_number,)
        )

        customer = cursor.fetchone()

        if customer:

            print("\n------ Account Found ------")
            print("Customer ID    :", customer[0])
            print("Account Number :", customer[1])
            print("Customer Name  :", customer[2])
            print("Phone Number   :", customer[3])
            print("Balance        :", customer[5])
            print("Role           :", customer[6])

        else:

            print("Account Not Found")




    elif choice == "4":

        account_number = input("Enter Account Number: ")

        cursor.execute(
            "SELECT Balance FROM Customers WHERE AccountNumber = ?",
            (account_number,)
        )

        customer = cursor.fetchone()

        if customer:

            amount = float(input("Enter Deposit Amount: "))

            new_balance = customer[0] + amount

            cursor.execute(
                "UPDATE Customers SET Balance = ? WHERE AccountNumber = ?",
                (new_balance, account_number)
            )

            cursor.execute(
                "INSERT INTO Transactions (AccountNumber, TransactionType, Amount) VALUES (?, ?, ?)",
                (account_number, "Deposit", amount)
            )

            conn.commit()

            print("\nDeposit Successful")
            print("Current Balance :", new_balance)

        else:

            print("Account Not Found")


    

    elif choice == "5":

        account_number = input("Enter Account Number: ")

        cursor.execute(
            "SELECT Balance FROM Customers WHERE AccountNumber = ?",
            (account_number,)
        )

        customer = cursor.fetchone()

        if customer:

            amount = float(input("Enter Withdraw Amount: "))

            if amount <= customer[0]:

                new_balance = customer[0] - amount

                cursor.execute(
                    "UPDATE Customers SET Balance = ? WHERE AccountNumber = ?",
                    (new_balance, account_number)
                )

                cursor.execute(
                    "INSERT INTO Transactions (AccountNumber, TransactionType, Amount) VALUES (?, ?, ?)",
                    (account_number, "Withdraw", amount)
                )

                conn.commit()

                print("Withdraw Successful")
                print("Current Balance :", new_balance)

            else:

                print("Insufficient Balance")

        else:

            print("Account Not Found")






    elif choice == "6":

        sender = input("Enter Your Account Number: ")
        receiver = input("Enter Receiver Account Number: ")

        amount = float(input("Enter Transfer Amount: "))

        cursor.execute(
            "SELECT Balance FROM Customers WHERE AccountNumber = ?",
            (sender,)
        )

        sender_account = cursor.fetchone()

        cursor.execute(
            "SELECT Balance FROM Customers WHERE AccountNumber = ?",
            (receiver,)
        )

        receiver_account = cursor.fetchone()

        if sender_account and receiver_account:

            if sender_account[0] >= amount:

                new_sender_balance = sender_account[0] - amount
                new_receiver_balance = receiver_account[0] + amount

                cursor.execute(
                    "UPDATE Customers SET Balance = ? WHERE AccountNumber = ?",
                    (new_sender_balance, sender)
                )

                cursor.execute(
                    "UPDATE Customers SET Balance = ? WHERE AccountNumber = ?",
                    (new_receiver_balance, receiver)
                )

                cursor.execute(
                    "INSERT INTO Transactions (AccountNumber, TransactionType, Amount) VALUES (?, ?, ?)",
                    (sender, "Transfer", amount)
                )

                conn.commit()

                print("Transfer Successful")
                print("Your New Balance :", new_sender_balance)

            else:

                print("Insufficient Balance")

        else:

            print("Account Not Found")





    elif choice == "7":

        account_number = input("Enter Account Number: ")

        cursor.execute(
            "SELECT * FROM Customers WHERE AccountNumber = ?",
            (account_number,)
        )

        customer = cursor.fetchone()

        if customer:

            cursor.execute(
                "DELETE FROM Customers WHERE AccountNumber = ?",
                (account_number,)
            )

            conn.commit()

            print("Account Deleted Successfully")

        else:

            print("Account Not Found")





    elif choice == "8":

        account_number = input("Enter Account Number: ")

        cursor.execute(
            "SELECT TransactionType, Amount FROM Transactions WHERE AccountNumber = ?",
            (account_number,)
        )

        transactions = cursor.fetchall()

        if len(transactions) == 0:

            print("No Transactions Found")

        else:

            print("\n------ Transaction History ------")

            for transaction in transactions:

                print("Transaction Type :", transaction[0])
                print("Amount           :", transaction[1])
                print("------------------------------")




    elif choice == "9":

        print("\n------ Login ------")

        account_number = input("Enter Account Number: ")
        password = input("Enter Password: ")

        password = hash_password(password)

        cursor.execute(
            "SELECT CustomerName, Role FROM Customers WHERE AccountNumber = ? AND Password = ?",
            (account_number, password)
        )

        user = cursor.fetchone()

        if user:

            logged_in = True
            current_role = user[1]
            current_account = account_number

            print("\nLogin Successful")
            print("Welcome", user[0])
            print("Role :", current_role)

        else:

            print("Invalid Account Number or Password")






    elif choice == "10":

        cursor.execute("""
        SELECT AccountNumber, CustomerName, Balance
        FROM Customers
        ORDER BY Balance DESC
        """)

        customers = cursor.fetchall()

        print("\n------ Customers Sorted By Balance ------")

        for customer in customers:

            print("----------------------------")
            print("Account Number :", customer[0])
            print("Customer Name  :", customer[1])
            print("Balance        :", customer[2])






    elif choice == "11":

        cursor.execute("SELECT * FROM Customers")

        customers = cursor.fetchall()

        workbook = Workbook()

        sheet = workbook.active

        sheet.append([
            "Customer ID",
            "Account Number",
            "Customer Name",
            "Phone Number",
            "Balance",
            "Role"
        ])

        for customer in customers:

            sheet.append([
                customer[0],
                customer[1],
                customer[2],
                customer[3],
                customer[5],
                customer[6]
            ])

        workbook.save("Customers.xlsx")

        import os

        print(os.path.abspath("Customers.xlsx"))

        print("Excel File Created Successfully")






    elif choice == "12":

        cursor.execute("SELECT * FROM Customers")

        customers = cursor.fetchall()

        data = [["ID", "Account", "Name", "Phone", "Balance", "Role"]]

        for customer in customers:

            data.append([
                customer[0],
                customer[1],
                customer[2],
                customer[3],
                customer[5],
                customer[6]
            ])

        pdf = SimpleDocTemplate("Customers.pdf")

        table = Table(data)

        pdf.build([table])

        print(os.path.abspath("Customers.pdf"))

        print("PDF File Created Successfully")



    elif choice == "0":

     if logged_in:

            logged_in = False
            current_role = ""
            current_account = ""

            print("\nLogged Out Successfully")

    else:

            print("\nThank You For Using Mini Bank System")

            conn.close()
            break


