import requests, json, csv, time, sys, smtplib
import datetime
from datetime import datetime
from urllib.parse import urlparse
sys.path.append('/tools')
import mySetup


# defining the api-endpoint  
API_ENDPOINT = "https://api.uptimerobot.com/v2/getMonitors"
  
# your API key here 
API_KEY = "u339994-75e37f9e35d26bd0d4718e1e"
  
csv_file = open("uptime-output.csv", "w")
csv_file.write("Monitor Name,URL,Ratios,Event,Date,Duration (min),Details,Status\n")

downMonitors = 0; pausedMonitors = 0; upMonitors = 0; downWebsites = []; pausedWebsites=[]

def send_request(offset, downMonitors, pausedMonitors, upMonitors):
	file_content = "" 
	data = {'api_key':API_KEY, 
		'format':'json',
		'offset' : offset,
		'custom_uptime_ratios': '1-7-30',
		'logs' : '1'} 

	r = requests.post(url = API_ENDPOINT, data = data)
	up_response = r.text
	parsed = json.loads(up_response)

	monitory = (parsed["monitors"])

	for monitor in monitory:
		if (monitor["status"] == 0 or monitor["status"] == 1):
			pausedMonitors += 1
			pausedWebsites.append(monitor["url"])
		elif (monitor["status"] == 8 or monitor["status"] == 9):
			downMonitors += 1
			downWebsites.append(monitor["url"])
		elif monitor["status"] == 2:
			upMonitors += 1

	for monitor in monitory:
		logs = (monitor["logs"])

		for log in logs:
			log_type = log["type"]
			if log_type == 1:
				log_type = "Down"
			elif log_type == 2:
				log_type = "Up"
			elif log_type == 99:
				log_type = "Paused"
			else:
				log_type = "Started"

			dtime = (datetime.utcfromtimestamp(log["datetime"]).strftime('%Y-%m-%d %H:%M:%S'))
			duration = round(log["duration"]/60); duration = round(duration)
			reason_detail = log["reason"]["detail"]

			file_content += monitor["friendly_name"] + "," + monitor["url"] + "," + monitor["custom_uptime_ratio"] + "," + str(log_type) + "," + dtime + "," + str(duration) + "," + reason_detail + "," + str(monitor["status"]) + "\n"

	csv_file.write(file_content)
	return (file_content, downMonitors, pausedMonitors, upMonitors, downWebsites, pausedWebsites)

file_conent, downMonitors, pausedMonitors, upMonitors, downWebsites, pausedWebsites = send_request(0, downMonitors, pausedMonitors, upMonitors)
file_conent, downMonitors, pausedMonitors, upMonitors, downWebsites, pausedWebsites = send_request(50, downMonitors, pausedMonitors, upMonitors)
file_conent, downMonitors, pausedMonitors, upMonitors, downWebsites, pausedWebsites = send_request(100, downMonitors, pausedMonitors, upMonitors)
csv_file.close()





#PULLING DATA THAT WAS RETRIEVED ABOVE

import datetime
today = datetime.datetime.now()
oneDayAgo = today - datetime.timedelta(hours=24)
sevenDaysAgo = today - datetime.timedelta(days=7)
thirdayDaysAgo = today - datetime.timedelta(days=30)


oneDayTotalUp = 0; oneDayTotalDown = 0; sevenDayTotalUp = 0; sevenDayTotalDown = 0; thirdayDayTotalUp = 0; thirdayDayTotalDown = 0;
headers = "Date & Time          |       Event        |Duration|     URL  \n"
oneDayEvents = headers; sevenDayEvents = headers

with open('uptime-output.csv', 'r') as csvfile:
	readCSV = csv.reader(csvfile, delimiter=',')
	
	for row in readCSV:
		if row[4] >= str(oneDayAgo):
			if(row[3] == "Up") or (row[3] == "Paused"):
				oneDayTotalUp += int(row[5])
			if row[3] == "Down":
				oneDayTotalDown += int(row[5])
				oneDayEvents += "%s  |  %s |  %s  |   %s\n" % (row[4], row[6], row[5], row[1])

		if row[4] >= str(sevenDaysAgo):
			if(row[3] == "Up") or (row[3] == "Paused"):
				sevenDayTotalUp += int(row[5])
			if row[3] == "Down":
				sevenDayTotalDown += int(row[5])
				sevenDayEvents += "%s  |  %s |  %s  |   %s\n" % (row[4], row[6], row[5], row[1])

		if row[4] >= str(thirdayDaysAgo):
			if(row[3] == "Up") or (row[3] == "Paused"):
				thirdayDayTotalUp += int(row[5])
			if row[3] == "Down":
				thirdayDayTotalDown += int(row[5])
	csvfile.close()




#1 Day Metrics
email_summary = "---------------------------------------------------------\n\n"
email_summary += "LAST 24 HOURS REVIEW:\n"
email_summary += "Last 24 Hours Up Minutes: %d" % oneDayTotalUp + "\n"
email_summary += "Last 24 Hours Down Minutes: %d" % oneDayTotalDown + "\n"

oneDayAllTime = oneDayTotalUp + oneDayTotalDown
oneDayUpRatio = (oneDayTotalUp / oneDayAllTime) * 100
email_summary += "Last 24 Hours Uptime Ratio: " + str(round(oneDayUpRatio,2)) + "%\n\n\n"

#7 Days Metrics
email_summary += "LAST 7 DAYS REVIEW:\n"
email_summary += "7-Day Up Minutes: %d" % sevenDayTotalUp + "\n"
email_summary += "7-Day Down Minutes: %d" % sevenDayTotalDown + "\n"

sevenDayAllTime = sevenDayTotalUp + sevenDayTotalDown
sevenDayUpRatio = (sevenDayTotalUp / sevenDayAllTime) * 100
email_summary += "7-Day Uptime Ratio: " + str(round(sevenDayUpRatio,2)) + "%\n\n\n"

#30 Days Metrics
email_summary += "LAST 30 DAYS REVIEW:\n"
email_summary += "30-Day Up Minutes: %d" % thirdayDayTotalUp + "\n"
email_summary += "30-Day Down Minutes: %d"% thirdayDayTotalDown + "\n"

thirdayDayAllTime = thirdayDayTotalUp + thirdayDayTotalDown
thirdaDayUpRatio = (thirdayDayTotalUp / thirdayDayAllTime) * 100
email_summary += "30-Day Uptime Ratio: " + str(round(thirdaDayUpRatio,2)) + "%\n\n\n"

#Monitors Status
email_summary += "---------------------------------------------------------\n"
email_summary += "CURRENT MONITORS STATUS\n\n"
email_summary += "Number Of Down Monitors: %d" % downMonitors + "\n"
for row in downWebsites:
	email_summary += row + "\n"
email_summary += "\nNumber Of Paused Monitors: %d" % pausedMonitors + "\n"
for row in pausedWebsites:
	email_summary += row + "\n"
email_summary += "\nNumber Of Up Monitors: %d" % upMonitors + "\n\n"

#List of Outages
email_summary += "---------------------------------------------------------\n"
email_summary += "OUTAGES THAT HAPPENED WITHIN LAST 24 HOURS:\n\n"
email_summary += oneDayEvents
email_summary += "\n\n\nOUTAGES THAT HAPPENED WITHIN LAST 7 DAYS:\n\n"
email_summary += sevenDayEvents


print(email_summary)

#Sending Email
subject = '%s mins down - Enterprise Daily Web Monitoring Report' % oneDayTotalDown 
body = 'Hello,\n\nThis is Web For Enterprise Daily Web Monitoring Report including most vital website uptime metrics.\n\n\n' + email_summary
recipients = 'mswiader@yodle.com'
gmail_user = mySetup.gmailUsername
gmail_pwd = mySetup.gmailPassword
smtpserver = smtplib.SMTP("smtp.gmail.com",587)
smtpserver.ehlo(); smtpserver.starttls(); smtpserver.login(gmail_user, gmail_pwd)
header = 'To:' + recipients + '\n' + 'From: ' + gmail_user + '\n' + 'Subject:' + subject + ' \n'
msg = header + '\n' + body + '\n\n'
smtpserver.sendmail(gmail_user, recipients.split(', '), msg)


