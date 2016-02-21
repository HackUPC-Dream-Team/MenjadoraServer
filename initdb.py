import sqlite3

con = sqlite3.connect('database.db')
c = con.cursor()

c.execute('''DROP TABLE IF EXISTS feed''')
c.execute('''CREATE TABLE feed (amount INTEGER, time INTEGER)''')
c.execute('''INSERT INTO feed VALUES (200, 400)''')

c.close()
con.close()

con = sqlite3.connect('database.db')
c = con.cursor()

c.execute('''SELECT * FROM feed''')
print c.fetchall()

c.close()
con.close()