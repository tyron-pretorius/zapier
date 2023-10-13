#input variables to Zapier Step 12: Update Marketo Dynamic Email Content Sections
input={
  'token': 'Token' #from Step 2: Get Marketo Access Token
  'dids': 'Dynamic Ids' #from Step 11: Create Marketo Dynamic Email Content Sections
  'eid': 'Eid' #from Step 7: Create Email
  
  'template': '<p style="Margin:0;padding:0;-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;font-size:14px;line-height:20px;color:#5F6368;font-family:roboto, 'helvetica neue', helvetica, arial, sans-serif;"><strong>${articleTitle}</strong></p>
<br>
<p style="Margin:0;padding:0;-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;font-size:14px;line-height:20px;color:#5F6368;font-family:roboto, 'helvetica neue', helvetica, arial, sans-serif;">${articleText}</p>
<br>
<p style="Margin:0;padding:0;-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;font-size:14px;line-height:20px;color:#5F6368;font-family:roboto, 'helvetica neue', helvetica, arial, sans-serif;"><a href="${articleLink}" style="color: #00c08b;font-weight:bold;" target="_blank">${articleCTA}</a></p>'
  
  'content': 'Dynamic Values' #from Step 1: New Spreadsheet Row
  'values': 'Variable Values' #from Step 1: New Spreadsheet Row
  }


import requests
import datetime
import urllib.parse

month = datetime.datetime.today().month

jibberish = ["—", "’"]
char = ["--", "'"]

querystring = input['values'].split('*')[-1]
querystring = querystring.replace("&","&amp;")
print(querystring)

for i in range(0, len(jibberish)):
    input['content']=input['content'].replace(jibberish[i], char[i])

content = input['content'].split('*')

replace = ['${articleLink}', '${articleCTA}', '${articleTitle}', '${articleText}']

headers = {
  'Content-Type': 'application/x-www-form-urlencoded',
  'Authorization': 'Bearer ' + input['token']
}

dids = input['dids'].split(",")
segments = ['SMS','Elastic SIP Trunking','Call Control']
order = ['Elastic SIP Trunking','Call Control', 'SMS']

response=''

for d in range(0,len(dids)):

    url = 'https://028-jjw-728.mktorest.com/rest/asset/v1/email/'+input['eid']+'/dynamicContent/'+dids[d]+'.json'
    
    for s in range(0,len(segments)):
        value = input['template']
        
        for r in range(0,len(replace)):
            if r == 0:
                value = value.replace(replace[r], content[(d*12)+(s*4)+r]+querystring)
            else:
                value = value.replace(replace[r], content[(d*12)+(s*4)+r])
        
        print(value)
        encoded = urllib.parse.quote(value)
        
        payload = 'segment='+segments[s]+'&type=html&value='+encoded
        response = response + requests.request("POST", url, headers=headers, data = payload).text
        
        if segments[s] == order[month%3]:
            payload = 'segment=Default&type=html&value='+encoded
            response = response + requests.request("POST", url, headers=headers, data = payload).text

return {'response': response, "qs":querystring}
