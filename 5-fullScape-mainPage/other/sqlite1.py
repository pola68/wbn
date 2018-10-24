import sqlite3

conn = sqlite3.connect('database.db'); c = conn.cursor()

#c.execute('''CREATE TABLE main_audit (corp_name text, client_id int, client_name text)''')


#c.execute("INSERT INTO main_audit VALUES ('Handyman Matters','332544','Handyman Matters - New York22')")
#c.execute("INSERT INTO main_audit VALUES ('Handyman Matters','121326','Handyman Matters - Rover')")
#c.execute("INSERT INTO main_audit VALUES ('SpeedPro','353431','SpeedPro - Philadelpia')")

test1 = "Firma"
test2 = '123'
test3 = "Firma NYC"
#c.execute("INSERT INTO main_audit VALUES ('Handyman Matters','332544',%s), (testm)")
c.execute("INSERT INTO main_audit VALUES ('Dupka2', ?, ?)", (test2, test3))





conn.commit()

"""
c.execute("SELECT * FROM main_audit WHERE client_name like '%New%'")
results = c.fetchall()

for result in results:
	print(result)
"""
conn.close()


