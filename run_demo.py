import sqlite3
import datetime

def setup_database(cursor):
    print("--- Setting up Database Schema (SQLite Adaptation) ---")
    
    # 1. Customers
    cursor.execute('''
        CREATE TABLE Customers (
            CustomerID INTEGER PRIMARY KEY AUTOINCREMENT,
            FirstName TEXT,
            LastName TEXT,
            Email TEXT,
            Phone TEXT,
            Country TEXT,
            RegistrationDate TEXT
        )
    ''')

    # 2. Products
    cursor.execute('''
        CREATE TABLE Products (
            ProductID INTEGER PRIMARY KEY AUTOINCREMENT,
            ProductName TEXT,
            Category TEXT,
            Price REAL,
            StockQuantity INTEGER,
            IsActive INTEGER
        )
    ''')

    # 3. Orders
    cursor.execute('''
        CREATE TABLE Orders (
            OrderID INTEGER PRIMARY KEY AUTOINCREMENT,
            CustomerID INTEGER,
            OrderDate TEXT,
            TotalAmount REAL,
            Status TEXT,
            FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID)
        )
    ''')

    # 4. OrderDetails
    cursor.execute('''
        CREATE TABLE OrderDetails (
            OrderDetailID INTEGER PRIMARY KEY AUTOINCREMENT,
            OrderID INTEGER,
            ProductID INTEGER,
            Quantity INTEGER,
            UnitPrice REAL,
            FOREIGN KEY (OrderID) REFERENCES Orders(OrderID),
            FOREIGN KEY (ProductID) REFERENCES Products(ProductID)
        )
    ''')
    print("Tables created successfully.\n")

def insert_sample_data(cursor):
    print("--- Inserting Sample Data ---")
    
    # Customers
    customers = [
        ('John', 'Smith', 'john.smith@gmail.com', '555-0100', 'USA', '2023-01-15'),
        ('Jane', 'Doe', 'jane.doe@yahoo.com', '555-0101', 'UK', '2023-02-20'),
        ('Bob', 'Jones', 'bob.jones@gmail.com', '555-0102', 'USA', '2024-03-10')
    ]
    cursor.executemany("INSERT INTO Customers (FirstName, LastName, Email, Phone, Country, RegistrationDate) VALUES (?, ?, ?, ?, ?, ?)", customers)

    # Products
    products = [
        ('Laptop', 'Electronics', 1200.00, 50, 1),
        ('Mouse', 'Electronics', 25.00, 200, 1),
        ('Keyboard', 'Electronics', 45.00, 150, 1)
    ]
    cursor.executemany("INSERT INTO Products (ProductName, Category, Price, StockQuantity, IsActive) VALUES (?, ?, ?, ?, ?)", products)

    # Orders (Dates in ISO format for SQLite sorting)
    orders = [
        (1, '2024-01-15 10:00:00', 1225.00, 'Completed'), # John Smith
        (2, '2024-05-20 14:30:00', 45.00, 'Shipped'),     # Jane Doe
        (1, '2023-12-01 09:00:00', 1200.00, 'Completed')  # John Smith (Old order)
    ]
    cursor.executemany("INSERT INTO Orders (CustomerID, OrderDate, TotalAmount, Status) VALUES (?, ?, ?, ?)", orders)

    # Order Details
    order_details = [
        (1, 1, 1, 1200.00), # Laptop
        (1, 2, 1, 25.00),   # Mouse
        (2, 3, 1, 45.00),   # Keyboard
        (3, 1, 1, 1200.00)  # Laptop
    ]
    cursor.executemany("INSERT INTO OrderDetails (OrderID, ProductID, Quantity, UnitPrice) VALUES (?, ?, ?, ?)", order_details)
    print("Sample data inserted.\n")

def run_queries(cursor):
    print("--- Running Simulated Queries ---")

    # Query 1: Email Search (Optimized logic adapted for SQLite)
    print("1. Searching for '@gmail.com' customers:")
    cursor.execute("SELECT FirstName, Email FROM Customers WHERE Email LIKE '%@gmail.com'")
    rows = cursor.fetchall()
    for row in rows:
        print(f"   Found: {row[0]} ({row[1]})")
    
    # Query 2: Sales Aggregation (Date Range)
    print("\n2. Total Sales for 2024:")
    # SQLite doesn't have YEAR(), using strftime or string comparison
    cursor.execute("SELECT SUM(TotalAmount) FROM Orders WHERE OrderDate >= '2024-01-01' AND OrderDate < '2025-01-01'")
    result = cursor.fetchone()[0]
    print(f"   Total Sales: ${result:,.2f}")

    # Query 3: Join for 'Smith'
    print("\n3. Order History for 'Smith':")
    cursor.execute('''
        SELECT c.FirstName, c.LastName, o.OrderDate, p.ProductName
        FROM Customers c
        JOIN Orders o ON c.CustomerID = o.CustomerID
        JOIN OrderDetails od ON o.OrderID = od.OrderID
        JOIN Products p ON od.ProductID = p.ProductID
        WHERE c.LastName = 'Smith'
    ''')
    rows = cursor.fetchall()
    for row in rows:
        print(f"   {row[0]} {row[1]} ordered {row[3]} on {row[2]}")

def main():
    # Connect to in-memory database
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()
    
    setup_database(cursor)
    insert_sample_data(cursor)
    run_queries(cursor)
    
    conn.close()

if __name__ == "__main__":
    main()
