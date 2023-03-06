import pandas as pd
import mysql.connector as sql


# Connect to the database
db_connection = sql.connect( host='192.168.1.21',
                             database='Logs_fw', 
                             user='root', 
                             password='mypass123')


# Create a cursor object
db_cursor = db_connection.cursor()

# Execute the query
db_cursor.execute('SELECT * FROM FW')

# Fetch all the records
table_rows = db_cursor.fetchall()

# Close the cursor
db_cursor.close()

# Close the database connection
db_connection.close()

# Create a dataframe from the database table
dfdb = pd.DataFrame(table_rows)
dfdb.columns=['date', 'ipsrc', 'ipdst', 'port','proto', 'action', 'policyid']