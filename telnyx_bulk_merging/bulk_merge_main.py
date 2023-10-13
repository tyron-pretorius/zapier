import pandas as pd
from datetime import datetime
import os
import time

from Priority import ruler
from AppendDict import appendDict
from Marketo_API_Get_Auth import getToken
from Marketo_API_Merge import mergeLead
from Marketo_API_Create_Update_Lead import createUpdateLead
from ToBoolean import ToBoolean
from ToInt import ToInt
from ToUTC import ToUTC

base_url = "https://028-jjw-728.mktorest.com"

raw_list = pd.read_csv('/home/tyron/Downloads/Possible_Duplicates (18).csv')
raw_list.rename(columns={'Id':'id', 'Marketo SFDC ID': 'sfdcLeadId', 'SFDC Type':'sfdcType', 'Email Address': 'email', 'Created At': 'createdAt', 'First Name': 'firstName', 'Last Name': 'lastName', 'Person Status': 'leadStatus', 'Status Details': 'Status_Details__c', 'MC Account - Blocked?': 'MC_Account_Blocked__c','Person Source':'leadSource','Lead Source Detail': 'Lead_Source_Detail__c', 'utm_source': 'utm_source__c', 'utm_medium':'utm_medium__c','utm_campaign':'utm_campaign__c' , 'MQL Source':'MQL_Source__c', 'MQL Source Detail':'MQL_Source_Detail__c', 'reMQL Source':'reMQL_Source__c', 'reMQL Source Detail':'reMQL_Source_Detail__c', 'reMQL Source History':'reMQLSourceHistory__c', 'reMQL Source Detail History':'reMQLSourceDetailHistory__c','Unsubscribed':'unsubscribed','Subscription - Last Updated':'subscriptionLastUpdated','Subscription - Opt-In':'Subscription_Opt_In__c','Subscription - Bootcamp': 'Subscription_Bootcamp__c','Subscription - Developer':'Subscription_Developer__c' ,'Subscription - Event Updates':'Subscription_Event_Updates__c','Subscription - Featured Content':'Subscription_Featured_Content__c','Subscription - Marketing Newsletter':'Subscription_Marketing_Newsletter__c','Subscription - Product News':'Subscription_Product_News__c','Subscription - Product Programmable Voic':'Subscription_Product_Programmable_Voic__c','Subscription - Product SMS':'Subscription_Product_SMS__c', 'Subscription - Product Voice':'Subscription_Product_Voice__c','Subscription - Product Wireless':'Subscription_Product_Wireless__c','Behavior Score - 7 day':'Behavior_Score_7_day__c','Behavior Score - 7 day History':'Behavior_Score_7_day_History__c'},inplace=True)

ToInt(raw_list)
ToUTC(raw_list)
raw_list = raw_list.where(raw_list.notnull(), None)

#this boolean conversion needs to be after NaN has been replaced by None otherwise all values will be set to True. With NaN replaced by None these None values will
#correctly be converted to False values
ToBoolean(raw_list)

#convert the dataframe to a dictionary
raw_list = raw_list.to_dict(orient='records')

#sorts the dictionary by email address
raw_list = sorted(raw_list, key=lambda d: d['email'])

field_dict = {'id': [], 'sfdcLeadId': [], 'sfdcType':[], 'email': [], 'createdAt': [], 'firstName': [], 'lastName': [], 'leadSource': [], 'Lead_Source_Detail__c': [], 'utm_source__c': [],'utm_medium__c':[],'utm_campaign__c':[], 'leadStatus': [], 'Status_Details__c':[],'MC_Account_Blocked__c':[] , 'MQL_Source__c':[], 'MQL_Source_Detail__c':[], 'reMQL_Source__c':[], 'reMQL_Source_Detail__c':[], 'reMQLSourceDetailHistory__c':[], 'reMQLSourceHistory__c':[],'Behavior_Score_7_day__c':[],'Behavior_Score_7_day_History__c':[],'subscriptionLastUpdated':[],'unsubscribed': [],'Subscription_Opt_In__c':[] ,'Subscription_Product_Programmable_Voic__c':[],'Subscription_Product_SMS__c':[],'Subscription_Product_Voice__c':[],'Subscription_Product_Wireless__c':[],'Subscription_Product_News__c':[],'Subscription_Featured_Content__c':[], 'Subscription_Marketing_Newsletter__c':[],'Subscription_Event_Updates__c':[],'Subscription_Bootcamp__c':[],'Subscription_Developer__c':[]}
final_dict = field_dict.fromkeys(field_dict, [])

count = 0
#update_leads = ['']
i= 0

dateTimeObj = datetime.now()
file_name = dateTimeObj.strftime("%m-%d-%Y_%H:%M:%S")
file_name = "/home/tyron/Downloads/" + file_name + " " + os.path.basename(__file__)
file_name = file_name.replace("py","txt")

remaining = 0
limit = len(raw_list)

while i < limit:

    time.sleep(remaining)  # if the remaining time is less than 60 secs then wait for the token to expire before getting a new one

    count = 0
    start = time.time()
    temp = getToken()
    token = temp[0]
    expires = temp[1]
    print(token, expires)
    remaining = expires - (time.time() - start)


    while i < limit and remaining> 60 : #Marketo token expires after 3600secs and give 60 sec window so token does not expire mid execution of the loop below

        field_dict = field_dict.fromkeys(field_dict, [])
        final_dict = final_dict.fromkeys(final_dict, [])

        appendDict(field_dict, raw_list[i])

        j=i+1
        while j < len(raw_list) and (raw_list[i]['email'] == raw_list[j]['email']):
            appendDict(field_dict, raw_list[j])
            j=j+1

        i = j


        # for n in range(0, len(field_dict['id'])):
        #     field_dict['id'][n] = int(field_dict['id'][n])

        # print(field_dict)

        for line in field_dict:
            # sfdcType exclusion is needed in the if statement below because in the cases that the SFDC types match we need to go through the elif line =='sfdc_type' logic below instead of going through here
            if all(elem == field_dict[line][0] for elem in field_dict[
                line]) and line != 'sfdcType' and line != 'leadStatus' and line != 'Behavior_Score_7_day__c' and line != 'subscriptionLastUpdated' and line != 'leadSource':
                final_dict[line] = field_dict[line][0]
            else:
                if line in ['email', 'id', 'sfdcLeadId', 'Lead_Source_Detail__c', 'utm_source__c', 'utm_medium__c',
                            'utm_campaign__c',
                            'Status_Details__c', 'Behavior_Score_7_day_History__c', 'unsubscribed', 'Status_Details__c',
                            'Subscription_Product_Programmable_Voic__c', 'Subscription_Product_SMS__c',
                            'Subscription_Product_Voice__c', 'Subscription_Product_Wireless__c',
                            'Subscription_Product_News__c', 'Subscription_Featured_Content__c',
                            'Subscription_Marketing_Newsletter__c', 'Subscription_Event_Updates__c',
                            'Subscription_Bootcamp__c', 'MQL_Source__c', 'MQL_Source_Detail__c', 'reMQL_Source__c',
                            'reMQL_Source_Detail__c', 'reMQLSourceDetailHistory__c', 'reMQLSourceHistory__c']:
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

                        final_dict["utm_source__c"] = field_dict["utm_source__c"][index]
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
                    final_dict["Subscription_Product_Wireless__c"] = field_dict["Subscription_Product_Wireless__c"][
                        index]
                    final_dict["Subscription_Product_News__c"] = field_dict["Subscription_Product_News__c"][index]
                    final_dict["Subscription_Featured_Content__c"] = field_dict["Subscription_Featured_Content__c"][
                        index]
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

        f = open(file_name, "a")
        dateTimeObj = datetime.now()
        f.write(dateTimeObj.strftime("%m-%d-%Y_%H:%M:%S") + "\t" + str(count) + "\t" + str(i) + "\n\n")
        f.write("Winning and losing lead information:\n")
        f.write(str(field_dict) + "\n\n")
        f.write("Winning ID with field and value combinations to be updated after merging:\n")
        # f.write(str(final_dict) + "\n\n")

        print(count)
        print(i)
        print(field_dict)
        print(final_dict)
        print('')

        loser_ids = field_dict['id'].copy()
        loser_ids.remove(final_dict['id'])

        #all_loser_ids.append(loser_ids)
        # update_leads[0] = final_dict
        # # if isinstance(update_leads[0]['leadScore'], numbers.Number):
        # #     update_leads[0]['leadScore'] = int(update_leads[0]['leadScore'])

        f.write(str(final_dict) + "\n\n")

        response = mergeLead(base_url, token, final_dict['id'], loser_ids, True)
        f.write("Merge Response:\n")
        f.write(str(response) + "\n\n")
        print(response)



        if '"success":false' in str(response):
            f.write("---------------------------------------------------------------------------------------\n\n")
            f.close()

        else:
            response = createUpdateLead(base_url, token, [final_dict])
            print(response)
            f.write("Update Response:\n")
            f.write(response + "\n\n")
            n = 0
            while '"status":"skipped"' in str(response) and n < len(loser_ids):
                final_dict['id'] = loser_ids[n]
                print(final_dict)
                f.write(str(final_dict) + "\n\n")
                response = createUpdateLead(base_url, token, [final_dict])
                print(response)
                f.write("Update Response:\n")
                f.write(response + "\n\n")
                n = n + 1

            f.write("---------------------------------------------------------------------------------------\n\n")
            f.close()

        count = count + 1

        time.sleep(0.2)

        remaining = 0 if (expires - (time.time() - start)) < 0 else (expires - (time.time() - start))
