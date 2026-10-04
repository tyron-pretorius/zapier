#this will change the data type of each column to UTC timestamps
import pytz
import pandas as pd

utc = pytz.timezone('UTC')

def ToUTC (df):

    int_fields = ["createdAt", "subscriptionLastUpdated"]

    for f in int_fields:
        temp = df.copy()
        temp.index = pd.to_datetime(df[f])
        temp.index =  temp.index.tz_localize('America/Chicago')
        temp.index =  temp.index.tz_convert('UTC')
        temp.index =  temp.index.strftime('%Y-%m-%dT%H:%M:%SZ')
        df[f]=temp.index
        df[f] = df[f].astype(str)
        df[f] = df[f].apply(lambda x: None if x == "NaT" else x)
