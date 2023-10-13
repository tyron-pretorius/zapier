from datetime import datetime
import json
import re
import requests
import os

# -------------- Priority Function Start ------------------------------

# return the index and value (in string format) containing the earliest date
def minDate(list, *args):
    time_list =[]
    for i in list:
        if i == 'None':
            time_list.append(datetime.strptime("9999-12-31T11:59:59Z", '%Y-%m-%dT%H:%M:%SZ'))
        else:
            time_list.append(datetime.strptime(i, '%Y-%m-%dT%H:%M:%SZ'))

    return [time_list.index(min(time_list)), min(time_list).strftime('%Y-%m-%dT%H:%M:%SZ')]


# return the index and value (in string format) containing the latest date
def maxDate(list, *args):
    for i in list:
        time_list = []
        if i == 'None':
            time_list.append(datetime.strptime("1111-01-01T00:00:01Z", '%Y-%m-%dT%H:%M:%SZ'))
        else:
            time_list.append(datetime.strptime(i, '%Y-%m-%dT%H:%M:%SZ'))
    return [time_list.index(max(time_list)), max(time_list).strftime('%Y-%m-%dT%H:%M:%SZ')]

# return the first index and value where the value is non-null and does not contain "null-like" values
def notNull(list, *args):
    new_list = [x.lower() for x in list]

    crap = ["empty", "unknown", "n/a", "[", "]", 'none', 'null']

    for i in new_list:
        good = "true"
        for j in crap:
            if j in i:
                good = False
        if good:
            return [new_list.index(i), list[new_list.index(i)]]

    return [0, list[0]]


# define the prioritized values for certain lead fields in order of decreasing priority from left to right
priority_dict = {
    'leadSource': ["Advertising", "Paid Search", "Referral", "Organic", "Marketing Generated", "Event", "Tradeshow", "Content",
                   "Webinar",  "Sales Generated", "Direct"],
    'leadStatus': ['Disqualified', 'Customer', 'Closed Won', 'SQL', 'SDR Engaged', 'SAL', 'MQL', 'ReNurture', 'SSL',
                   'Prospects', 'Prospects Cold', 'Known', 'Not a Lead'],
    'sfdcType': ['Contact']
}


# use the priority_dict function to find the highest priority value and corresponding index among the input
# lead values for a certain field. Else if none of the input lead values has a prioritized value return the first
# non-null value and index
def priority(list, line):
    for j in priority_dict[line]:
        for i in list:
            if j in i:
                return [list.index(i), i]

    return (notNull(list))


# return the first TRUE value and its index. True is prioritized because this function is used for the subscription opt in
# account blocked fields where it is important to favor TRUE over FALSE
def boolTest(list, *args):
    for i in list:
        if i is True:
            return [list.index(i), i]


#return the index and value of the maximum lead score
def leadScore(list, *args):

    new_list = list.copy()

    while 'None' in new_list:
        del new_list[new_list.index('None')]

    if len(new_list) > 0:
        return [list.index(max(new_list)), max(new_list) ]
    else:
        return [0, None ]


# define the prioritization function that will be called for each field
rules = {
    'createdAt': minDate,
    'subscriptionLastUpdated' : maxDate,
    'sfdcLeadId': notNull,
    'firstName': notNull,
    'utm_source__c' : notNull,
    'lastName': notNull,
    'leadSource': priority,
    'leadStatus': priority,
    'sfdcType': priority,
    'MC_Account_Blocked__c': boolTest,
    'Subscription_Opt_In__c': boolTest,
    'Subscription_Developer__c' : boolTest,
    'Behavior_Score_7_day__c': leadScore
}


# create a new list with None converted to string format and then pass this list to the rules dictionary so
# the correct prioritzation function is used on the lead
def ruler(line, line_list):
    formatted_list = []
    for x in line_list:
        if x is None:
            formatted_list.append('None')
        else:
            formatted_list.append(x)

    response = rules[line](formatted_list, line)
    if response[1] is 'None':
        response[1]=None

    return response


# -------------- Priority Function End ------------------------------

emails = ['office@voipasheville.com','johnh@respage.com','mberghoff@chabad.org','jonathonhills69420@gmail.com','mrmario098513@gmail.com','dshapalov@gmail.com','atmmachines@cloudmaveninc.com','conanolagvvw7wu83pib@gmail.com','tiniosmani2009@gmail.com','lobnajwan1002@gmail.com','johnmanfung_af_downey@yahoo.com','testabi009@gmail.com','maloka.505050@gmail.com','cecilperkins34@gmail.com','torresy1610@gmail.com','t.khimiak@gmail.com','stevenrbelmont@gmail.com','salib@moontechnolabs.com','wiegehtesdir87@gmail.com','ruiguo20888@gmail.com']
dateTimeObj = datetime.now()
file_name = dateTimeObj.strftime("%m-%d-%Y_%H:%M:%S")
file_name = "/home/tyron/Downloads/" + file_name + " " + os.path.basename(__file__)
file_name = file_name.replace("py", "txt")
f = open(file_name, "a")

for email in emails:
    # -------------- Get Duplicate Leads Start ------------------------------
    input={
        'token': '22e3c789-2e9b-4557-99e4-3b42655784e6:ab', #from Step 2: Get Marketo Access Token
        'lookup_value': email,
        'lookup_field_api_name': 'email',
        'base_url': 'https://028-JJW-728.mktorest.com',
        'field_names': 'id, sfdcLeadId, email, createdAt, firstName, lastName,leadSource, Lead_Source_Detail__c, unsubscribed, leadStatus, utm_source__c,utm_medium__c,utm_campaign__c,subscriptionLastUpdated,Subscription_Opt_In__c ,Status_Details__c,MC_Account_Blocked__c,Subscription_Product_Programmable_Voic__c,Subscription_Product_SMS__c,Subscription_Product_Voice__c,Subscription_Product_Wireless__c,Subscription_Product_News__c,Subscription_Featured_Content__c, Subscription_Marketing_Newsletter__c,Subscription_Event_Updates__c,Subscription_Bootcamp__c,Subscription_Developer__c,sfdcType,Behavior_Score_7_day__c,Behavior_Score_7_day_History__c,MQL_Source__c, MQL_Source_Detail__c, reMQL_Source__c, reMQL_Source_Detail__c, reMQLSourceDetailHistory__c, reMQLSourceHistory__c'
    }

    url = input['base_url'] + '/rest/v1/leads.json?filterType='+input['lookup_field_api_name']+'&filterValues='+input['lookup_value']+'&fields='+input['field_names']
    print(input['field_names'])
    print(url)
    headers = {
        'Authorization': 'Bearer '+input['token']
    }

    response = requests.request("GET", url, headers=headers)
    print(response.text)


    # -------------- Get Duplicate Leads End ------------------------------

    result = re.search('"result":\[(.*)\]',response.text).group(1)
    people = re.findall('{"id":.*?}(?=,{"id":)',result)
    end  = re.sub('{"id":.*?},(?={"id":)','',result)
    people.append(end)

    field_dict = {'id': [], 'sfdcLeadId': [], 'sfdcType':[], 'email': [], 'createdAt': [], 'firstName': [], 'lastName': [], 'leadSource': [], 'Lead_Source_Detail__c': [], 'utm_source__c': [],'utm_medium__c':[],'utm_campaign__c':[], 'leadStatus': [], 'Status_Details__c':[],'MC_Account_Blocked__c':[] , 'MQL_Source__c':[], 'MQL_Source_Detail__c':[], 'reMQL_Source__c':[], 'reMQL_Source_Detail__c':[], 'reMQLSourceDetailHistory__c':[], 'reMQLSourceHistory__c':[],'Behavior_Score_7_day__c':[],'Behavior_Score_7_day_History__c':[],'subscriptionLastUpdated':[],'unsubscribed': [],'Subscription_Opt_In__c':[] ,'Subscription_Product_Programmable_Voic__c':[],'Subscription_Product_SMS__c':[],'Subscription_Product_Voice__c':[],'Subscription_Product_Wireless__c':[],'Subscription_Product_News__c':[],'Subscription_Featured_Content__c':[], 'Subscription_Marketing_Newsletter__c':[],'Subscription_Event_Updates__c':[],'Subscription_Bootcamp__c':[],'Subscription_Developer__c':[]}

    final_dict = field_dict.fromkeys(field_dict, [])

    for p in people:
        for key in json.loads(p):
            field_dict[key] = field_dict[key] + [json.loads(p)[key]]

    for line in field_dict:
        #sfdcType exclusion is need in the if statement below because in the cases that the SFDC types match we need to go through the elif line =='sfdc_type' logic below instead of going through here
        if all(elem == field_dict[line][0] for elem in field_dict[line]) and line != 'sfdcType' and line != 'leadStatus' and line != 'Behavior_Score_7_day__c' and line!='subscriptionLastUpdated' and line!='leadSource':
            final_dict[line] = field_dict[line][0]
        else:
            if line in ['email', 'id', 'sfdcLeadId',  'Lead_Source_Detail__c',  'utm_source__c', 'utm_medium__c' ,'utm_campaign__c',
                        'Status_Details__c', 'Behavior_Score_7_day_History__c', 'unsubscribed', 'Status_Details__c',
                        'Subscription_Product_Programmable_Voic__c','Subscription_Product_SMS__c',
                        'Subscription_Product_Voice__c','Subscription_Product_Wireless__c',
                        'Subscription_Product_News__c','Subscription_Featured_Content__c',
                        'Subscription_Marketing_Newsletter__c','Subscription_Event_Updates__c','Subscription_Bootcamp__c','MQL_Source__c', 'MQL_Source_Detail__c', 'reMQL_Source__c', 'reMQL_Source_Detail__c', 'reMQLSourceDetailHistory__c', 'reMQLSourceHistory__c']:
                pass
            elif line == 'sfdcType':
                [index, value] = ruler(line, field_dict[line])
                final_dict[line] = value
                if value == 'Contact':
                    final_dict['sfdcLeadId'] = field_dict['sfdcLeadId'][index]
                    final_dict['id'] = field_dict['id'][index]
                else:
                    [index, value] = ruler('sfdcLeadId', field_dict['sfdcLeadId'])
                    if value is not None:
                        final_dict['sfdcLeadId'] = value
                        final_dict['id'] = field_dict['id'][index]
                    else:
                        [index, value] = ruler("createdAt", field_dict["createdAt"])
                        final_dict["createdAt"] = value
                        final_dict['id'] = field_dict['id'][index]
            elif line == 'leadSource':
                [index, value] = ruler(line, field_dict[line])
                final_dict[line] = value
                final_dict["Lead_Source_Detail__c"] = field_dict["Lead_Source_Detail__c"][index]
                if field_dict["utm_source__c"][index]:  # not empty
                    final_dict["utm_source__c"] = field_dict["utm_source__c"][index]
                    final_dict["utm_medium__c"] = field_dict["utm_medium__c"][index]
                    final_dict["utm_campaign__c"] = field_dict["utm_campaign__c"][index]
                else:  # if empty then get the 3xutm parameters from another lead
                    [index, value] = ruler("utm_source__c", field_dict["utm_source__c"])

                    final_dict["utm_campaign__c"] = field_dict["utm_campaign__c"][index]
                    final_dict["utm_medium__c"] = field_dict["utm_medium__c"][index]
                    final_dict["utm_campaign__c"] = field_dict["utm_campaign__c"][index]
            elif line == 'Behavior_Score_7_day__c':
                [index, value] = ruler(line, field_dict[line])
                final_dict[line] = value
                final_dict["Behavior_Score_7_day_History__c"] = field_dict["Behavior_Score_7_day_History__c"][index]
            elif line == 'subscriptionLastUpdated':
                [index, value] = ruler(line, field_dict[line])
                final_dict[line] = value
                final_dict["unsubscribed"] = field_dict["unsubscribed"][index]
                final_dict["Subscription_Product_Programmable_Voic__c"] = field_dict["Subscription_Product_Programmable_Voic__c"][index]
                final_dict["Subscription_Product_SMS__c"] = field_dict["Subscription_Product_SMS__c"][index]
                final_dict["Subscription_Product_Voice__c"] = field_dict["Subscription_Product_Voice__c"][index]
                final_dict["Subscription_Product_Wireless__c"] = field_dict["Subscription_Product_Wireless__c"][index]
                final_dict["Subscription_Product_News__c"] = field_dict["Subscription_Product_News__c"][index]
                final_dict["Subscription_Featured_Content__c"] = field_dict["Subscription_Featured_Content__c"][index]
                final_dict["Subscription_Marketing_Newsletter__c"] = field_dict["Subscription_Marketing_Newsletter__c"][index]
                final_dict["Subscription_Event_Updates__c"] = field_dict["Subscription_Event_Updates__c"][index]
                final_dict["Subscription_Bootcamp__c"] = field_dict["Subscription_Bootcamp__c"][index]
            elif line == 'leadStatus':
                [index, value] = ruler(line, field_dict[line])
                final_dict[line] = value
                final_dict["Status_Details__c"] = field_dict["Status_Details__c"][index]
                final_dict["MQL_Source__c"] = field_dict["MQL_Source__c"][index]
                final_dict["MQL_Source_Detail__c"] = field_dict["MQL_Source_Detail__c"][index]
                final_dict["reMQL_Source__c"] = field_dict["reMQL_Source__c"][index]
                final_dict["reMQL_Source_Detail__c"] = field_dict["reMQL_Source_Detail__c"][index]
                final_dict["reMQLSourceHistory__c"] = field_dict["reMQLSourceHistory__c"][index]
                final_dict["reMQLSourceDetailHistory__c"] = field_dict["reMQLSourceDetailHistory__c"][index]
            else:
                final_dict[line] = ruler(line, field_dict[line])[1]

    #dateTimeObj = datetime.now()
    log = dateTimeObj.strftime("%m-%d-%Y_%H:%M:%S") + "\n\nWinning and losing lead information:\n" + str(field_dict) + "\n\nWinning ID with field and value combinations to be updated after merging:\n"+str(final_dict) + "\n\n"
    print(dateTimeObj.strftime("%m-%d-%Y_%H:%M:%S") + "\n\nWinning and losing lead information:\n" + str(field_dict) + "\n\nWinning ID with field and value combinations to be updated after merging:\n"+str(final_dict) + "\n\n")


    #dateTimeObj = datetime.now()
    f.write(dateTimeObj.strftime("%m-%d-%Y_%H:%M:%S") + "\t" + input['lookup_value'] + "\n\n")
    f.write("Winning and losing lead information:\n")
    f.write(str(field_dict) + "\n\n")
    f.write("Winning ID with field and value combinations to be updated after merging:\n")
    f.write(str(final_dict) + "\n\n")
    #return{'field_dict':str(field_dict),'final_dict':str(final_dict), 'log':log}


    #------------- Merge Function Start ------------------
    #this function merges multiple leads together using the merge REST API endpoint
    #https://developers.marketo.com/rest-api/lead-database/leads/#merge
    def mergeLead(base_url, token, winner_id, loser_ids, CRMmerge):

        payload = {}
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + token
        }

        #When mergeinCRM is TRUE then you can only merge two leads at a time (when this is false you can merge multiple leads in a single call) hence why a for loop is needed to successively merge each of the losing ids with the winner
        loser_ids = [str(x) for x in loser_ids]
        response = []
        for i in loser_ids:
            url = base_url + '/rest/v1/leads/' + str(winner_id) + '/merge.json?mergeInCRM=' + str(CRMmerge) + '&leadIds=' + i
            response.append(requests.request("POST", url, headers=headers, data=payload).text)

        return (response)

    #------------- Merge Function End ------------------

    #field_dict = ast.literal_eval(field_dict)
    #final_dict = ast.literal_eval(final_dict)

    loser_ids = field_dict['id'].copy()
    loser_ids.remove(final_dict['id'])

    response = mergeLead(input['base_url'], input['token'], final_dict['id'], loser_ids, True)

    log = "Merge Response:\n" + str(response)+"\n\n"
    print(response)
    f.write("Merge Response:\n")
    f.write(str(response) + "\n\n")


    #---------------- Update Function Start ------------

    #use the Marketo REST API leads endpoint to update a lead field's with the values contained within the input lead_dict
    #https://developers.marketo.com/rest-api/lead-database/leads/#create_and_update
    def createUpdateLead(base_url, token, lead_dict):

        url = base_url + '/rest/v1/leads.json'

        payload = {
            "action":"updateOnly",
            "lookupField":"id",
            "input": lead_dict
        }
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + token
        }

        response = requests.request("POST", url, headers=headers, data=json.dumps(payload))

        return (response.text)

    #---------------- Update Function End --------------
    #field_dict = ast.literal_eval(field_dict)
    #final_dict = ast.literal_eval(final_dict)

    #loser_ids = field_dict['id'].copy()
    #loser_ids.remove(final_dict['id'])

    update_leads = ['']
    update_leads[0] = final_dict

    response = createUpdateLead(input['base_url'], input['token'], update_leads)
    log = "Update Response:\n" + response + "\n\n"
    f.write("Update Response:\n")
    f.write(response + "\n\n")
    f.write("---------------------------------------------------------------------------------------\n\n")
    print("Update Response:\n")
    print(response + "\n\n")


    n = 0

    #In the case that Marketo's merging rules selected a different winner than our logic, the the previous update call will contain "skipped" and we then need to cycle through the "loser" ids to find and update the actual winner
    while '"status":"skipped"' in str(response) and n < len(loser_ids):
        update_leads[0]['id'] = loser_ids[n]
        log = log + str(update_leads[0]) + "\n\n"
        response = createUpdateLead(input['base_url'], input['token'], update_leads)
        log = log + "Update Response:\n" + response + "\n\n"
        f.write("Update Response:\n")
        f.write(response + "\n\n")
        f.write("---------------------------------------------------------------------------------------\n\n")
        n=n+1

f.close()
