

import psycopg2

inputid = 362336
inputatt = 'unpaid'

def db_connection(inputid_db, inputatt_db):
	try:
		conn=psycopg2.connect( host="coredb2.prod.yodle.com", user="", password="", dbname="natpal")
	except:
		print("I am unable to connect to the database.")

	cur = conn.cursor()
	try:
		#cur.execute("SELECT id, name, status FROM control.client WHERE id = '{inputid}'".format(**vars()))
		cur.execute("SELECT conf.client_id, num.number, ctc.primaryattribution, ctc.secondaryattribution FROM control.calltrackingnumber num JOIN control.calltrackingnumberconfiguration conf ON conf.id = num.calltrackingnumberconfiguration_id LEFT JOIN control.ctcattributionconfig ctc on ctc.id = conf.attributionconfig_id WHERE ctc.secondaryattribution is null and ctc.primaryattribution = 'unpaid' and conf.client_id = 362336".format(**vars()))
		rows = cur.fetchall()
		print(rows[0][1] + " " + rows[0][2])
		print(rows)
		newvar = rows[0][1]
		print("Nowka " + newvar)
		cur.close()

	except:
		print("I can't drop our test database!")

	conn.close()


db_connection(inputid, inputatt)


