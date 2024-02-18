import streamlit as st
import preprocessor
import helper
import matplotlib.pyplot as plt
import seaborn as sns
# from wordcloud import wordcloud

st.sidebar.title("Whatsapp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)
    # st.dataframe(df)------>through this i can print the whole data frame 

    #fetch unique users

    user_list = df['User'].unique().tolist()
    # user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,"Overall")

    selected_user = st.sidebar.selectbox("Show Analysis wrt", user_list)

    if st.sidebar.button("Show Analysis"):

        num_messages , words,num_links = helper.fetch_stats(selected_user,df)
        
        st.title("Top Statistics")
        col1,col2,col3= st.columns(3)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total  Words")
            st.title(words)
        with col3:
            st.header('Links shared')
            st.title(num_links)

        #monthly timeline
        st.title("Monthly Timeline")    
        timeline = helper.monthly_timeline(selected_user,df)
        fig,ax = plt.subplots()
        ax.plot(timeline['time'],timeline['Message'],color = 'green')
        plt.xticks(rotation = 'vertical')
        st.pyplot(fig)

        #daily timeline
        st.title("Daily Timeline")    
        dailytimeline = helper.daily_timeline(selected_user,df)
        fig,ax = plt.subplots()
        ax.plot(dailytimeline['Only_date'],dailytimeline['Message'],color = 'black')
        # plt.xticks(rotation = ')
        st.pyplot(fig)
        

        #activity map
        st.title("Activity Map")

        col1,col2 = st.columns(2)
        with col1:
            st.header("Most Busy Day")
            busy_day = helper.week_activity_map(selected_user,df)
            fig,ax = plt.subplots()
            ax.bar(busy_day.index,busy_day.values)
            st.pyplot(fig)
        
        with col2:
            st.header("Most Busy Month")
            busy_month = helper.month_activity_map(selected_user,df)
            fig,ax = plt.subplots()
            ax.bar(busy_month.index,busy_month.values,color = 'purple')
            plt.xticks(rotation = 'vertical')
            st.pyplot(fig)



            
        #heatmap 
        st.title("Weekly Activity Map")
        user_heatmap = helper.activity_heatmap(selected_user,df)
        fig,ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)



        # finding the busiest users in the group (only for group level)
            
        if selected_user =='Overall':
            st.title("Most busy users")
            x ,new_df= helper.most_busy_users(df)
            fig,ax = plt.subplots()
            
            col1,col2 = st.columns(2)

            with col1:
                ax.bar(x.index,x.values,color = 'red')
                plt.xticks(rotation = 'vertical')
                st.pyplot(fig)

            with col2:
                st.dataframe(new_df)
        
        #wordcloud
        st.title("WordCloud")
        df_wc = helper.create_word_clod(selected_user,df)
        fig,ax = plt.subplots()
        plt.imshow(df_wc)
        st.pyplot(fig)


        # most common words

        most_common_df = helper.most_common_words(selected_user,df)

        fig,ax = plt.subplots()
        ax.barh(most_common_df[0],most_common_df[1])
        plt.xticks(rotation ='vertical')
        st.title("Most Common Words")

        st.pyplot(fig)
        

        # st.dataframe(most_common_df)

        # emoji analysis
        st.title("Emoji Analysis")
        emoji_df = helper.emoji_helper(selected_user ,df)
        if len(emoji_df) == 0:
            st.title("No Emoji Used")
        
        else:

            col1,col2 = st.columns(2)
            with col1:

                st.dataframe(emoji_df)

            with col2:
                explode = (0.1,0.1,0,0,0)
                fig,ax = plt.subplots()
                ax.pie(emoji_df[1].head(),explode=explode,labels = emoji_df[0].head(),autopct='%1.1f%%')
                st.pyplot(fig)


        


        



         


    