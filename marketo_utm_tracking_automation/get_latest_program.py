#input variables to Zapier Step 7: Get Latest Marketo Program For Sub-Channel
input={
  'token': 'Token', #from Step 4: Get Marketo Access Token
  'sub_channel': 'Sub-Channel', #from Step 3: Update Next Row in UTM Builder Sheet
  }

import requests
import datetime
import re


today = datetime.datetime.today().date()

year_ago = (datetime.datetime.today().date()-datetime.timedelta(60))

today = str(today)
year_ago = str(year_ago)

url = "https://028-jjw-728.mktorest.com/rest/asset/v1/programs.json?earliestUpdatedAt="+year_ago+"&latestUpdatedAt="+today+"&maxReturn=200"

payload = {}
headers = {
  'Authorization': 'Bearer' + input['token']
}

response = requests.request("GET", url, headers=headers, data = payload)

search_string= '"id":\d*,"name":"\d*\s-\s[\w\s]+-\s' + input['sub_channel']
print(search_string)

programs = re.findall(search_string,response.text )
programs.sort(reverse = True)
print(programs)

try:
    pid = re.search('"id":(\d*),',programs[0]).group(1)
except:
    print('Program not found')
    pid = '2712' #202101 - Paid Search - Google - Brand

return {'pid': pid}
