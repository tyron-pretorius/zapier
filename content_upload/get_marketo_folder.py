#input variables to Zapier Step 7: Get Marketo Folder ID
input={
  'c_type': 'Content Type' #from Step 1: Get Submission from Google Form
  'token': 'Token' #from Step 3: Get Marketo Access Token
  }
  
import requests
import datetime
import re
import urllib.parse

c_type = input['c_type']

now = datetime.datetime.now()
year = str(now.year) 

content_type = {"Case Study": ["Case Studies", "1947"] , "eBook":["eBooks","1948"], "Fact Sheet":["Fact Sheets","2125"], "Infographic":["Infographics","1949"], "Guide":["Guides","2892"], "Whitepaper":["Whitepapers","1950"]}


name = year + ' ' + content_type[c_type][0]

#https://developers.marketo.com/rest-api/assets/folders/#by_name
url = "https://###-xxx-###.mktorest.com/rest/asset/v1/folder/byName.json?name="+name

payload = {}
headers = {
  'Authorization': 'Bearer ' + input['token']
}

response = requests.request("GET", url, headers=headers, data = payload)
print(response.text)

if 'No assets found for the given search criteria' in response.text:
    headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': 'Bearer' + input['token']
    }
    
    folder= '{"id":'+content_type[c_type][1]+',"type":"Folder"}'
    
    payload = 'name=' +  urllib.parse.quote(name) + '&parent=' + urllib.parse.quote(folder)
    
    url = 'https://###-xxx-###.mktorest.com/rest/asset/v1/folders.json'
    
    response = requests.request("POST", url, headers=headers, data = payload)
    print(response.text)
    fid = re.search('"folderId":{"id":(\d*),', response.text ).group(1)
    info = "New:"+fid
else:
    fid = re.search('"folderId":{"id":(\d*),', response.text ).group(1)
    info = "Existing:"+fid

return {'folder_info': info}
