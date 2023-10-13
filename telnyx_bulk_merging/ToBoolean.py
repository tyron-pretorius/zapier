#this will change the data type of each column to boolean
def ToBoolean (raw_list):

    bool_fields = ["MC_Account_Blocked__c", "unsubscribed", "Subscription_Opt_In__c", "Subscription_Product_Programmable_Voic__c", "Subscription_Product_SMS__c"\
,"Subscription_Product_Voice__c", "Subscription_Product_Wireless__c","Subscription_Product_News__c", "Subscription_Featured_Content__c", "Subscription_Marketing_Newsletter__c"\
,"Subscription_Event_Updates__c", "Subscription_Bootcamp__c","Subscription_Developer__c"]

    for f in bool_fields:
        raw_list[f]=raw_list[f].astype(bool)
