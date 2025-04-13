import psycopg2

conn = psycopg2.connect(
    host = "localhost",
    port = "5432",
    database = "LegacyIQ",
    user = "postgres",
    password="password123")

if conn:
    print("connnection to database was successful")
else:
    print("error")

cur= conn.cursor()
#add orgID to acount table 
#cur.execute("CREATE TABLE account(accountID INTEGER, blogID INTEGER, accountType TEXT)" )
#cur.execute("INSERT INTO account(accountID, blogID, accountType) VALUES(%s, %s, %s)", ("1234", "2234", "blogger"))
#conn.commit()

cur.execute("SELECT * FROM account")
rows = cur.fetchall()
for r in rows:
    print(r)

cur.close()
conn.close() 

print("Connection to database is closed")