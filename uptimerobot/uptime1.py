import requests, json, csv
  
# defining the api-endpoint  
API_ENDPOINT = "https://api.uptimerobot.com/v2/getMonitors"
  
# your API key here 
API_KEY = "u339994-75e37f9e35d26bd0d4718e1e"
  
# your source code here 
source_code = ''' 
print("Hello, world!") 
a = 1 
b = 2 
print(a + b) 
'''
  
# data to be sent to api 
data = {'api_key':API_KEY, 
        'format':'json',
        'custom_uptime_ratios': '7-30',
        'logs_start_date' : '1540024579',
        'logs_end_date' : '1540629379'} 
  
# sending post request and saving response as response object 
r = requests.post(url = API_ENDPOINT, data = data) 
  
# extracting response text  
up_response = r.text
parsed = json.loads(up_response)
print(parsed)

monitors = (parsed["monitors"])
sevenDaysTotal = 0.0; thirtyDaysTotal = 0.0
for monitor in monitors:
	print("Name: " + monitor["friendly_name"])
	print(monitor["url"])
	print(monitor["status"])
	sevenDays, thirtyDays = (monitor)["custom_uptime_ratio"].split("-", 1)
	print("7-days: " + sevenDays)
	print("30-days: " + thirtyDays)
	sevenDaysTotal += float(sevenDays)
	thirtyDaysTotal += float(thirtyDays)
	print("\n")

print("7-Day Uptime: " + str(sevenDaysTotal/len(monitors)))
print("30-Day Uptime: " + str(thirtyDaysTotal/len(monitors)))

