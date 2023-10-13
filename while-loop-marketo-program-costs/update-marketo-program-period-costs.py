#input variables to Zapier Step 3: Update Marketo Program Period Costs
input={
  'index': 'index', #from Step 1: Catch Webhook
  'timestamp': 'timestamp'#from Step 1: Catch Webhook
  'programs': 'programs', #from Step 2: Get Marketo Program Period Cost Data
  'costs': 'costs', #from Step 2: Get Marketo Program Period Cost Data
  'log': 'log', #from Step 2: Get Marketo Program Period Cost Data
  }

import json
import requests
import time
import re
from datetime import datetime

#Create an array of programs and cost by splitting the input strings
programs = input['programs'].split('*')
costs = costs_str.split('*')

#Marketo only accepts whole numbers for program costs so each element in the costs lists is converted from a string to a float, rounded, and then converted to an integer
costs = [int(round(float(i))) for i in costs]

#Use the input timestamp to get the date. The date is then changed to be the 1st day of the month and all program costs for the previous month will be marked with this date i.e. mm/01/yyyy
ts = input['timestamp']
date = ts.split(',')[0]
date = re.sub('/\d*/', '/1/', date)

# The Rest API enpoint for you Marketo instance can be found in Admin > Web Services
base_url = "https://###-XXX-###.mktorest.com"

#A variable to store the remaining seconds left on the life of the current Marketo access token
remaining = 0

#Each step in Zapier has a 10s timeout so this is the maximum amount of time we will need the Marketo access token to survive for. To be on the safe side, the "wait" variable is set to 20 secs to give more than enough time.
wait = 20 #secs

#This while loop gets an access token that has a remaining lifespan greater than 20 secs
while remaining < wait:
    #if the remaining lifespan of the access token is less than 20 secs than wait out the remainder of the lifespan before getting a new token
    time.sleep(remaining)
    
    #Make a Get request to get an access token and then use json.loads to create a dictionary out of the json response
    #https://developers.marketo.com/rest-api/authentication/#creating_an_access_token
    temp = json.loads(requests.get(
        base_url+'/identity/oauth/token?grant_type=client_credentials&client_id=xxxx&client_secret=xxx').text)

    #Get the token and the remaining lifespan of the token by accessing their respective keys in the "temp" dictionary
    token = temp['access_token']
    remaining = temp['expires_in']

#Set the headers that will be used for each post request in the while loop below
headers = {
    'Content-Type': "application/x-www-form-urlencoded",
    'cache-control': "no-cache",
    'Authorization': 'Bearer ' + token
}

#The starting point to begin iterating over the programs list i.e. 0, 20, 40 etc depending on how many iterations this zap has gone through
index = int(input['index'])
#Set the iterative variable i to the starting point
i = index
#The limit of 20 programs for this step was found by experimentation. If any more programs are updated in this step then the chances of exceeding the 10sec timeout limit imposed on all Zapier steps will be increased
limit = 20
#Store any exisiting information in the log cell so that more information can be appended in the while loop below
log = input['log']

#Iterate through the remaining programs starting at position i. (i-index) < limit ensures that this while loop only does 20 or less program updates at a time so as not to exceed the 10sec timeout
while i < len(programs) and (i - index) < limit:

    #Use a GET request to get the program information using the program name.   https://developers.marketo.com/rest-api/assets/programs/#by_name
    get_name_response = requests.request("GET", base_url + "/rest/asset/v1/program/byName.json?name=" + programs[i]+'&includeCosts=true',
                                         headers={'Authorization': 'Bearer ' + token}, data={}).text
    
    #Only proceed if the program is found correctly
    if "No assets found" not in get_name_response and "name cannot be blank." not in get_name_response:
        #parse out the result array
        result = re.search('result":\[(.*)\]}', get_name_response).group(1)
        #convert the result array to a dictionary
        dict = json.loads(result)
        #Store the program id and costs list
        pid = str(dict["id"])
        costs_list = dict["costs"]

        #Convert the date format to match that used by Marketo
        date_object = datetime.strptime(date, '%m/%d/%Y').date()
        
        #Iterate through the costs_list dictionary to see if there is already a program cost for the date for last month
        ind = next((i for i, item in enumerate(costs_list) if item["startDate"] == (str(date_object)+'T05:00:00Z+0000')), None)
        
        #If there is no cost for the last month's date then append the date and cost to costs_list
        if ind is None:
            costs_list.append({"startDate": str(date_object)+'T05:00:00Z+0000',"cost": costs[i]})
        #If there is an existing cost for last month's date then replace this old cost with the new cost    
        else:
            costs_list[ind]["cost"] = costs[i]
        
        #Convert the costs_list dictionary to JSON format for use in the payload string. Setting costsDestructiveUpdate to true will erase any previous costs in the program, which will now be replaced by the updated costs list: https://developers.marketo.com/rest-api/assets/programs/#update
        payload = 'costs=' + json.dumps(costs_list) + '&costsDestructiveUpdate=True'
        update_program_response = requests.request("POST", base_url + '/rest/asset/v1/program/' + pid + '.json',data=payload, headers=headers).text

        #If the update was successful, parse out the url and costs_list from the reponse and append them to the log along with the iteration number i and the program name
        if '"success":true' in update_program_response:
            result = re.search('result":\[(.*)\]}', update_program_response).group(1)
            dict = json.loads(result)
            url = dict["url"]
            costs_list = str(dict["costs"])

            log = log + '***#' + str(i) + '---' + programs[i] + '---'+ url + '---' + costs_list
        #Record a failed update in the log if the update was not successful, listing the program name for future debugging
        else:
            log = log + '***#' + str(i) + '---' + programs[i] + ': Update Failed'
    
    #If the program name is not found or blank then update the log to indicate that the program was not found
    else:
        log = log + '***#' + str(i) + '---' + programs[i] + ': Not Found'
    
    #Increment i to access the next program in the list for the next iteration of the while loop
    i=i+1
    
#Set finished to false by default. If all the programs have been updated then set finished to True.
finished = False     
if i == len(programs):
    finished=True
    
#Output the log so it can be updated in the Google sheet, i so it can be sent via webhook to trigger the next iteration of the zap if necessary, and the finished boolean value to be used in Step 5 of the Zap to determine whether another webhook must be sent to trigger another iteration of this zap.    
output = [{'log': log, 'index': i, 'finished':finished}]
