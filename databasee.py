import sqlite3

conn = sqlite3.connect("MiniBank.db")
cursor = conn.cursor()

# Customers Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS Customers(

    CustomerID INTEGER PRIMARY KEY AUTOINCREMENT,
    AccountNumber TEXT UNIQUE,
    CustomerName TEXT,
    PhoneNumber TEXT,
    Password TEXT,
    Balance REAL,
    Role TEXT

)
""")

# Transactions Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS Transactions(

    TransactionID INTEGER PRIMARY KEY AUTOINCREMENT,
    AccountNumber TEXT,
    TransactionType TEXT,
    Amount REAL,
    Date TIMESTAMP DEFAULT CURRENT_TIMESTAMP

)
""")

conn.commit()

print("Database Created Successfully")
print("Tables Created Successfully")

conn.close()