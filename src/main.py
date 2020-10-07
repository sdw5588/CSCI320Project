import psycopg2  # pip install psycorg2

NAME = 'PythonAPP'

def main():

    f = open("creds.txt", "r")
    usr = f.readline().rstrip()
    passwd = f.readline().rstrip()
    #print("dbname="+ usr + " user= " + usr + " password=" + passwd + " host=reddwarf.cs.rit.edu", sep = "")

    conn = psycopg2.connect("dbname="+ usr + " user= " + usr + " password=" + passwd + " host=reddwarf.cs.rit.edu")
    print("Connected with " + conn.dsn)

    cur = conn.cursor()

    cur.execute("""
    INSERT INTO "TestTable" ("id", "Information", "Owner", "Rented")
    VALUES (99, 'SQL Test', '{}', false)
    """.format(NAME))
    conn.commit()

    cur.close()
    conn.close()

if __name__ == '__main__':
    main()
