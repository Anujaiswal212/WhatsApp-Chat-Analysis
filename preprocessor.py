import pandas as pd
import re

def preprocess(data):
    #f = open('WhatsApp Chat with FRIENDS❤️🧡💚 FOREVER.txt', 'r', encoding='utf-8')
    pattern = '\d+/\d+/\d+, \d+:\d+ [A-Z]{2}\s-'
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)
    df = pd.DataFrame({'user_messages': messages, 'Date_time': dates})


    # convert Date_time
    df['Date_time'] = pd.to_datetime(df['Date_time'], format='%m/%d/%y, %I:%M %p -')
    df.rename(columns={'Date_time': 'dates'}, inplace=True)

    # seperate user and massages

    messages = []
    users = []
    for message in df['user_messages']:

        entry = re.split('([\w\s\w]+?):\s', message)
        if entry[1:]:  # user name
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('Group Notification')
            messages.append(entry[0])
    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_messages'], inplace=True)

    df['year'] = df['dates'].dt.year
    df['month_num'] = df['dates'].dt.month
    df['month'] = df['dates'].dt.month_name()
    df['daily'] = df['dates'].dt.date
    df['day'] = df['dates'].dt.day
    df['day_name'] = df['dates'].dt.day_name()
    df['hour'] = df['dates'].dt.hour
    df['minute'] = df['dates'].dt.minute

    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + '-' + str(hour + 1))
    df['period'] = period
    return df