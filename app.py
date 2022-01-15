import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import helper
import preprocessor
import seaborn as sns


st.sidebar.title("WhatsApp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
     bytes_data = uploaded_file.getvalue()
     data= bytes_data.decode("Utf-8")
     #st.text(data)
     df= preprocessor.preprocess(data)



     # user list
     user_list= df['user'].unique().tolist()
     user_list.remove('Group Notification')
     user_list.sort()
     user_list.insert(0,'Overall Member')
     selected_user = st.sidebar.selectbox("Analysis With respect to", user_list)

     if st.sidebar.button("Show Analysis"):
          num_messages, words, num_media_messages,link = helper.fetch_stats(selected_user, df)
          st.title("Statistics Analysis")
          col1, col2, col3, col4=st.columns(4)
          with col1:
               st.header("Total Messages")
               st.title(num_messages)
          with col2:
               st.header("Total words")
               st.title(words)
          with col3:
               st.header("Media Shared")
               st.title(num_media_messages)
          with col4:
               st.header("link Shared")
               st.title(link)

          # Monthly-timeline

          st.title('Monthly-based Timeline')
          timeline= helper.month_timeline(selected_user,df)
          fig,ax= plt.subplots()
          ax.plot(timeline['time'], timeline['message'], color='red')
          plt.xticks(rotation='vertical')
          st.pyplot(fig)


          # Daily-timeline

          st.title('Daily-Based Timeline')
          daily_timeline = helper.daily_timeline(selected_user, df)
          fig, ax = plt.subplots()
          ax.plot(daily_timeline['daily'], daily_timeline['message'], color='black')
          plt.xticks(rotation='vertical')
          st.pyplot(fig)

          # Month_wise_activity-map
          st.title("Activity-Map")
          col1,col2= st.columns(2)
          with col1:
               st.header("Month-wise-Activity-map")
               busy_month = helper.month_wise_activity_map(selected_user, df)
               fig, ax = plt.subplots()
               ax.bar(busy_month.index, busy_month.values,color='red')
               plt.xticks(rotation='vertical')
               st.pyplot(fig)

          # Day_wise_activity-map
          with col2:
               st.header("day-wise-Activity-map")
               busy_day = helper.day_wise_activity_map(selected_user, df)
               fig, ax = plt.subplots()
               ax.bar(busy_day.index, busy_day.values,color='green')
               plt.xticks(rotation='vertical')
               st.pyplot(fig)

          # heatmap of activity map
          st.title('Weekly Activity Heatmap')
          user_heatmap= helper.activity_heatmap(selected_user, df)
          fig,ax=plt.subplots()
          ax=sns.heatmap(user_heatmap)
          st.pyplot(fig)




     # find the most busiest user in group

          if selected_user=='Overall Member':
               st.title('Busy user')
               x, new_df= helper.most_active_users(df)
               fig,ax = plt.subplots()


               col1, col2 = st.columns(2)
               with col1:
                    ax.bar(x.index, x.values, color='orange')
                    st.pyplot(fig)

               with col2:
                    st.dataframe(new_df)

          #WordCloud

          st.title('Word Cloud')
          df_wc = helper.create_word_cloud(selected_user, df)
          fig,ax = plt.subplots()
          ax.imshow(df_wc)
          st.pyplot(fig)

          #Most_common_Words
          most_common_df = helper.most_common_words(selected_user,df)

          fig,ax= plt.subplots()
          ax.barh(most_common_df[0],most_common_df[1], color='purple')
          plt.xticks(rotation='vertical')
          st.pyplot(fig)

# emojis Analysis
          emoji_df = helper.emoji_helper(selected_user,df)
          st.title("Emoji Analysis")

          col1, col2 = st.columns(2)
          with col1:
               st.dataframe(emoji_df)

          with col2:
               fig, ax = plt.subplots()
               ax.pie(emoji_df[1].head(), labels= emoji_df[0].head(),autopct="%0.2f")
               st.pyplot(fig)


