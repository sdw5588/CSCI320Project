import psycopg2  # pip install psycorg2
import os
from time import sleep
from datetime import datetime, timedelta
from tabulate import tabulate
import random

NAME = 'PythonAPP'
conn = object

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

def set_returned(uname, barcode):
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

    if barcode in lent_bcs:
        if returned[lent_bcs.index(barcode)]:
            print('This tool is already returned to you')
            input('Press Enter to exit...')
            return
        else:
            #mark it as returned
            sql = '''
            UPDATE "borrows"
            SET "returned" = 'true'
            WHERE "barcode" = %s AND "returned" = 'false'
            '''
            cursor.execute(sql, (barcode,))
            print('...Successfully marked as returned')
            sleep(.7)
            cursor.close()
    else:
        print('This tool is not lent out')
        input('Press Enter to exit...')
        return


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


def lend(uname, barcode, lendable, borrow_uname, lend_time):
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

    #time to actually lend

    start_date = datetime.now()
    due_date = start_date + timedelta(days=lend_time)

    sql = '''
    INSERT INTO "borrows" ("username", "barcode", "start_date", "due_date")
    VALUES (%s, %s, %s, %s)
    '''
    cursor.execute(sql, (borrow_uname, barcode, start_date, due_date))

    print('...Successfully Lent')
    sleep(.7)
    cursor.close()


# you need to make a file called creds.txt with the username on the first line and password on the next one
# f = open("creds.txt", "r")
usr = "p320_26"
passwd = "eewier5eix2ag3ohChoo"
# print("dbname="+ usr + " user= " + usr + " password=" + passwd + " host=reddwarf.cs.rit.edu", sep = "")

conn = psycopg2.connect("dbname=" + usr + " user=" + usr + " password=" + passwd + " host=reddwarf.cs.rit.edu")
print("Connected with " + conn.dsn)
os.system('cls')

uname_list, f_name_list, l_name_list = show_all_users(None)
barcodes, tool_names, lend_list = view_tools(None)

os.system('cls')

for i in range(6):
    user_to = random.choice(uname_list)
    barcode = random.choice(barcodes)
    owner = get_tool_owner(barcode)
    time = random.randrange(3, 106)

    name, lendable, ownx, collx, catx = get_tool_details(barcode)

    if user_to == owner:
        pass;

    print('lending', barcode, 'of', owner, 'to', user_to, 'for', time)
    lend(owner, barcode, lendable, user_to, time)
    chance = random.choice([1, 0, 0])
    if chance:
        print('RETURNING too')
        set_returned(owner, barcode)
    conn.commit()
