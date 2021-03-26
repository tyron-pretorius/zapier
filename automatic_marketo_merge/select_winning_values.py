#input variables to Zapier Step 4: Select Winning Field Values
input={
  'people': 'people_array_string' #from Step 3: Get Duplicate Leads
  }

from datetime import datetime
import json
import re

# -------------- Priority Function Start ------------------------------

# return the index and value (in string format) containing the earliest created at date
def createdAt(list, *args):
    time_list = [datetime.strptime(i, '%Y-%m-%dT%H:%M:%SZ') for i in list]
    return [time_list.index(min(time_list)), min(time_list).strftime('%Y-%m-%dT%H:%M:%SZ')]


# return the first index and value where the value is non-null and does not contain "null-like" values
def notNull(list, *args):
    new_list = [x.lower() for x in list]

    crap = ["empty", "unknown", "n/a", "[", "]", 'none']

    for i in new_list:
        good = "true"
        for j in crap:
            if j in i:
                good = False
        if good:
            return [new_list.index(i), list[new_list.index(i)]]

    return [0, list[0]]


# define the prioritized values for certain lead fields in order of descreasing priority from left to right
priority_dict = {
    'leadSource': ["Advertising", "Paid Search", "Organic", "Marketing Generated", "Event", "Tradeshow", "Content",
                   "Webinar", "Referral", "Sales Generated", "Direct"],
    'leadStatus': ['Disqualified', 'Customer', 'Closed Won', 'SQL', 'SDR Engaged', 'SAL', 'MQL', 'ReNurture', 'SSL',
                   'Prospects', 'Prospects Cold', 'Known', 'Not a Lead']
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


# return the first TRUE value and its index. True is prioritized because this function is used for the unsubscribed
# account blocked fields where it is important to favor TRUE over FALSE
def boolTest(list, *args):
    for i in list:
        if i is True:
            return [list.index(i), i]


# define the prioritization function that will be called for each field
rules = {
    'createdAt': createdAt,
    'sfdcLeadId': notNull,
    'firstName': notNull,
    'lastName': notNull,
    'leadSource': priority,
    'leadStatus': priority,
    'unsubscribed': boolTest
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
    return rules[line](formatted_list, line)


# -------------- Priority Function End ------------------------------

people = re.findall('{.*?}', input['people'])

field_dict = {'id': [], 'sfdcLeadId': [], 'email': [], 'createdAt': [], 'firstName': [], 'lastName': [],'leadSource': [], 'Lead_Source_Detail__c': [], 'unsubscribed': [], 'leadStatus': []}

final_dict = field_dict.fromkeys(field_dict, [])

for p in people:
    for key in json.loads(p):
        field_dict[key] = field_dict[key] + [json.loads(p)[key]]

for line in field_dict:
    if all(elem == field_dict[line][0] for elem in field_dict[line]) and line != 'sfdcLeadId':
        final_dict[line] = field_dict[line][0]
    else:
        if line in ['email', 'id', 'Lead_Source_Detail__c']:
            pass
        elif line == 'sfdcLeadId':
            [index, value] = ruler(line, field_dict[line])
            if value is not None:
                final_dict[line] = value
                final_dict['id'] = field_dict['id'][index]
            else:
                [index, value] = ruler("createdAt", field_dict["createdAt"])
                final_dict["createdAt"] = value
                final_dict['id'] = field_dict['id'][index]
        elif line == 'leadSource':
            [index, value] = ruler(line, field_dict[line])
            final_dict[line] = value
            final_dict["Lead_Source_Detail__c"] = field_dict["Lead_Source_Detail__c"][index]
        else:
            final_dict[line] = ruler(line, field_dict[line])[1]

dateTimeObj = datetime.now()
log = dateTimeObj.strftime("%m-%d-%Y_%H:%M:%S") + "\n\nWinning and losing lead information:\n" + str(field_dict) + "\n\nWinning ID with field and value combinations to be updated after merging:\n"+str(final_dict) + "\n\n"

return{'field_dict':str(field_dict),'final_dict':str(final_dict), 'log':log}
