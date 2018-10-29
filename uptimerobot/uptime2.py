import requests, json, csv, time
from datetime import datetime
  
# defining the api-endpoint  
API_ENDPOINT = "https://api.uptimerobot.com/v2/getMonitors"
  
# your API key here 
API_KEY = "u339994-75e37f9e35d26bd0d4718e1e"
  
csv_file = open("uptime-output.csv", "w")
  


def send_request(offset):
	file_content = "Monitor Name,URL,Status,7-day Uptime,30-day Uptime\n"

	data = {'api_key':API_KEY, 
		'format':'json',
		'offset' : offset,
		'custom_uptime_ratios': '7-30',
		'logs' : '1'} 

	r = requests.post(url = API_ENDPOINT, data = data)
	up_response = r.text
	parsed = json.loads(up_response)

	monitory = (parsed["monitors"])
	print(monitory)

	for monitor in monitory:
		print(monitor["friendly_name"])
		print(monitor["url"])
		print(monitor["status"])
		logs = (monitor["logs"])
		for log in logs:
			log_type = log["type"]
			duration = time.strftime('%M:%S', time.localtime(log["duration"]))
			dtime = (datetime.utcfromtimestamp(log["datetime"]).strftime('%Y-%m-%d %H:%M:%S'))

			file_content += monitor["friendly_name"] + "," + str(log_type) + "," + str(dtime) + "," + str(duration) + "\n"

	return file_content



write_it = send_request(0)
write_it += send_request(50)
write_it += send_request(100)

csv_file.write(write_it)

"""

# data to be sent to api 
data1 = {'api_key':API_KEY, 
		'format':'json',
		'custom_uptime_ratios': '7-30',
		'logs' : '1',
		'logs_start_date' : '1540024579',
		'logs_end_date' : '1540629379'} 

data2 = {'api_key':API_KEY, 
		'format':'json',
		'offset' : '50',
		'custom_uptime_ratios': '7-30',
		'logs' : '1',
		'logs_start_date' : '1540024579',
		'logs_end_date' : '1540629379'} 
  
# sending post request and saving response as response object 
r1 = requests.post(url = API_ENDPOINT, data = data1) 
r2 = requests.post(url = API_ENDPOINT, data = data2)

# extracting response text  
up_response1 = r1.text
parsed1 = json.loads(up_response1)
print(parsed1)

up_response2 = r2.text
parsed2 = json.loads(up_response2)
print("SECOND REQUEST:")
print(parsed2)

monitors = (parsed1["monitors"])

#Initiazing variables
sevenDaysTotal = 0.0; thirtyDaysTotal = 0.0

for monitor in monitors:
	print("Name: " + monitor["friendly_name"])
	file_content += monitor["friendly_name"] + ","
	print(monitor["url"])
	file_content += monitor["url"] + ","
	print(monitor["status"])
	file_content += str(monitor["status"]) + ","
	sevenDays, thirtyDays = (monitor)["custom_uptime_ratio"].split("-", 1)
	print("7-days: " + sevenDays)
	file_content += sevenDays + ","
	print("30-days: " + thirtyDays)
	file_content += thirtyDays + ",\n"
	sevenDaysTotal += float(sevenDays)
	thirtyDaysTotal += float(thirtyDays)
	print("\n")

print("7-Day Uptime: " + str(sevenDaysTotal/len(monitors)))
print("30-Day Uptime: " + str(thirtyDaysTotal/len(monitors)))

csv_file.write(file_content)
csv_file.close()

"""