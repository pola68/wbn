import psycopg2


try:
	conn=psycopg2.connect( host="coredb2.prod.yodle.com", user="", password="", dbname="natpal")
except:
	print("I am unable to connect to the database.")

cur = conn.cursor()
try:
	cur.execute("SELECT conf.client_id, num.number, ctc.primaryattribution, ctc.secondaryattribution FROM control.calltrackingnumber num JOIN control.calltrackingnumberconfiguration conf ON conf.id = num.calltrackingnumberconfiguration_id LEFT JOIN control.ctcattributionconfig ctc on ctc.id = conf.attributionconfig_id WHERE ctc.secondaryattribution is null and ctc.primaryattribution = 'paid' and conf.client_id = {clientid}".format(**vars()))
	rows = cur.fetchall()
	db_paidNumber = []; db_paidNumber = rows[0][1]
	print("DB Paid number: " + db_paidNumber)
	file.write("DB Paid," + str(db_paidNumber) + ",")
	cur.close()
except:
	print("DB Paid number: Not Found")
	file.write("DB Paid,No DB Paid Number,")

	


	#file.write("DB Unpaid," + str(db_unpaidNumber) + "," + str(db_unpaidShowDest) + ",")
	cur.close()
except:
	print("DB Unpaid number: Not Found")
	#file.write("DB Unpaid,No DB Unpaid Number,")