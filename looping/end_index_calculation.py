#input={ 'length': 1250, 'last_index': 501, 'limit':500}


last_index = int(input['last_index'])
limit = int(input['limit'])
length = int(float(input['length']))

if (last_index+limit) > length:
    end_index = length
else:
    end_index = last_index+limit
    
return{'end_index':end_index}
