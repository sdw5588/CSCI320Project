import psycopg2  # pip install psycorg2
import random
import os
from time import sleep
import datetime

NAME = 'PythonAPP'
conn = object

def main():
    global conn

    f = open("creds.txt", "r")
    usr = f.readline().rstrip()
    passwd = f.readline().rstrip()
    #print("dbname="+ usr + " user= " + usr + " password=" + passwd + " host=reddwarf.cs.rit.edu", sep = "")

    conn = psycopg2.connect("dbname="+ usr + " user= " + usr + " password=" + passwd + " host=reddwarf.cs.rit.edu")
    print("Connected with " + conn.dsn)

    # now we can start the PythonAPP

    #addTest(conn, random.randint(100, 1000), 'This was done by a robot', 'PythonAPP', True)
    #getFromTable()

    start()

    conn.close()


def showMainMenu():
    print(' -- -- -- -- MENU -- -- -- -')
    print(' 0. Exit')
    print(' 1. Register User')
    print(' 2. User Menu')
    print(' -- -- -- -- -- -- -- -- -- -- ')

def start():
    os.system('cls')
    showMainMenu()
    n = int(input('Enter option : '))
    if n == 0:
        os.system('cls')
        print(' -- -- -- Thank You -- -- -')
    elif n == 1:
        os.system('cls')
        registerUser()
    elif n == 2:
        os.system('cls')
        getUserName()
    else:
        os.system('cls')
        start()

def registerUser():
    global conn

    id = input('Enter user id : ')
    fname = input('Enter user first_name : ')
    lname = input('Enter user last_name : ')

    cursor = conn.cursor()
    sql = '''
    INSERT INTO "user" ("id", "first_name", "last_name")
    VALUES (%s, %s, %s)
    '''
    cursor.execute(sql, (id, fname, lname))
    conn.commit()
    print("...User added successfully!")
    sleep(.5)
    start()


def showUserMenu():
    print(' -- -- -- User MENU -- -- -')
    print(' 0. Exit')
    print(' 1. Add Tool')
    print(' -- -- -- -- -- -- -- -- -- -- ')



def getUserName():
    global conn
    cursor = conn.cursor()

    id = input('Enter your user id : ')

    sql = '''
    SELECT "first_name", "last_name" FROM "user"
    WHERE "id"=%s;
    '''
    cursor.execute(sql, (id,))
    name = cursor.fetchall()

    if len(name) == 1:
        userMenu(id, name)
    else:
        print('Please enter a valid user_id')
        getUserName()


def userMenu(id, user_name):
    os.system('cls')
    print('Hello,', user_name[0])
    showUserMenu()
    n = int(input('Enter option : '))
    if n == 0:
        os.system('cls')
        print(' -- -- -- Thank You -- -- -')
    elif n == 1:
        os.system('cls')
        addTool(id)
    else:
        os.system('cls')
        start()



def addTool(id):
    global conn

    barcode = input('Enter tool barcode : ')
    name = input('Enter tool name : ')
    lend = input('Is the tool lendable? (y/n): ')
    if lend == "n":
        lend = False
    else:
        lend == True
    # category = input('Enter cat_name\nOr n for no category : ')

    cursor = conn.cursor()

    sql ='''
    INSERT INTO "tool" ("barcode", "name", "lendable")
    VALUES (%s, %s, %s)
    '''
    cursor.execute(sql, (barcode, name, lend))

    # if category != "n":
    #     sql ='''
    #     INSERT INTO "category" ("cat_name")
    #     VALUES (%s)
    #     '''
    #     cursor.execute(sql, (category,))
    #     sql ='''
    #     INSERT INTO "is_in" ("cat_name", "barcode")
    #     VALUES (%s, %s)
    #     '''
    #     cursor.execute(sql, (category, barcode))

    if id != '':# you can use the function to add non-owned tools :)

        buy_date = datetime.datetime.now()

        sql ='''
        INSERT INTO "owns" ("user_id", "barcode", "buy_date")
        VALUES (%s, %s, %s)
        '''
        cursor.execute(sql, (id, barcode, buy_date))

    conn.commit()



def addTest(conn, id, info, owner, rented):
    # where the fun begins
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO "TestTable" ("id", "Information", "Owner", "Rented")
    VALUES (%s, %s, %s, %s)
    """, (id, info, owner, rented))

    conn.commit()
    cur.close()

    print("Added an entry to testTable")


def getFromTable():
    global conn
    cursor = conn.cursor()

    sql = '''
    SELECT * FROM "TestTable"
    '''
    cursor.execute(sql)

    list = cursor.fetchall()
    i = 0
    for item in list:
        print(item[0], item[1])
    exit()

if __name__ == '__main__':
    main()
