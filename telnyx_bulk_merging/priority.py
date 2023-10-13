from datetime import datetime

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

    if (max(time_list).strftime('%Y-%m-%dT%H:%M:%SZ') == "1111-01-01T00:00:01Z"):
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
    'leadStatus': ['Disqualified', 'Customer', 'Closed Won', 'SQO', 'SQL', 'SAL', 'MQL', 'ReNurture', 'SSL',
                   'Known', 'Prospect'],
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
    'Subscription_Developer__c': boolTest,
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
