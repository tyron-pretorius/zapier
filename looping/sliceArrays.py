#input={'names_raw':names_raw,'orders_raw':orders_raw,'phones_raw':phones_raw,'emails_raw':emails_raw,'start_index':0,'limit':500,'length':1251}

start_index = int(float(input['start_index']))
limit = int(input['limit'])
length = int(float(input['length']))

if (start_index+limit) >= length:
    end_index = length
    finished = True
else:
    end_index = start_index+limit
    finished = False
    
names = input['names_raw'].split('*')[start_index:end_index]
orders = input['orders_raw'].split('*')[start_index:end_index]
phones = input['phones_raw'].split('*')[start_index:end_index]
emails = input['emails_raw'].split('*')[start_index:end_index]
    
return{'end_index':end_index, 'names':names, 'orders':orders, 'phones':phones, 'emails':emails, 'finished':finished}
