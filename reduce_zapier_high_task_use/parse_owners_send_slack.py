#the re module is need for regex parsing
import re
import json

#only continue if the message was sent by a bot i.e. no username
if input['username'] == 'empty':
    #lists for the first and tag names are created by splitting the input strings
    f_names = input['f_names'].split('**')[0].split('*')
    t_names = input['t_names'].split('**')[0].split('*')

    #a dictionary is created to map first names to their corresponding tag name
    mapping = dict(zip(f_names,t_names))

    #the Slack message from Step 1 is stored
    text = input['text']

    #regex patterns are used to search for owner and SDR names
    acc_owner = re.search('Account Owner:\s(\w*.\w*)\n',text)
    acc_sdr = re.search('Account SDR:\s(\w*)\s\w*\n\n',text)
    lead_owner = re.search('Lead Owner:\s(\w*.\w*)\n',text)
    lead_sdr = re.search('Lead SDR:\s(\w*)\s\w*\n',text)

    #a list is created containing the search results
    l_names = [acc_owner,acc_sdr, lead_owner, lead_sdr]

    #the eventual Slack message is initialized
    message = ""

    #each search result is then assessed and its
    for l in l_names:

        #if the search result is not empty and the name found is not in the message already
        if l != None and mapping[l.group(1)] not in message: 
            #append the name to message
            message = message + "@" + mapping[l.group(1)] + " "
    
    #only continue if the message is populated
    if message != '':
        
        #destination url of the slack channel
        url= 'https://hooks.slack.com/services/xxxxx/xxxx/xxxxx'
        
        #convert the message to json format
        payload = json.dumps({'text': message})
        
        #configure the webhook for json messages
        headers = {'Content-Type': 'application/json'}
        
        #send webhook and store the response
        response = requests.request("POST", url, headers=headers, data = payload)
          

return {'message': message, 'response': response.text}
