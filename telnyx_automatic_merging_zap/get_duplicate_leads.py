#input variables to Zapier Step 3: Get Duplicate Leads
input={
  'token': 'Token', #from Step 2: Get Marketo Access Token
  'lookup_value': 'Email Address', #from Step 1: Lead Added to Duplicates List
  'lookup_field_api_name': 'email',
  'base_url': 'https://###-xxx-###.mktorest.com',
  'field_names': 'id, sfdcLeadId, email, createdAt, firstName, lastName,leadSource, Lead_Source_Detail__c, unsubscribed, leadStatus, utm_source__c,utm_medium__c,utm_campaign__c,subscriptionLastUpdated,Subscription_Opt_In__c ,Status_Details__c,MC_Account_Blocked__c,Subscription_Product_Programmable_Voic__c,Subscription_Product_SMS__c,Subscription_Product_Voice__c,Subscription_Product_Wireless__c,Subscription_Product_News__c,Subscription_Featured_Content__c, Subscription_Marketing_Newsletter__c,Subscription_Event_Updates__c,Subscription_Bootcamp__c,Subscription_Developer__c,sfdcType,Behavior_Score_7_day__c,Behavior_Score_7_day_History__c,MQL_Source__c, MQL_Source_Detail__c, reMQL_Source__c, reMQL_Source_Detail__c, reMQLSourceDetailHistory__c, reMQLSourceHistory__c'
  }

import requests
import json
import re
import urllib.parse

#https://developers.marketo.com/rest-api/lead-database/leads/#query

url = input['base_url'] + '/rest/v1/leads.json?filterType='+input['lookup_field_api_name']+'&filterValues='+input['lookup_value']+'&fields='+input['field_names']
print(input['field_names'])
print(url)
headers = {
  'Authorization': 'Bearer '+input['token']
}

response = requests.request("GET", url, headers=headers)
print(response.text)

return{'response':response.text}
