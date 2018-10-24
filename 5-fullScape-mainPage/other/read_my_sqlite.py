import sqlite3

#Opening SQLite Connection
sqlite_connection = sqlite3.connect('database.db'); c = sqlite_connection.cursor()

file = open("michaltest.txt","w")

#Manipulating SQLite DB
c.execute("SELECT * from main_audit")
rows = c.fetchall()
for row in rows:
	print("Date: %s\nCorp Name: %s\nClientID: %s\nClientName: %s\nPPC Produt: %s\nPPC Number Matched: %s\n" % (row[0],row[1],row[2],row[3],row[4],row[5]))
	file.write("Date: %s\nCorp Name: %s\nClientID: %s\nClientName: %s\nPPC Product: %s\nPPC Number Matched: %s\n" % (row[0],row[1],row[2],row[3],row[4],row[5]))
	



# Closing SQLite DB Entries and Connection
sqlite_connection.commit(); sqlite_connection.close()

file.close
