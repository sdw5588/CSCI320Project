import psycopg2  # pip install psycorg2
import os
from time import sleep
from datetime import datetime, timedelta
from tabulate import tabulate
import random

NAME = 'PythonAPP'
conn = object


def show_all_users(uname):
    """
    Displays one or all users in the database.
    :param uname: uname of a specific user. If None, then displays all users.
    :return: the attributes of a specific user or all the users.
    """
    global conn
    cursor = conn.cursor()

    if uname is None:
        # Get a list of all users
        sql = '''
        SELECT "username", "first_name", "last_name" FROM "user"
        '''
    else:
        # Get a list of all users but the uname given
        sql = '''
        SELECT "username", "first_name", "last_name" FROM "user"
        WHERE "username" != %s
        '''

    cursor.execute(sql, (uname,))
    all_users = cursor.fetchall()

    print(' -- -- Users -- -- ')
    # print('--ID--', '-FIRST-', '-LAST-', sep='\t')
    uname_list = []
    f_name_list = []
    l_name_list = []
    i = 0
    for user in all_users:
        uname_list.append(user[0])
        f_name_list.append(user[1])
        l_name_list.append(user[2])
        # print(id_list[i], fname_list[i], lname_list[i], sep='\t')
        i += 1

    print(tabulate(all_users, headers=['USRNAME', 'FIRST', 'LAST']))
    print(' -- -- ')

    return uname_list, f_name_list, l_name_list


def add_tool(uname, toolname):
    """
    Add a tool to be owned by a user.
    :param uname: username of user getting a new tool.
    :return: None
    """
    global conn
    cursor = conn.cursor()

    # Get a lits of all tool barcodes
    sql = '''
    SELECT "barcode" FROM "tool"
    '''
    cursor.execute(sql)
    all_barcodes = cursor.fetchall()

    # Gotta make sure barcodes are not reused
    valid_barcode = False
    while not valid_barcode:

        try:
            barcode = random.randrange(1, 9999, 1)

            if len(all_barcodes) == 0:
                valid_barcode = True

            for bc in all_barcodes:
                # print(bc[0])
                if bc[0] == barcode:
                    print('That barcode already exists!')
                    valid_barcode = False
                    break
                else:
                    valid_barcode = True
        except ValueError:
            print('Barcode must be numeric...')
            pass

    lendable = True

    # Get a list of all categories
    sql = '''
    SELECT "cat_name" FROM "category"
    '''
    cursor.execute(sql)
    all_cats = cursor.fetchall()  # look at this cat --> (,,,)=(^..^)=(,,,)

    print(' -- Existing Categories are -- ')
    cat_list = []
    new_cat = True
    for cat in all_cats:
        cat_list.append(cat[0])
        print(cat[0])
    print(' -- -- ')

    category = ''
    print(toolname)
    while len(category) == 0:
        category = input('\nEnter cat_name\nIf that category does not exist it will be made : ').strip().lower()

    if category in cat_list:
        new_cat = False

    # Add to tool table
    sql = '''
    INSERT INTO "tool" ("barcode", "name", "lendable")
    VALUES (%s, %s, %s)
    '''
    cursor.execute(sql, (barcode, toolname, lendable))

    if new_cat:
        # add in new category
        sql = '''
        INSERT INTO "category" ("cat_name")
        VALUES (%s)
        '''
        cursor.execute(sql, (category,))

    # add in category relation
    sql = '''
    INSERT INTO "is_in" ("cat_name", "barcode")
    VALUES (%s, %s)
    '''
    cursor.execute(sql, (category, barcode))

    if uname != '':  # you can use the function to add non-owned tools :)

        buy_date = datetime.now()

        sql = '''
        INSERT INTO "owns" ("username", "barcode", "buy_date")
        VALUES (%s, %s, %s)
        '''
        cursor.execute(sql, (uname, barcode, buy_date))

    cursor.close()

    print('...Tool successfully added')
    sleep(.7)
    os.system('cls')

"""
Looks in creds.txt for username and password and connects to the database.
Enters the main loop for the program afterwards.
:return:
"""

# you need to make a file called creds.txt with the username on the first line and password on the next one
# f = open("creds.txt", "r")
usr = "p320_26"
passwd = "eewier5eix2ag3ohChoo"
# print("dbname="+ usr + " user= " + usr + " password=" + passwd + " host=reddwarf.cs.rit.edu", sep = "")

conn = psycopg2.connect("dbname=" + usr + " user=" + usr + " password=" + passwd + " host=reddwarf.cs.rit.edu")
print("Connected with " + conn.dsn)
os.system('cls')


with open("tools.txt") as f:
    content = f.readlines()
# you may also want to remove whitespace characters like `\n` at the end of each line
content = [x.strip() for x in content]

print(content)


uname_list, f_name_list, l_name_list = show_all_users(None)

print(random.randrange(1, 9999, 1))

for tool in content:
    user = random.choice(uname_list)
    add_tool(user, tool)


conn.commit()

conn.close()
