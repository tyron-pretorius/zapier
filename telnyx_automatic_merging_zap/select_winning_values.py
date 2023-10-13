#input variables to Zapier Step 4: Select Winning Field Values
input={
  'response': 'Response' #from Step 3: Get Duplicate Leads
  }

from datetime import datetime
import json
import re

# -------------- Priority Function Start ------------------------------

# return the index and value (in string format) containing the earliest date
def minDate(list, *args):
    time_list =[]
    for i in list:
        if i == 'None':
            time_list.append(datetime.strptime("9999-12-31T11:59:59Z", '%Y-%m-%dT%H:%M:%SZ'))
        else:
            time_list.append(datetime.strptime(i, '%Y-%m-%dT%H:%M:%SZ'))
    if (min(time_list).strftime('%Y-%m-%dT%H:%M:%SZ')=="9999-12-31T11:59:59Z"):
        return [0, 'None']
    else:
        return [time_list.index(min(time_list)), min(time_list).strftime('%Y-%m-%dT%H:%M:%SZ')]


# return the index and value (in string format) containing the latest date
def maxDate(list, *args):
    time_list = []
    for i in list:
        if i == 'None':
            time_list.append(datetime.strptime("1111-01-01T00:00:01Z", '%Y-%m-%dT%H:%M:%SZ'))
        else:
            time_list.append(datetime.strptime(i, '%Y-%m-%dT%H:%M:%SZ'))
            
    if (max(time_list).strftime('%Y-%m-%dT%H:%M:%SZ')=="1111-01-01T00:00:01Z"):
        return [0, 'None']
    else:
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
    'leadStatus': ['Disqualified', 'Customer', 'Closed Won', 'SQO', 'SQL','SAL','MQL', 'ReNurture', 'SSL','Known','Prospect'],
    'sfdcType': ['Contact']
}


# use the priority_dict function to find the highest priority value and corresponding index among the inputlead values for a certain field. Else if none of the input lead values has a prioritized value return the first non-null value and index
def priority(list, line):
    for j in priority_dict[line]:
        for i in list:
            if j in i:
                return [list.index(i), i]

    return (notNull(list))


# return the first TRUE value and its index. True is prioritized because this function is used for the subscription opt in and account blocked fields where it is important to favor TRUE over FALSE
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


# create a new list with None converted to string format and then pass this list to the rules dictionary so the correct prioritzation function is used on the lead
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

result = re.search('"result":\[(.*)\]',input['response']).group(1)
people = re.findall('{"id":.*?}(?=,{"id":)',result)
end  = re.sub('{"id":.*?},(?={"id":)','',result)
people.append(end)

field_dict = {'id': [], 'sfdcLeadId': [], 'sfdcType':[], 'email': [], 'createdAt': [], 'firstName': [], 'lastName': [], 'leadSource': [], 'Lead_Source_Detail__c': [], 'utm_source__c': [],'utm_medium__c':[],'utm_campaign__c':[], 'leadStatus': [], 'Status_Details__c':[],'MC_Account_Blocked__c':[] , 'MQL_Source__c':[], 'MQL_Source_Detail__c':[], 'reMQL_Source__c':[], 'reMQL_Source_Detail__c':[], 'reMQLSourceDetailHistory__c':[], 'reMQLSourceHistory__c':[],'Behavior_Score_7_day__c':[],'Behavior_Score_7_day_History__c':[],'subscriptionLastUpdated':[],'unsubscribed': [],'Subscription_Opt_In__c':[] ,'Subscription_Product_Programmable_Voic__c':[],'Subscription_Product_SMS__c':[],'Subscription_Product_Voice__c':[],'Subscription_Product_Wireless__c':[],'Subscription_Product_News__c':[],'Subscription_Featured_Content__c':[], 'Subscription_Marketing_Newsletter__c':[],'Subscription_Event_Updates__c':[],'Subscription_Bootcamp__c':[],'Subscription_Developer__c':[]}

final_dict = field_dict.fromkeys(field_dict, [])

for p in people:
    for key in json.loads(p):
        field_dict[key] = field_dict[key] + [json.loads(p)[key]]

print(field_dict)

for line in field_dict:
    #sfdcType exclusion is needed in the if statement below because in the cases that the SFDC types match we need to go through the elif line =='sfdc_type' logic below instead of going through here
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

dateTimeObj = datetime.now()
log = dateTimeObj.strftime("%m-%d-%Y_%H:%M:%S") + "\n\nWinning and losing lead information:\n" + str(field_dict) + "\n\nWinning ID with field and value combinations to be updated after merging:\n"+str(final_dict) + "\n\n"

return{'field_dict':str(field_dict),'final_dict':str(final_dict), 'log':log}
