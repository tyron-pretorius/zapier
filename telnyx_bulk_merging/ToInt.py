#this will change the data type of each column to int

import numpy as np

def ToInt (raw_list):

    int_fields = ["Behavior_Score_7_day__c"]

    for f in int_fields:
        raw_list[f] = raw_list[f].fillna(-1)
        raw_list[f] = raw_list[f].astype(int)
        raw_list[f] = raw_list[f].astype(str)
        raw_list[f] = raw_list[f].replace('-1', np.nan)
