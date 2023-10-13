#input variables to Zapier Code Transfer Step 12: Upload To Marketo
input={
  'token': 'Token', #from Step 4: Get Marketo Access Token
  'parent id': 'fid', #from Step 5: Get Parent ID or Create Parent Folder
  }

import requests
import urllib
import json
import re
import ast

mapping = ast.literal_eval(input['dict'])

payload = {
'folder': '{"id":367,"type":"Folder"}' #Email Files folder
}

headers = {
  'Authorization': 'Bearer ' + input['token']
}

url = "https://028-jjw-728.mktorest.com/rest/asset/v1/files.json"

for key, value in mapping.items():
    if isinstance(value, list):
        path  = urllib.parse.urlparse(value[0]).path
        path = re.search("(/Telnyx.*$)",path).group(0).lower()
        path = urllib.parse.unquote(path)
        name = path.split("/")[-1]
        
        remove = ["email", "banner", "image", "thumbnail"]
        for i in range(0, len(remove)):
            name = name.replace(remove[i],'')
            
        name = re.sub(r'[\s-]','_',name)
        
        for i in range(1,len(name)-2):
            if name[i] == '_' and re.match('\w_\w',name[i-1:i+2]) is None:
                name = name[:i] + name[i+1:]
        
        f = urllib.request.urlopen(value[1])
        mime_type = f.info().get_content_type()
        
        if 'banner' in key.lower():
            f_name = 'Asset_Email_Banner_'+name
        else:
            f_name = 'Asset_Email_Thumbnail_'+name

        files = {'file': (f_name, f, mime_type)}

        response = requests.request("POST", url, headers=headers, data = payload, files = files)
        print(response.text)
        mapping[key] = re.search('"url":"(.*)","folder',response.text).group(1)

return {'dict': str(mapping)}
