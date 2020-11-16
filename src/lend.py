import psycopg2  # pip install psycorg2
import os
from time import sleep
from datetime import datetime, timedelta
from tabulate import tabulate
import random

NAME = 'PythonAPP'
conn = object

# you need to make a file called creds.txt with the username on the first line and password on the next one
# f = open("creds.txt", "r")
usr = "p320_26"
passwd = "eewier5eix2ag3ohChoo"
# print("dbname="+ usr + " user= " + usr + " password=" + passwd + " host=reddwarf.cs.rit.edu", sep = "")

conn = psycopg2.connect("dbname=" + usr + " user=" + usr + " password=" + passwd + " host=reddwarf.cs.rit.edu")
print("Connected with " + conn.dsn)
os.system('cls')

times = int(input("How many times to lend?"))
