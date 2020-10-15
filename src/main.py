import psycopg2  # pip install psycorg2
import random
import os
from time import sleep
import datetime
from tabulate import tabulate

#TESTING AGAIN FOR GIT VIA CMD

NAME = 'PythonAPP'
conn = object


def main():
    global conn

    # you need to make a file called creds.txt with the username on the first line and password on the next one
    f = open("creds.txt", "r")
    usr = f.readline().strip()
    passwd = f.readline().strip()
    # print("dbname="+ usr + " user= " + usr + " password=" + passwd + " host=reddwarf.cs.rit.edu", sep = "")

    conn = psycopg2.connect("dbname=" + usr + " user=" + usr + " password=" + passwd + " host=reddwarf.cs.rit.edu")
    print("Connected with " + conn.dsn)
    os.system('cls')

    # now we can start the PythonAPP

    # addTest(conn, random.randint(100, 1000), 'This was done by a robot', 'PythonAPP', True)
    #get_user_name()

    start()

    conn.close()


###############################################################################
#                        MAIN MENU ITEMS
###############################################################################


def show_main_menu():
    print(' -- -- -- -- MAIN MENU -- -- -- -- ')
    print(' 0. Exit')
    print(' 1. Register User')
    print(' 2. User Menu')
    print(' 3. Browse Tools')
    print(' 4. List Users')
    print(' -- -- -- -- -- -- -- -- -- -- ')


def start():
    while True:
        os.system('cls')
        show_main_menu()
        try:
            n = int(input('Enter option : '))
        except ValueError:
            n = -1
        if n == 0:
            os.system('cls')
            print(' -- -- -- Thank You -- -- -')
            exit(0)
        # register user
        elif n == 1:
            os.system('cls')
            register_user()
        # User Menu
        elif n == 2:
            os.system('cls')
            get_user_name()
        # Browse tools by: all / category / collection
        elif n == 3:
            os.system('cls')
        # List Users
        elif n == 4:
            os.system('cls')
            show_all_users(None)  # if an id is specified it shows all but that id
            input('Press Enter to continue...')
        else:
            os.system('cls')


def register_user():
    global conn
    cursor = conn.cursor()

    # Get a lits of all usernames
    sql = '''
    SELECT "username" FROM "user"
    '''
    cursor.execute(sql)
    all_uname = cursor.fetchall()
    # Gotta make sure unames arent reused
    valid_uname = False

    while not valid_uname:
        usr_name = input('Enter username : ').strip()

        if len(all_uname) == 0:
            valid_uname = True

        for uname in all_uname:
            # print(uid[0])
            if uname[0] == usr_name:
                print('That username already exists!')
                break
            else:
                valid_uname = True

    f_name = input('Enter user first_name : ').strip()
    l_name = input('Enter user last_name : ').strip()

    sql = '''
    INSERT INTO "user" ("username", "first_name", "last_name")
    VALUES (%s, %s, %s)
    '''
    cursor.execute(sql, (usr_name, f_name, l_name))
    conn.commit()
    print("...User added successfully!")
    sleep(.7)
    cursor.close()


def show_all_users(uname):
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

###############################################################################
#                         USER MENU
###############################################################################


def get_user_name():

    uname_list, f_name_list, l_name_list = show_all_users(None)

    while True:
        global conn
        cursor = conn.cursor()

        usr_name = input('Enter your username : ')

        print(usr_name)
        print(uname_list)

        sql = '''
        SELECT "first_name", "last_name" FROM "user"
        WHERE "username"=%s;
        '''
        cursor.execute(sql, (usr_name,))
        name = cursor.fetchall()

        print(name)

        if len(name) == 1:
            cursor.close()
            user_menu(usr_name, name[0])
            return
        else:
            print('Please enter a valid username')


def show_user_menu():
    print(' -- -- -- User Menu -- -- -- ')
    print(' 0. Back')
    print(' 1. Add Tool')
    print(' 2. Edit Tool')
    print(' 3. View your Tools')
    print(' 4. View your Collections')
    print(' -- -- -- -- -- -- -- -- -- -- ')


def user_menu(uname, user_name): # oof thats a little confusing isnt it
    while True:
        os.system('cls')
        print('Hello,', user_name[0])
        show_user_menu()
        try:
            n = int(input('Enter option : '))
        except ValueError:
            n = -1
        # exit
        if n == 0:
            os.system('cls')
            return
        # add tool
        elif n == 1:
            os.system('cls')
            add_tool(uname)
        # edit tool
        elif n == 2:
            os.system('cls')
            edit_tool(uname)
        # View my Tools
        elif n == 3:
            os.system('cls')
            view_tools(uname)
            input('Press Enter to return...')
        # View my collections
        elif n == 4:
            os.system('cls')
            show_collections(uname)
        else:
            os.system('cls')


def add_tool(uname):
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
        barcode = int(input('Enter tool barcode : '))

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

    name = input('Enter tool name : ').strip()
    lendable_in = input('Is the tool lendable? (y/n): ')
    if lendable_in == "n":
        lendable = False
    else:
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

    category = input('\nEnter cat_name\nIf that category does not exist it will be made : ').strip().lower()

    if category in cat_list:
        new_cat = False

    # Add to tool table
    sql = '''
    INSERT INTO "tool" ("barcode", "name", "lendable")
    VALUES (%s, %s, %s)
    '''
    cursor.execute(sql, (barcode, name, lendable))

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

        buy_date = datetime.datetime.now()

        sql = '''
        INSERT INTO "owns" ("username", "barcode", "buy_date")
        VALUES (%s, %s, %s)
        '''
        cursor.execute(sql, (uname, barcode, buy_date))

    conn.commit()
    cursor.close()

    print('...Tool successfully added')
    sleep(.7)


def view_tools(usr_id):
    global conn
    cursor = conn.cursor()

    if usr_id is None: # does not work yet
        # Show all tools
        sql = '''
        SELECT "username", "barcode", "name", "lendable" FROM "tool"
        '''
        print(' -- -- ALL TOOLS -- -- ')
    else:
        # Get a list of the User's Owned Tools
        sql = '''
        SELECT "barcode", "name", "lendable" FROM "tool"
        WHERE "barcode" IN (
            SELECT "barcode" FROM "owns"
            WHERE "username" = %s AND "sold_date" IS NULL
        );
        '''
        print(' -- -- YOUR TOOLS -- -- ')

    cursor.execute(sql, (usr_id,))
    tools = cursor.fetchall()

    # Print out the users tools
    barcodes = []  # their barcodes
    tool_names = []
    lend_list = []

    for tool in tools:
        # print(tool[0], tool[1], tool[2], sep='\t')
        barcodes.append(tool[0])
        tool_names.append(tool[1])
        lend_list.append(tool[2])

    print(tabulate(tools, headers=['BARCODE', 'NAME', 'LEND']))
    print(' -- -- ')

    return barcodes, tool_names, lend_list

def show_collections(uname):
    global conn
    cursor = conn.cursor()

    # Get a list of all collections
    sql = '''
    SELECT "coll_name" FROM "collection"
    '''
    cursor.execute(sql)
    all_colls = cursor.fetchall()

    print(' -- Existing Collections are -- ')
    coll_list = []
    new_coll = True
    for coll in all_colls:
        coll_list.append(coll[0])
    print(tabulate(coll_list, headers=['COLLECTION NAME']))
    print(' -- -- ')

def show_tools_in_coll(uname):
    global conn
    cursor = conn.cursor()

    show_collections(uname)

    coll_name = input('Enter the collection name to see tools in it : ').strip()

    sql = '''
    SELECT "username", "barcode" FROM "owns"
    WHERE "collection" = %s
    '''
    cursor.execute(sql, (collection,))

    coll_tools = cursor.fetchall()

    print(coll_tools)







###############################################################################
#                         EDIT TOOL SUB MENU
###############################################################################


def edit_tool(uname):
    global conn

    cursor = conn.cursor()

    selected_tool = False

    barcodes, tool_names, lend_list = view_tools(uname)

    while not selected_tool:

        try:
            barcode = int(input('Enter the tool barcode to edit : '))
        except ValueError:
            barcode = ''
            print('Please enter a number...')


        if barcode in barcodes:
            # Its actually their tool
            cursor.close()
            tool_edit(uname, barcode, tool_names[barcodes.index(barcode)], lend_list[barcodes.index(barcode)])
            selected_tool = True
        else:
            # not their tool
            print('You dont own that tool, or it doesnt exist')


def show_tool_edit():
    print(' -- -- -- Tool EDITOR -- -- -- ')
    print(' 0. Back')
    print(' 1. Change Name')
    print(' 2. Lend Tool')
    print(' 3. Add to Collection')
    print(' 4. Add to Category')
    print(' 5. Sell')
    print(' -- -- -- -- -- -- -- -- -- -- ')


def tool_edit(uname, barcode, tool_name, lendable):
    os.system('cls')
    print('Editing:', tool_name)
    show_tool_edit()
    n = int(input('Enter option : '))
    if n == 0:
        os.system('cls')
    elif n == 1:  # change name
        os.system('cls')
        change_name(uname, barcode, tool_name)
    elif n == 2:  # Lend
        os.system('cls')
        lend(uname, barcode, tool_name, lendable)
    elif n == 3:  # add to collection
        os.system('cls')
        add_to_collection(uname, barcode, tool_name)
    elif n == 4:  # add to category
        os.system('cls')
        add_to_category(uname, barcode, tool_name)
    elif n == 5:  # sell
        os.system('cls')
        sell(uname, barcode, tool_name)
    else:
        os.system('cls')


def change_name(uname, barcode, tool_name):
    global conn
    cursor = conn.cursor()

    new_name = input('Whats the new name for ' + tool_name + ' : ')

    sql = '''
    UPDATE "tool"
    SET "name" = %s
    WHERE "barcode" = %s
    '''
    cursor.execute(sql, (new_name, barcode))

    conn.commit()

    print('...Update Successful')
    sleep(.7)
    cursor.close()


def lend(uname, barcode, tool_name, lendable):

    if not lendable:
        print(tool_name, 'is not marked as lendable, would you like to change this and lend anyways?')
        force_lend = input('\n(y/n): ')
        if force_lend[0] == 'y':
            pass
            # make_lendable(barcode)
        else:
            return

    uname_list, f_name_list, l_name_list = show_all_users(uname)

    correct_uname = False

    while not correct_uname:
        borrow_uname = input('Enter the username of the user to lend to : ').strip()

        if borrow_uname in uname_list:
            correct_uname = True
        else:
            print('That is not a valid username, try again...\n')


def add_to_collection(uname, barcode, tool_name):
    global conn
    cursor = conn.cursor()

    collection = input('\nEnter collection name\nIf that collection does not exist it will be made : ').strip()

    if collection in coll_list:
        new_coll = False

    if new_coll:
        # add in new collection
        sql = '''
        INSERT INTO "collection" ("coll_name")
        VALUES (%s)
        '''
        cursor.execute(sql, (collection,))

    # add in collection relation
    sql = '''
    UPDATE "owns"
    SET "collection" = %s
    WHERE "user_id" = %s AND "barcode" = %s;
    '''
    cursor.execute(sql, (collection, usr_id, barcode))
    conn.commit()
    print('...Successfully Added')
    sleep(.7)
    cursor.close()


def add_to_category(uname, barcode, tool_name):
    global conn
    cursor = conn.cursor()

    # Get a list of all categories
    # Also this is a copy of code in the Add tool func, because i dont want to write a function to do it
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

    category = input('\nEnter cat_name\nIf that category does not exist it will be made : ').strip()

    if category in cat_list:
        new_cat = False

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
    conn.commit()
    print('...Successfully Added')
    sleep(.7)
    cursor.close()


def sell(uname, barcode, tool_name):
    # TODO: Write the function
    pass

###############################################################################
#                         OLD FUNCTIONS / DEBUGGING
###############################################################################


def add_test(conn, id, info, owner, rented):
    # where the fun begins
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO "TestTable" ("username", "Information", "Owner", "Rented")
    VALUES (%s, %s, %s, %s)
    """, (id, info, owner, rented))

    conn.commit()
    cur.close()

    print("Added an entry to testTable")


def get_from_table():
    global conn
    cursor = conn.cursor()

    sql = '''
    SELECT * FROM "TestTable"
    '''
    cursor.execute(sql)

    items = cursor.fetchall()
    i = 0
    for item in items:
        print(item[0], item[1])
    exit()


if __name__ == '__main__':
    main()
