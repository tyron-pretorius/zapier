#input variables to Developer Newsletter Creation Step 15: Get Month and Year
input={
  'token': 'Token', #from Step 2: Get Token
  'parent id': 'fid', #from Step 3: Get Parent ID or Create Parent Folder
  }

import datetime

now = datetime.datetime.now()
year = str(now.year) 

return {'id': 1234, 'rawHTML': now.strftime("%B")+" "+year}
