import pandas as pd
import pandasql as ps
from datetime import datetime
import pickle
import joblib
import mysql.connector as sql


db_connection = sql.connect(host='192.168.1.21', database='Logs_fw', user='root', password='mypass123')
db_cursor = db_connection.cursor()
db_cursor.execute('SELECT * FROM FW')
table_rows = db_cursor.fetchall()
db = pd.DataFrame(table_rows)
db.columns=['date', 'ipsrc', 'ipdst', 'port','proto', 'action', 'policyid']
