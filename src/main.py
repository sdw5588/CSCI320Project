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
    print(' -- -- -- -- MAIN MENU -- -- -- -- ')
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
        exit(0)
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
    cursor = conn.cursor()

    # Get a lits of all user ids
    sql = '''
    SELECT "id" FROM "user"
    '''
    cursor.execute(sql)
    all_uid = cursor.fetchall()

    # Gotta make sure uids arent reused
    valid_uid = False
    while valid_uid == False:
        id = int(input('Enter user id : '))

        for uid in all_uid:
            #print(uid[0])
            if uid[0] == id:
                print('That user_id already exists!')
                break
            else:
                valid_uid = True

    fname = input('Enter user first_name : ')
    lname = input('Enter user last_name : ')

    sql = '''
    INSERT INTO "user" ("id", "first_name", "last_name")
    VALUES (%s, %s, %s)
    '''
    cursor.execute(sql, (id, fname, lname))
    conn.commit()
    print("...User added successfully!")
    sleep(.5)
    start()

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
        userMenu(id, name[0])
    else:
        print('Please enter a valid user_id')
        getUserName()


def showUserMenu():
    print(' -- -- -- User Menu -- -- -- ')
    print(' 0. Back')
    print(' 1. Add Tool')
    print(' 2. Edit Tool')
    print(' 3. Add Collection')
    print(' -- -- -- -- -- -- -- -- -- -- ')


def userMenu(id, user_name):
    os.system('cls')
    print('Hello,', user_name[0])
    showUserMenu()
    n = int(input('Enter option : '))
    if n == 0:
        os.system('cls')
        start()
    elif n == 1:
        os.system('cls')
        addTool(id)
    elif n == 2:
        os.system('cls')
        editTool(id)
        print(user_name[0])
    else:
        os.system('cls')
        start()
    userMenu(id, user_name)



def addTool(id):
    global conn
    cursor = conn.cursor()

    # Get a lits of all tool barcodes
    sql = '''
    SELECT "barcode" FROM "tool"
    '''
    cursor.execute(sql)
    all_barcodes = cursor.fetchall()

    # Gotta make sure barcodes arent reused
    valid_barcode = False
    while valid_barcode == False:
        barcode = int(input('Enter tool barcode : '))

        for bc in all_barcodes:
            #print(bc[0])
            if bc[0] == barcode:
                print('That barcode already exists!')
                valid_barcode = False
                break
            else:
                valid_barcode = True

    name = input('Enter tool name : ')
    lend = input('Is the tool lendable? (y/n): ')
    if lend == "n":
        lend = False
    else:
        lend == True

    # Get a list of all categories
    sql = '''
    SELECT "cat_name" FROM "category"
    '''
    cursor.execute(sql)
    all_cats = cursor.fetchall() # look at this cat --> (,,,)=(^..^)=(,,,)

    print(' -- Existing Categories are -- ')
    cat_list = []
    new_cat = True
    for cat in all_cats:
        cat_list.append(cat[0])
        print(cat[0])
    print(' -- -- ')

    category = input('\nEnter cat_name\nIf that category does not exist it will be made : ')

    if category in cat_list:
        new_cat = False

    # Add to tool table
    sql ='''
    INSERT INTO "tool" ("barcode", "name", "lendable")
    VALUES (%s, %s, %s)
    '''
    cursor.execute(sql, (barcode, name, lend))

    if new_cat:
        # add in new category
        sql ='''
        INSERT INTO "category" ("cat_name")
        VALUES (%s)
        '''
        cursor.execute(sql, (category,))

    # add in category relation
    sql ='''
    INSERT INTO "is_in" ("cat_name", "barcode")
    VALUES (%s, %s)
    '''
    cursor.execute(sql, (category, barcode))

    if id != '':# you can use the function to add non-owned tools :)

        buy_date = datetime.datetime.now()

        sql ='''
        INSERT INTO "owns" ("user_id", "barcode", "buy_date")
        VALUES (%s, %s, %s)
        '''
        cursor.execute(sql, (id, barcode, buy_date))

    conn.commit()

def editTool(id):
    global conn

    cursor = conn.cursor()
    # Get a lits of the User's Owned Tools
    sql = '''
    SELECT "barcode", "name" FROM "tool"
    WHERE "barcode" IN (
        SELECT "barcode" FROM "owns"
        WHERE "user_id" = %s AND "sold_date" IS NULL
    );
    '''
    cursor.execute(sql, (id,))
    tools = cursor.fetchall()
    # Print out the users tools
    print('-- -- YOUR TOOLS -- --')
    barcodes = [] # their barcodes
    tool_names = []
    selected_tool = False

    for tool in tools:
        print(tool[0], tool[1], sep='\t')
        barcodes.append(tool[0])
        tool_names.append(tool[1])

    while selected_tool == False:
        barcode = int(input('Enter the tool barcode : '))

        if barcode in barcodes:
            # Its actually their tool
            toolEdit(id, barcode, tool_names[barcodes.index(barcode)])
            selected_tool = True
        else:
            #not their tool
            print('You dont own that tool, or it doesnt exist')





def showToolEdit():
    print(' -- -- -- Tool EDITOR -- -- -- ')
    print(' 0. Back')
    print(' 1. Change Name')
    print(' 2. Lend Tool')
    print(' 3. Add to Collection')
    print(' -- -- -- -- -- -- -- -- -- -- ')


def toolEdit(id, barcode, tool_name):
    os.system('cls')
    print('Editing:', tool_name)
    showToolEdit()
    n = int(input('Enter option : '))
    if n == 0:
        os.system('cls')
    elif n == 1: # change name
        os.system('cls')
    elif n == 2: # Lend
        os.system('cls')
    elif n == 3: # add to collection
        os.system('cls')
    else:
        os.system('cls')
        start()



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
