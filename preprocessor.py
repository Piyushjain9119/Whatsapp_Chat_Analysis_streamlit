import re 
import pandas as pd

def preprocess(data):
    pattern = '\[\d{2}/\d{2}/\d{2},\s\d{1,2}:\d{2}:\d{2}]\s~\s'
    messages = re.split(pattern,data)
    del messages[0]
    dates = re.findall(pattern,data)
    def mapper(values):
        data = []
        for value in values:
            
            value = value.split('~')
            
            data.append(value[0])
        return data

    dates = mapper(dates)
    df = pd.DataFrame({'user_message':messages , 'message_date':dates})
    # convert message data type
    df['message_date'] = pd.to_datetime(df['message_date'],format ='[%d/%m/%y, %H:%M:%S] ')

    df.rename(columns = {'message_date' :'Date'},inplace = True)
    # separate users and messages
    users = []
    messages = []
    for message in df['user_message']:
        entry =re.split('([\w\W]+?):\s',message)
        if entry[1:]:# user name
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])
            
    df['User']  = users
    df['Message'] = messages
    df.drop(columns = ['user_message'] , inplace = True)
    df['Year'] = df['Date'].dt.year
    df['Month_num'] = df['Date'].dt.month
    df['Month'] = df['Date'].dt.month_name()
    df['Day'] =df['Date'].dt.day
    df['Only_date'] = df['Date'].dt.day
    df['Hour'] =df['Date'].dt.hour
    df['Minute'] = df['Date'].dt.minute
    df['day_name'] = df['Date'].dt.day_name()

    period = []
    for hour in df[['day_name','Hour']]['Hour']:
        if hour ==23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" +str(hour+1))
        else:
            period.append(str(hour) + "-" +str(hour +1))
    
    df['period'] = period

    return df

                
