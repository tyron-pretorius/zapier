#input variables to Zapier Code Transfer Step 7: Create Dictionary
input={
  'token': 'Token', #from Step 4: Get Marketo Access Token
  'parent id': 'fid', #from Step 5: Get Parent ID or Create Parent Folder
}

import re

v_array = input['values'].split('*')
h_array = input['headers'].split('*')
dictionary = dict(zip(h_array, v_array))

filtered = {k: v for k, v in dictionary.items() if k is not None}

return{'dict_string':str(filtered),'dict_values':filtered}
