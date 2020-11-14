#input variables to Zapier Step 8: Get Latest Marketo Program ID
input={
  'c_type': 'Content Type' #from Step 1: Get Submission from Google Form
  'token': 'Token' #from Step 3: Get Marketo Access Token
  'folder_info': 'Folder Info' #from Step 7: Get Marketo Folder ID
  }
  
  
import requests
import datetime
import re

now = datetime.datetime.now()
year = str(now.year) 

content_type = {"Case Study": ["Case Studies", "1947"] , "eBook":["eBooks","1948"], "Fact Sheet":["Fact Sheets","2125"], "Infographic":["Infographics","1949"], "Guide":["Guides","2892"], "Whitepaper":["Whitepapers","1950"]}

if 'Existing' in input['folder_info']:
    fid = input['folder_info'].split(":")[1]
else:
    c_type = input['c_type']
    name = str(now.year-1) + ' ' + content_type[c_type][0]
    #https://developers.marketo.com/rest-api/assets/folders/#by_name
    url = "https://###-xxx-###.mktorest.com/rest/asset/v1/folder/byName.json?name="+name

    payload = {}
    headers = {
        'Authorization': 'Bearer ' + input['token']
    }
    response = requests.request("GET", url, headers=headers, data = payload)
    fid = re.search('"folderId":{"id":(\d*),', response.text ).group(1)
    print(response.text)
#https://developers.marketo.com/rest-api/assets/folders/#browse
url = 'https://###-xxx-###.mktorest.com/rest/asset/v1/folders.json?root={\"id\":'+fid+',\"type\":\"Folder\"}'

payload = {}
headers = {
  'Authorization': 'Bearer ' + input['token']
}

response = requests.request("GET", url, headers=headers, data = payload)

raw=response.text
print(raw)
pattern = '"createdAt":"\d*-\d*-\w*:\d*:\w*\+\d*","updatedAt":"\d*-\d*-\w*:\d*:\w*\+\d*","url":"https://app-ab20.marketo.com/#PG\w+","folderId":{"id":\d*,"type":"Program"}'
     
dates = re.findall(pattern, raw)
print(dates)
dates.sort(reverse=True)
print(dates)

pattern = '"folderId":{"id":(\d*),"type":"Program"}'
program_ids = re.findall(pattern, "".join(dates))
print(program_ids)
latest_id=program_ids[0]

return {'program_id': latest_id}
