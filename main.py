import pyodbc
import pandas as pd

#The following comment lines are the code I used to run this program on my machine. I have implemented user input for these variables to connect to your database.
#SERVER = 'Thweps\\SQLEXPRESS'
#DATABASE = 'KnightHardwareCo'
#USERNAME = 'sa'
#PASSWORD = '#################'
#connectionString = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={SERVER};DATABASE={DATABASE};UID={USERNAME};PWD={PASSWORD}'
#conn = pyodbc.connect(connectionString)
#cursor = conn.cursor()

def main():
#Part 1: Select statement, conditional handles user input and query selection, loop handles input validation
    print('''You are the new CEO at Knight Hardware Co.\n
You will be working with me, your database administrator, to make decisions related to the business and have those decisions reflected in the company database.''')
    input('Please make sure you have executed the file called knight_hardware_db.sql in SQL Server Management Studio. (Enter to continue)')

#Connection setup
    SERVER = input('Please paste in your server name in SSMS: ')
    DATABASE = 'KnightHardwareCo'
    USERNAME = input('Please enter your SSMS username: ')
    PASSWORD = input('Please enter your SSMS password: ')
    connectionString = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={SERVER};DATABASE={DATABASE};UID={USERNAME};PWD={PASSWORD}'
    conn = pyodbc.connect(connectionString)
    
    print('''\nFirst, we will need to get you an overview of the company\'s most important sources of revenue.\nWe will take a look at the total revenue from each product ordered, 
as well as the customer that ordered it, how many were ordered, the inventory on hand, and the unit price.\n''')
    choice = ''
    while choice != '1' and choice != '2':
        choice = input('Would you like this product revenue overview to be:\n1. Sorted purely by highest revenue\n2. Sorted alphabetically by customer\n(Enter 1 or 2): ')
        if choice == '1':
            selectquery1(conn)
        elif choice == '2':
            selectquery2(conn)
        else:
            print("Invalid selection. Please enter 1 or 2.")

    input('\nGreat! Now that you have a bird\'s eye view of the business, you\'ll be ready for whatever comes up in the future. (Press Enter to continue)')

#Part 2: Insert statement, loop handles input validation, conditionals handle query selection and corresponding assignment of name, qty, inventory, partnumber variables for Part 3
    print('\nThree weeks later...\n\nBoss! We have two potential new customers, but we only have one available sales rep to handle their orders.')
    choice =''
    while choice != '1' and choice != '2':
        print('\nWesley Appliance Shop is owned by a friend of Al from Al\'s Appliance and Sport. \nBestWare is a subsidiary of Johnson\'s Department Store.')
        print('\nBased on these customers providing similar revenue as their connections to us, which customer should we take on?\n')
        choice = input('1. Wesley Appliance Shop\n2. BestWare\n(Enter 1 or 2): ')
        if choice == '1':
            name = 'Wesley Appliance Shop'
            qty = 51
            product = 'Irons'
            inv = 50
            part_number = 'AT94'
            insertquery(conn, '708', 'Wesley Appliance Shop', 'Wesley', 'FL')
        elif choice == '2':
            name = 'BestWare'
            qty = 10
            product = 'Treadmills'
            inv = 9
            part_number = 'KV29'
            insertquery(conn, '709', 'BestWare', 'Northfield', 'FL')
        else:
            print("Invalid selection. Please enter 1 or 2.")
    input(f'Great! {name} is thrilled for us to serve them. I\'ve added them to the Customers table of our database. (Press Enter to continue)')

#Part 3: Update statement, loop handles input validation for a positive number, try catch blocks handle int conversion, new_quantity is current inventory plus amount ordered
    print(f'\nTwo days later...\n\nBoss! {name} just called to let us know that they will be ordering {qty} {product}. I just checked, and we only have {inv} {product} on hand!')
    choice2 = 0
    while choice2 <= 0:
        try:
            choice2 = int(input(f'How many {product} should we order for inventory?\nWe\'ll need at least one, but how many more is up to you.(Enter a number greater than 0): '))
        except ValueError:
            print('Invalid input. Please enter a valid number.')
    new_quantity = str(inv + choice2)
    updatequery(conn, new_quantity, part_number)
    input(f"Great! I've updated our Inventory to reflect that we will now have {new_quantity} total {product}. (Press Enter to continue)")

#Part 4: Delete statement
    print(f'\nSix months later...\n\nBoss! It\'s been a while. {name} received their {product} and was happy enough to have ordered more since, but they are unexpectedly closing down.')
    print(f'I just need you to give me the OK to delete {name} from our company database. It will free up resources for some new customers I need to add.')
    input('(Press Enter to give approval)')
    deletequery(conn, name)

#Conclusion
    print('Excellent! Well thanks for all your help boss! Today is my last day before retiring. Best of luck to you and Knight Hardware Co.!')

    conn.close()


#Returns Customer Name, Part Number, Part Description, Inventory On Hand, Unit Price, Number Ordered, and Total Price ordered by Total Price
def selectquery1(conn):
    cursor = conn.cursor()
    query1 = """
    SELECT c.CustomerName, p.PartNumber, PartDescription, InventoryOnHand, Price AS UnitPrice, NumberOrdered, NumberOrdered*Price AS TotalPrice
    FROM Parts p
    JOIN OrderDetails od ON p.PartNumber = od.PartNumber
    JOIN Orders o ON o.OrderNumber = od.OrderNumber
    JOIN Customers c ON c.CustomerNumber = o.CustomerNumber
    ORDER BY TotalPrice DESC;"""
    cursor.execute(query1)
    results = cursor.fetchall()
    processed_results = [
        (r[0], r[1], r[2], r[3], float(r[4]), r[5], float(r[6])) for r in results
    ]
    df = pd.DataFrame(processed_results, columns=["CustomerName","PartNumber","PartDescription","InventoryOnHand","UnitPrice","NumberOrdered","TotalPrice"])
    print(df.to_string(index=False))
    conn.commit()
    cursor.close()

#Returns Customer Name, Part Number, Part Description, Inventory On Hand, Unit Price, Number Ordered, and Total Price ordered by Customer Name
def selectquery2(conn):
    cursor = conn.cursor()
    query2 = """
    SELECT c.CustomerName, p.PartNumber, PartDescription, InventoryOnHand, Price AS UnitPrice, NumberOrdered, NumberOrdered*Price AS TotalPrice
    FROM Parts p
    JOIN OrderDetails od ON p.PartNumber = od.PartNumber
    JOIN Orders o ON o.OrderNumber = od.OrderNumber
    JOIN Customers c ON c.CustomerNumber = o.CustomerNumber
    ORDER BY CustomerName, TotalPrice DESC;"""
    cursor.execute(query2)
    results = cursor.fetchall()
    processed_results = [
        (r[0], r[1], r[2], r[3], float(r[4]), r[5], float(r[6])) for r in results
    ]
    df = pd.DataFrame(processed_results, columns=["CustomerName","PartNumber","PartDescription","InventoryOnHand","UnitPrice","NumberOrdered","TotalPrice"])
    print(df.to_string(index=False))
    conn.commit()
    cursor.close()

#Inserts the arguments passed as CustomerNumber, CustomerName, City, and State respectively as a new row in the Customers table
def insertquery(conn, customernumber, customername, city, state):
    cursor = conn.cursor()
    insertquery = '''
    INSERT INTO Customers
    VALUES (''' + customernumber + ',\'' + customername +'\',\'' + city + '\',\'' + state + '\')'
    cursor.execute(insertquery)
    conn.commit()
    cursor.close()
    
#Updates the InventoryOnHand for a specific part_number in the Parts table to a new_quantity passed in as arguments
def updatequery(conn, new_quantity, part_number):
    cursor = conn.cursor()
    updatequery = '''
    UPDATE Parts
    SET InventoryOnHand = ''' + new_quantity + 'WHERE PartNumber = \'' + part_number + '\''
    cursor.execute(updatequery)
    conn.commit()
    cursor.close()

#Deletes the Customer row for a given customername provided as an argument
def deletequery(conn, customername):
    cursor = conn.cursor()
    deletequery = '''
    DELETE FROM Customers
    WHERE CustomerName = \'''' + customername + '\''
    cursor.execute(deletequery)
    conn.commit()
    cursor.close()



if __name__ == '__main__':
    main()