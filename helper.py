from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji

extract = URLExtract()
def fetch_stats(selected_user,df):

    if selected_user !='Overall':
       df = df[df['User']== selected_user]

    num_messages = df.shape[0]
    words = []
    for message in df['Message']:
       words.extend(message.split())

    # fetch number of media messages
    # num_media_messages = df[df['Message'] == 'image omitted'].shape[0]
       
    #fetch total number of links 
    links =[]
    for messages in df['Message']:
       links.extend(extract.find_urls(messages))

    return num_messages,len(words),len(links)


def most_busy_users(df):
   x = df['User'].value_counts().head()
   df = round(df['User'].value_counts()/df.shape[0]*100,2).reset_index().rename(columns = {"count" :"Percent" ,'User':'Name'})
   return x,df


def create_word_clod(selected_user,df):
   f = open('stop_hinglish.txt','r')
   stop_words = f.read()
   if selected_user != 'Overall':
        df = df[df['User']==selected_user]

   def remove_stop_words(message):
       y = []
       for word in message.lower().split():
           if word not in stop_words:
               y.append(word)
       return " ".join(y)
    

   wc = WordCloud(width = 500,height =500,min_font_size =10,background_color = 'white')
   df["Message"] = df['Message'].apply(remove_stop_words)
   df_wc = wc.generate(df['Message'].str.cat(sep=" "))
   return df_wc
   
def most_common_words(selected_user,df):
   f = open('stop_hinglish.txt','r')
   stop_words = f.read()
   if selected_user != 'Overall':
        df = df[df['User']==selected_user]

   words = []

   for message in df['Message']:
       for word in message.lower().split():
           if word not in stop_words:
               words.append(word)
   most_common_df = pd.DataFrame(Counter(words).most_common(20))

   return most_common_df
   

def emoji_helper(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['User']==selected_user]
       
    emojis =[]
    for message in df['Message']:
        emojis.extend([c for c in message if c in emoji.UNICODE_EMOJI['en']])


    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return emoji_df


def monthly_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['User']==selected_user]
    
    timeline = df.groupby(['Year','Month_num','Month']).count()['Message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['Month'][i] + "-" +str(timeline['Year'][i]))
    timeline['time'] = time
    return timeline



def daily_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['User']==selected_user]
    
    daily_timeline = df.groupby('Only_date').count()['Message'].reset_index()

    return daily_timeline


def week_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['User']==selected_user]
    return df['day_name'].value_counts()

def month_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['User']==selected_user]
    return df['Month'].value_counts()


def activity_heatmap(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['User']==selected_user]

    user_heatmap = df.pivot_table(index = 'day_name' ,columns = 'period',values = 'Message',aggfunc = 'count').fillna(0)

    return user_heatmap


       
       


       