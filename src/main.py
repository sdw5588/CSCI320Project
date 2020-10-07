import psycopg2  # pip install psycorg2

NAME = 'PythonAPP'


def main():
    conn = psycopg2.connect("dbname=p320_26 user=p320_26 password=eewier5eix2ag3ohChoo host=reddwarf.cs.rit.edu")
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
