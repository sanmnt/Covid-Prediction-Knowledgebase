import os
import sys
import pandas as pd
from sqlalchemy import create_engine
import mysql.connector as msql
from mysql.connector import Error
import csv

covidData = pd.read_csv('csv file location/website', index_col=False)
#needs delimiter at end of each line so index_col=FALSE
covidData.head()
df = covidData.head()
conn_params_dic = {
    "host"      : "SQL ip addresss",
    "database"  : "databasename",
    "user"      : "username",
    "password"  : "password"
}
def connect(conn_params_dic):
    conn = None
    try:
        print('Connecting to the MySQL...........')
        conn = msql.connect(**conn_params_dic)
        print("Connection successfully..................")

    except Error as err:
        print("Error while connecting to MySQL", err)
        # set the connection to 'None' in case of error
        conn = None
    return conn
# Using alchemy method
connect_alchemy = "mysql+pymysql://%s:%s@%s/%s" % (
    conn_params_dic['user'],
    conn_params_dic['password'],
    conn_params_dic['host'],
    conn_params_dic['database']
)

def using_alchemy():
    try:
        print('Connecting to the MySQL...........')
        engine = create_engine(connect_alchemy)
        print("Connection successfully..................")
    except Error as err:
        print("Error while connecting to MySQL", err)      
        # set the connection to 'None' in case of error
        engine = None
    return engine
def using_csv_reader(engine, datafrm, table_name):

    try:
        # Change your own path
        datafrm.to_csv('../CovidData/covid_bulk.csv', index=False)
        # dataframe columns with Comma-separated
        cols = ','.join(list(datafrm.columns))
        # SQL query to execute
        sql = "INSERT INTO %s(%s) VALUES(%%s,%%s,%%s,%%s,%%s,%%s,%%s,%%s,%%s,%%s,%%s,%%s,%%s,%%s,%%s,%%s,%%s,%%s,%%s,%%s,%%s,%%s,%%s,%%s,%%s,%%s,%%s,%%s,%%s,%%s,%%s,%%s,%%s,%%s,%%s,%%s,%%s,%%s,%%s,%%s,%%s,%%s,%%s,%%s,%%s)" % (table_name, cols)
        sql = sql.format(table_name)
        # Change your own path
        with open('../CovidData/covid_bulk.csv') as fh:
            reader = csv.reader(fh)
            next(reader)  # Skip firt line (headers)
            data = list(reader)
        engine.execute(sql, data)
        print("Data inserted using Using_csv_reader() successfully...")
    except Error as err:
        print("Error while inserting to MySQL", e)

conn = connect(conn_params_dic)
engine = using_alchemy()
using_csv_reader(engine, covidData, 'anon_data')
