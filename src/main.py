"""
This program connects to our database and allows for all the necessary interactions.
Authors: Owen McClure, Shayne Winn, Joseph Saber, Bin Qiu
"""
import psycopg2  # pip install psycorg2
import os
from time import sleep
from datetime import datetime, timedelta
from tabulate import tabulate
import random

# The video for this is in the Phase 3 report and also here:
# ​https://www.youtube.com/watch?v=Tqb8EXflZdE

NAME = 'PythonAPP'
conn = object


def main():
    """
    Looks in creds.txt for username and password and connects to the database.
    Enters the main loop for the program afterwards.
    :return:
    """
    global conn

    # you need to make a file called creds.txt with the username on the first line and password on the next one
    # f = open("creds.txt", "r")
    usr = "p320_26"
    passwd = "eewier5eix2ag3ohChoo"
    # print("dbname="+ usr + " user= " + usr + " password=" + passwd + " host=reddwarf.cs.rit.edu", sep = "")

    conn = psycopg2.connect("dbname=" + usr + " user=" + usr + " password=" + passwd + " host=reddwarf.cs.rit.edu")
    print("Connected with " + conn.dsn)
    os.system('cls')

    # now we can start the PythonAPP

    # addTest(conn, random.randint(100, 1000), 'This was done by a robot', 'PythonAPP', True)
    start()

    conn.close()


###############################################################################
#                        MAIN MENU ITEMS
###############################################################################


def show_main_menu():
    """
    Displays the main menu.
    :return: None
    """
    print(' -- -- -- -- MAIN MENU -- -- -- -- ')
    print(' 0. Exit')
    print(' 1. Register User')
    print(' 2. User Menu')
    print(' 3. Browse Tools')
    print(' 4. List Users')
    print(' 5. Analytics')
    print(' -- -- -- -- -- -- -- -- -- -- ')


def start():
    """
    Gets input from the user from the main menu and takes appropriate action
    that input.
    :return: None
    """
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
            browse_tools()
        # List Users
        elif n == 4:
            os.system('cls')
            show_all_users(None)  # if an id is specified it shows all but that id
            input('Press Enter to continue...')
        elif n == 5:
            os.system('cls')
            analytics()
        else:
            os.system('cls')


def register_user():
    """
    Registers a new user into the database by getting input for required
    fields.
    :return: None
    """
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

        valid_uname = True
        if len(usr_name) == 0:
            valid_uname = False
            continue;
        for uname in all_uname:
            # print(uid[0])
            if uname[0] == usr_name:
                print('That username already exists!')
                valid_uname = False
                break
    f_name = ''
    while len(f_name) == 0:
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

    print(tabulate(all_users, headers=['USERNAME', 'FIRST', 'LAST']))
    print(' -- -- ')

    return uname_list, f_name_list, l_name_list


def browse_tools():
    """
    Display the tool menu and executes appropriate command.
    :return: None
    """
    while True:
        os.system('cls')
        print(' -- -- -- ALL TOOL MENU -- -- -- ')
        print(' 0. Exit')
        print(' 1. View By Category')
        print(' 2. View By Collection')
        print(' 3. View All Tools')
        print(' -- -- -- -- -- -- -- -- -- -- ')

        try:
            n = int(input('Enter option : '))
        except ValueError:
            n = 0
        if n == 0:
            return
        elif n == 1:
            #by cat
            tools_by_cat()
        elif n == 2:
            #by coll
            tools_by_coll()
        elif n == 3:
            #all
            print_tool_table(view_tools(None)[0])


def print_tool_table(barcodes):
    """
    Prints the relevant information for all tools whose barcode is listed.
    :param barcodes: barcodes of the users whose information to print.
    :return: None
    """
    os.system('cls')
    print('Getting Tool MEGA LIST...')
    table  = [get_tool_details(barcode) for barcode in barcodes]
    os.system('cls')
    print(tabulate(table, headers=['NAME', 'LENDABLE', 'OWNER', 'COLLECTION', 'CATEGORIES']))
    input(' -- -- \nPress Enter to continue...')


def tools_by_cat():
    """
    Prints the tools in a specific category.
    :return: None
    """
    os.system('cls')
    global conn
    cursor = conn.cursor()
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

    valid_choice = False
    while not valid_choice:
        category = input('\nEnter cat_name : ').strip().lower()

        if category in cat_list:
            valid_choice = True
        else:
            print('Thats not a valid category, try again...')

    sql='''
    SELECT "barcode" from "is_in"
    WHERE "cat_name"=%s
    '''
    cursor.execute(sql, (category,))
    all_barcodes = cursor.fetchall()
    barcodes = [barcode[0] for barcode in all_barcodes]
    print_tool_table(barcodes)


def tools_by_coll():
    """
    Print the tools in a specific collection.
    :return: None
    """
    os.system('cls')
    coll_list = show_collections(None)

    valid_choice = False
    while not valid_choice:
        collection = input('What Collection do you want to look in? : ').strip().lower()

        if collection in coll_list:
            valid_choice = True
        else:
            print('That collection does not exist. Please enter a valid collection...')

    bc_list = get_tools_in_coll(None, collection)

    print_tool_table(bc_list)

###############################################################################
#                         USER MENU
###############################################################################


def get_user_name():
    """
    Has user enter their username so they can log into their user menu.
    :return: None
    """
    uname_list, f_name_list, l_name_list = show_all_users(None)

    while True:
        global conn
        cursor = conn.cursor()

        usr_name = input('Enter your username : ')

        #print(usr_name)
        #print(uname_list)

        sql = '''
        SELECT "first_name", "last_name" FROM "user"
        WHERE "username"=%s;
        '''
        cursor.execute(sql, (usr_name,))
        name = cursor.fetchall()

        #print(name)

        if len(name) == 1:
            cursor.close()
            user_menu(usr_name, name[0])
            return
        else:
            print('Please enter a valid username')


def show_user_menu():
    """
    Display the user menu.
    :return: None
    """
    print(' -- -- -- User Menu -- -- -- ')
    print(' 0. Back')
    print(' 1. Add Tool')
    print(' 2. Edit Tool')
    print(' 3. View your Tools')
    print(' 4. View your Borrowed Tools')
    print(' 5. View your Collections')
    print(' 6. Recommended Tool')
    print(' -- -- -- -- -- -- -- -- -- -- ')


def user_menu(uname, user_name):
    """
    Gets input from the user on the user menu and execute appropriate command.
    :param uname: username of user.
    :param user_name: first name of user.
    :return: None
    """
    while True:
        os.system('cls')
        print('Hello,', user_name[0], user_name[1])
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
        # View my borrowed tools
        elif n == 4:
            os.system('cls')
            print_borrowed(view_borrowed(uname))
            input('Press Enter to return...')
        # View my collections
        elif n == 5:
            os.system('cls')
            view_collections(uname)
        elif n == 6:
            os.system('cls')
            recommend_tool(uname)
            input('Press Enter to return...')
        else:
            os.system('cls')


def add_tool(uname):
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
        except ValueError:
            print('Barcode must be numeric...')
            pass
    name = ''
    while len(name) == 0:
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

    category = ''
    while len(category) == 0:
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

        buy_date = datetime.now()

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
    """
    View tools of a specific user or all users.
    :param usr_id: If None, then display all tools. Otherwise, display
    tools of user with username as usr_id
    :return: list containing barcode, tool name, and who, if anyone, the tool(s)
    is currently being lent to.
    """
    global conn
    cursor = conn.cursor()

    if usr_id is None: # does work now
        # Show all tools
        sql = '''
        SELECT "barcode", "name", "lendable" FROM "tool"
        '''
        cursor.execute(sql, (usr_id,))
        tools = cursor.fetchall()
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
    """
    Print the collections of the tools of a specific user or all users.
    :param uname: if None, print for all users. Otherwise, print for user whose
    username is uname.
    :return: List of the collections
    """
    global conn
    cursor = conn.cursor()

    if uname == None:
        # Get a list of all collections
        sql = '''
        SELECT "coll_name" FROM "collection"
        '''
    else:
        #only show collections where a user has a tool in it
        sql = '''
        SELECT "coll_name" FROM "collection"
        WHERE "coll_name" IN (
            SELECT "collection" FROM "owns"
            WHERE "username" = %s
            AND "sold_date" IS NULL
            AND "rem_coll_date" IS NULL
        );
        '''
    cursor.execute(sql, (uname,))
    all_colls = cursor.fetchall()

    print(' -- Existing Collections are -- ')
    coll_list = []
    new_coll = True
    for coll in all_colls:
        coll_list.append(coll[0])
    print(tabulate(all_colls, headers=['COLLECTION NAME']))
    print(' -- -- ')

    return coll_list


def view_collections(uname):
    """
    Views the tools owned by a user in a collection
    :param uname: username of the user
    :return: None
    """
    coll_list = show_collections(uname)

    if len(coll_list) == 0:
        print('You don\'t have your tools in any collection!')
        return
    valid_choice = False
    while not valid_choice:
        collection = input('What Collection do you want to look in? : ').strip().lower()

        if collection in coll_list:
            valid_choice = True
        else:
            print('That collection does not exist. Please enter a valid collection...')

    bc_list = get_tools_in_coll(uname, collection)

    table = [(bc_list[i], get_tool_details(bc_list[i])[0]) for i in range(len(bc_list))]

    print(tabulate(table, headers=['BARCODE', 'NAME']))

    input('Press Enter to return...')


def get_tool_owner(barcode):
    """
    Get the username of the owner of a tool
    :param barcode: the tool's barcode.
    :return: The username of the owner of the tool.
    """
    global conn
    cursor = conn.cursor()

    #get owner & collection
    sql='''
    SELECT "username" from "owns"
    WHERE "barcode"=%s
    AND "sold_date" IS NULL
    AND "rem_coll_date" IS NULL
    '''
    cursor.execute(sql, (barcode,))
    data = cursor.fetchall()
    return data[0][0]


def get_tool_name(barcode):
    """
    Get the tool name of a tool.
    :param barcode: barcode of the tool.
    :return: tool name of that tool.
    """
    global conn
    cursor = conn.cursor()

    #get owner & collection
    sql='''
    SELECT "name" from "tool"
    WHERE "barcode"=%s
    '''
    cursor.execute(sql, (barcode,))
    data = cursor.fetchall()
    return data[0][0]


def view_borrowed(uname):
    """
    find and return the tools that a user is borrowing or has borrowed.
    :param uname: username of the user.
    :return: table data of tools in tabulate format.
    """
    global conn
    cursor = conn.cursor()

    sql='''
    SELECT "barcode", "start_date", "due_date", "returned" FROM "borrows"
    WHERE "username" = %s
    '''
    cursor.execute(sql, (uname,))
    data = cursor.fetchall()
    table = [(tool[0], get_tool_name(tool[0]), tool[1], tool[2], tool[3]) for tool in data]

    return table

def print_borrowed(table):
    """
    print the tools that a user is borrowing or has borrowed.
    :param table: table data of tools in tabulate format.
    :return: None
    """
    print(tabulate(table, headers=['BARCODE', 'NAME', 'START', 'DUE', 'RETURNED']))

def get_tool_details(barcode):
    """
    Get all the revelant information of a specific tool:
    its name, whether it's lendable, the username of the owner, and which
    collections / categories it belongs to.
    :param barcode: barcode of the tool.
    :return: List of the information.
    """
    # returns (name, lendable, username, collection, categories)
    global conn
    cursor = conn.cursor()

    #get name and lendable
    sql='''
    SELECT "name", "lendable" from "tool"
    WHERE "barcode"=%s
    '''
    cursor.execute(sql, (barcode,))
    data = cursor.fetchall()
    name = data[0][0]
    lendable = data[0][1]

    #get owner & collection
    sql='''
    SELECT "username", "collection" from "owns"
    WHERE "barcode"=%s
    AND "sold_date" IS NULL
    AND "rem_coll_date" IS NULL
    '''
    cursor.execute(sql, (barcode,))
    data = cursor.fetchall()
    username = data[0][0]
    collection = data[0][1]

    #get categories
    sql='''
    SELECT "cat_name" from "is_in"
    WHERE "barcode"=%s
    '''
    cursor.execute(sql, (barcode,))
    data = cursor.fetchall()
    categories = data

    return (name, lendable, username, collection, categories)


def get_tools_in_coll(uname, coll_name):
    """
    Get the tools that are owned by a user that are in a specific collection.
    :param uname: username of the user.
    :param coll_name: name of the collection.
    :return: List of the barcodes of the tools.
    """
    # must be a valid coll_name
    global conn
    cursor = conn.cursor()

    #if uname == None:
    sql = '''
    SELECT "barcode" FROM "owns"
    WHERE "collection" = %s AND "rem_coll_date" IS NULL
    '''
    cursor.execute(sql, (coll_name,))
    # else:
    #     sql = '''
    #     SELECT "barcode" FROM "owns"
    #     WHERE "collection" = %s
    #     AND "rem_coll_date" IS NULL
    #     AND "username" = %s
    #     '''
    #     cursor.execute(sql, (coll_name, uname))

    coll_tools = cursor.fetchall()

    bc_list = [tool[0] for tool in coll_tools]

    return bc_list


def recommend_tool(uname):
    """
    find and print the tools that a user is likely to borrow.
    :param uname: username of the user.
    :return: None
    """

    table = view_borrowed(uname)

    tools_borrowed = [tool[0] for tool in table]
    cats_borrowed = [cat for bc in tools_borrowed for cats in get_tool_details(bc)[4] for cat in cats]
    popular_cat = max(set(cats_borrowed), key = cats_borrowed.count)

    global conn
    cursor = conn.cursor()

    sql='''
    SELECT "barcode" from "is_in"
    WHERE "cat_name"=%s
    '''
    cursor.execute(sql, (popular_cat,))
    all_barcodes = cursor.fetchall()
    barcodes = [barcode[0] for barcode in all_barcodes]

    borrowed = True

    while borrowed:
        recommendation = random.choice(barcodes)
        if recommendation not in tools_borrowed:
            borrowed = False

    print('Since you always borrow tools in the', popular_cat, 'category we recommend:\n')
    print(recommendation, '|', get_tool_name(recommendation))

    owner = get_tool_owner(recommendation)
    if owner == uname:
        print('\nYou own this tool! so you dont even neet to borrow it!!!')
    else:
        print('\nThis tool can be borrowed from', owner)





###############################################################################
#                         EDIT TOOL SUB MENU
###############################################################################


def edit_tool(uname):
    """
    Enter the tool editing menu for a specific tool.
    :param uname: username of the user who's trying to enter.
    :return: None
    """
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
            print('You don\'t own that tool, or it doesn\'t exist')


def show_tool_edit():
    """
    Display the tool editing menu.
    :return: None
    """
    print(' -- -- -- Tool EDITOR -- -- -- ')
    print(' 0. Back')
    print(' 1. Change Name')
    print(' 2. Lend Tool')
    print(' 3. Add/Remove from Collection')
    print(' 4. Add to Category')
    print(' 5. Sell')
    print(' 6. Mark tool as returned')
    print(' -- -- -- -- -- -- -- -- -- -- ')


def tool_edit(uname, barcode, tool_name, lendable):
    """
    Gets input from the tool editing menu and executes appropriate command.
    :param uname: username of the owner of the tool.
    :param barcode: barcode of the tool.
    :param tool_name: name of the tool.
    :param lendable: lendability of the tool.
    :return: None
    """
    while True:

        os.system('cls')
        print('Editing:', tool_name)
        show_tool_edit()
        try:
            n = int(input('Enter option : '))
        except ValueError:
            n = -1
        if n == 0:
            os.system('cls')
            break
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
            break
        elif n == 6:  # set as returned
            os.system('cls')
            set_returned(uname, barcode, tool_name)
            break
        else:
            os.system('cls')


def change_name(uname, barcode, tool_name):
    """
    Change the name of a specific tool.
    :param uname: username of the owner of the tool.
    :param barcode: barcode of the tool.
    :param tool_name: current name of the tool.
    :return: None
    """
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


def get_lent_tools(uname):
    """
    Get the tools lent out from a user.
    :param uname: username of the user.
    :return: list containing the username, barcode, start date, end date,
    and whether it has been returned of all the tools lent out from the user.
    """
    global conn
    cursor = conn.cursor()

    sql='''
    SELECT "username", "barcode", "start_date", "due_date", "returned" FROM "borrows"
    '''
    cursor.execute(sql, (uname,))
    lent_tools = cursor.fetchall()

    all_bcs = [tool[1] for tool in lent_tools]
    lent_list = []

    for i in range(len(all_bcs)):
        if get_tool_owner(all_bcs[i]) == uname:
            lent_list.append(lent_tools[i])

    return lent_list


def lend(uname, barcode, tool_name, lendable):
    """
    Lends a tool to another user.
    :param uname: username of who is lending the tool
    :param barcode: barcode of the tool
    :param tool_name: name of the tool
    :param lendable: lendability of the tool. User can choose to force a tool to be lent.
    :return: None
    """
    global conn
    cursor = conn.cursor()

    lent_tools = get_lent_tools(uname)
    lent_bcs = [tool[1] for tool in lent_tools]
    returned = [tool[4] for tool in lent_tools]

    if barcode in lent_bcs:
        if not returned[lent_bcs.index(barcode)]:
            print('This tool is already lent out, mark it as returned or try a different tool')
            input('Press Enter to exit...')
            return

    if not lendable:
        print(tool_name, 'is not marked as lendable, would you like to change this and lend anyways?')
        force_lend = input('\n(y/n): ')
        if force_lend[0] == 'y':
            sql = '''
            UPDATE "tool"
            SET "lendable" = 'true'
            WHERE "barcode" = %s
            '''
            cursor.execute(sql, (barcode,))
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

    #time to actually lend

    while True:
        try:
            lend_time = int(input('How long are you lending it (in days) : '))
            if lend_time > 0:
                break
        except ValueError:
            print('Enter a number more than 0...')

    start_date = datetime.now()
    due_date = start_date + timedelta(days=lend_time)

    sql = '''
    INSERT INTO "borrows" ("username", "barcode", "start_date", "due_date")
    VALUES (%s, %s, %s, %s)
    '''
    cursor.execute(sql, (borrow_uname, barcode, start_date, due_date))

    conn.commit()
    print('...Successfully Lent')
    sleep(.7)
    cursor.close()


def add_to_collection(uname, barcode, tool_name):
    """
    Add a tool to a collection and create the collection if it doesn't exist yet.
    :param uname: username of user who owns the tool.
    :param barcode: barcode of the tool.
    :param tool_name: name of the tool.
    :return: None
    """
    # if you specify a collection the tool is in already it will remove it from that collection
    global conn
    cursor = conn.cursor()

    coll_list = show_collections(None)
    os.system('cls')

    show_collections(uname)

    collection = input('\nEnter collection name to add or remove the tool from...\nIf that collection does not exist it will be made : ').strip().lower()

    new_coll = True
    remove_from_coll = False
    if collection in coll_list:
        new_coll = False
        # see if we are adding or removing from the collection
        bc_list = get_tools_in_coll(uname, collection)
        if barcode in bc_list:
            remove_from_coll = True

    if new_coll:
        # add in new collection
        sql = '''
        INSERT INTO "collection" ("coll_name")
        VALUES (%s)
        '''
        cursor.execute(sql, (collection,))

    if remove_from_coll:
        sql='''
        UPDATE "owns"
        SET "rem_coll_date" = %s
        WHERE "username" = %s AND "barcode" = %s;
        '''
        cursor.execute(sql, (datetime.now(), uname, barcode))
    else:
        # add in collection relation
        sql = '''
        UPDATE "owns"
        SET "collection" = %s, "rem_coll_date" = NULL
        WHERE "username" = %s AND "barcode" = %s;
        '''
        cursor.execute(sql, (collection, uname, barcode))

    conn.commit()
    print('...Successfully Added')
    sleep(.7)
    cursor.close()


def add_to_category(uname, barcode, tool_name):
    """
    Adds a tool to a category, creating the category if it doesn't exist yet.
    :param uname: username of the owner of the tool.
    :param barcode: barcode of the tool
    :param tool_name: name of the tool
    :return: None
    """
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

    category = input('\nEnter cat_name\nIf that category does not exist it will be made : ').strip().lower()

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
    """
    Sells a tool to another user, transferring ownership as well.
    :param uname: username of user who currently owns the tool.
    :param barcode: barcode of the tool
    :param tool_name: name of the tool
    :return: None
    """
    global conn
    cursor = conn.cursor()

    lent_tools = get_lent_tools(uname)
    lent_bcs = [tool[1] for tool in lent_tools]
    returned = [tool[4] for tool in lent_tools]

    if barcode in lent_bcs:
        if not returned[lent_bcs.index(barcode)]:
            print('This tool is currently lent out, mark it as returned to sell it')
            input('Press Enter to exit...')
            return

    uname_list, f_name_list, l_name_list = show_all_users(uname)

    correct_uname = False

    while not correct_uname:
        sell_uname = input('Enter the username of the user to sell to : ').strip()

        if sell_uname in uname_list:
            correct_uname = True
        else:
            print('That is not a valid username, try again...\n')

    # Update tool as sold
    sql='''
    UPDATE "owns"
    SET "sold_date" = %s
    WHERE "username" = %s AND "barcode" = %s;
    '''
    cursor.execute(sql, (datetime.now(), uname, barcode))
    # make the new owner
    buy_date = datetime.now()
    sql = '''
    INSERT INTO "owns" ("username", "barcode", "buy_date")
    VALUES (%s, %s, %s)
    '''
    cursor.execute(sql, (sell_uname, barcode, buy_date))

    conn.commit()
    print('...Successfully Sold')
    sleep(.7)
    cursor.close()


def set_returned(uname, barcode, tool_name):
    """
    Mark a tool as returned.
    :param uname: username of user who owns the tool.
    :param barcode: barcode of the tool
    :param tool_name: name of the tool
    :return: None
    """
    global conn
    cursor = conn.cursor()

    lent_tools = get_lent_tools(uname)
    lent_bcs = [tool[1] for tool in lent_tools]
    returned = [tool[4] for tool in lent_tools]

    if barcode not in lent_bcs:
        print('This tool is not lent out')
        input('Press Enter to exit...')
        return
    for i in range(0, len(returned)):
        if lent_bcs[i] == barcode and not returned[i]:
            # mark it as returned
            sql = '''
            UPDATE "borrows"
            SET "returned" = 'true'
            WHERE "barcode" = %s AND "returned" = 'false'
            '''
            cursor.execute(sql, (barcode,))
            conn.commit()
            print('...Successfully marked as returned')
            sleep(.7)
            cursor.close()
            return
    # then must be returned
    print('This tool is already returned to you')
    input('Press Enter to exit...')
    return


def is_in(li, bar_code):
    """
    helper method for show_top_lent, check if barcode is in list
    :param li: list
    :param bar_code: barcode
    :return: index of barcode if it is in list, or -1 otherwise
    """
    for i in range(0, len(li)):
        if li[i][0] == bar_code:
            return i
    return -1


def add_barcode(li, bar_code):
    """
    Add barcode to list, helper function for show_top_lent
    :param li: list
    :param bar_code: barcode
    :return: None
    """
    n = is_in(li, bar_code)
    if n == -1:
        li.append([bar_code, 1])
    else:
        li[n][1] += 1


def show_top_lent():
    """
    Display the top 20 most lent items.
    :return: None
    """
    global conn
    sql = '''
        SELECT "barcode" from "borrows"
        '''

    cursor = conn.cursor()
    cursor.execute(sql)
    bar_codes = cursor.fetchall()
    new_bar_codes = []
    for entry in bar_codes:
        new_bar_codes.append(entry[0])
    bar_codes = new_bar_codes;
    bar_freq_list = []
    for code in bar_codes:
        add_barcode(bar_freq_list, code)
    bar_freq_list.sort(key=lambda x: x[1], reverse=True)
    tool_info_list = []
    for i in range(0,19):
        t = get_tool_details(bar_freq_list[i][0])
        n = (t[0], bar_freq_list[i][1], t[2], t[3], t[4])
        tool_info_list.append(n)
    print(tabulate(tool_info_list, headers=['NAME', 'FREQUENCY', 'OWNER', 'COLLECTION', 'CATEGORIES']))
    print()


def show_most_borrower():
    """
    Display the top 20 users who borrow the most.
    :return: None
    """
    global conn
    sql = '''
        SELECT "username" from "borrows"
        '''

    cursor = conn.cursor()
    cursor.execute(sql)
    unames = cursor.fetchall()
    new_unames = []
    for entry in unames:
        new_unames.append(entry[0])
    unames = new_unames
    name_freq_list = []

    for name in unames:
        add_barcode(name_freq_list, name)
    name_freq_list.sort(key=lambda x: x[1], reverse=True)

    name_list = []

    for i in range(0, 19):
        t = get_user_info(name_freq_list[i][0])
        n = (name_freq_list[i][0], name_freq_list[i][1], t[1], t[2])
        name_list.append(n)
    print(tabulate(name_list, headers=['USERNAME', 'FREQUENCY', 'FIRST NAME', 'LAST NAME']))
    print()


def get_user_info(uname):
    """
    Get the information of user in database
    :param uname: uname of a specific user. If None, then displays all users.
    :return: the attributes of a specific user or all the users.
    """
    global conn
    cursor = conn.cursor()

    if uname is None:
        return
    else:
        # Get a list of all users but the uname given
        sql = '''
        SELECT "username", "first_name", "last_name" FROM "user"
        WHERE "username" = %s
        '''
    cursor.execute(sql, (uname,))
    all_users = cursor.fetchall()

    # print('--ID--', '-FIRST-', '-LAST-', sep='\t')
    return [all_users[0][0], all_users[0][1], all_users[0][2]]


def analytics():
    """
        Display the tool menu and executes appropriate command.
        :return: None
        """
    while True:
        os.system('cls')
        print(' -- -- -- ALL TOOL MENU -- -- -- ')
        print(' 0. Exit')
        print(' 1. Most lent tools')
        print(' 2. Most common borrowers')
        print(' -- -- -- -- -- -- -- -- -- -- ')

        try:
            n = int(input('Enter option : '))
            os.system('cls')
        except ValueError:
            n = -1
        if n == 0:
            return
        elif n == 1:
            show_top_lent()
            input('Press Enter to return...')
        elif n == 2:
            show_most_borrower()
            input('Press Enter to return...')
        else:
            pass


if __name__ == '__main__':
    main()
