import streamlit as st
import preprocessor
import helper
import matplotlib.pyplot as plt

st.sidebar.title("WhatsApp Chat Analyzer")
uploaded_file=st.sidebar.file_uploader("choose a file")
if uploaded_file is not None:
    bytes_data=uploaded_file.getvalue()
    data=bytes_data.decode("utf-8")
    df=preprocessor.preprocess(data)
    
    user_list=df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,"Overall")

    selected_user=st.sidebar.selectbox("show analysis wrt ", user_list)
    if st.sidebar.button("Show Analysis"):
        st.title("Top Statistics")
        col1, col2, col3, col4 = st.columns(4)
        num_messages, num_words, num_media_messages, num_links = helper.fetch_stats(selected_user,df)
        with col1:
            st.header("Total messages")
            st.title(num_messages)
        with col2:
            st.header("Total words")
            st.title(num_words)
        with col3:
            st.header("Total media messages")
            st.title(num_media_messages)
        with col4:
            st.header("Total links")
            st.title(num_links)
        st.title("Monthly Timeline")        
        timeline=helper.monthly_timeline(selected_user,df)
        plt.plot(timeline['time'],timeline['message'],color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(plt)        
        if selected_user=='Overall':
            st.title("most busy users")
            x,y=helper.most_busy_users(df)
            col1, col2 = st.columns(2)
            fig, ax = plt.subplots()
            with col1:
                ax.bar(x.index, x.values, color='orange')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(y)
        st.title("WordCloud")            
        df_wc = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        ax.axis("off")
        st.pyplot(fig)


        st.title("Most Common Words")
        fig, ax = plt.subplots(figsize=(10, 6))

        common_df = helper.most_common_words(selected_user, df)

        ax.bar(
            common_df['Word'],
            common_df['Frequency'],
            color='green'
            )

        plt.tight_layout()
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
    
    st.title("Weekly Timeline Activity Map")

    busy_day = helper.weekly_timeline(selected_user, df)

    fig, ax = plt.subplots(figsize=(8, 5))

    ax.bar(busy_day.index, busy_day.values, color='red')
    ax.set_xticklabels(busy_day.index, rotation=90)

    st.pyplot(fig)