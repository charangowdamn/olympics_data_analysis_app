import streamlit as st
import pandas as pd
import preprocessor,helper
import plotly.express as px
import plotly.figure_factory as ff
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')

df = preprocessor.preprocess(df,region_df)
st.sidebar.title('Olympic Analysis')
st.sidebar.image('PinClipart.com_social-media-clip-art_514847.png')
user_menu = st.sidebar.radio(
    'SELECT AN OPTION',
    ('Medal Tally','Overall Analysis','Country-wise Analysis','Athlete-wise Analysis')
)

if user_menu == 'Medal Tally':

    years,country = helper.country_year_list(df)

    selected_year = st.sidebar.selectbox("select year",years)
    selected_country = st.sidebar.selectbox("select country", country)

    medal_tally = helper.fetch_medal_tally(df,selected_year,selected_country)
    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title("Overall Tally")
    if selected_year != 'Overall' and selected_country == 'Overall':
        st.title(f"Medal Tally in {selected_year} Olympics")
    if selected_year == 'Overall' and selected_country != 'Overall':
        st.title(f"Overall Performance of {selected_country}")
    if selected_year != 'Overall' and selected_country != 'Overall':
        st.title(f"{selected_country} performance in {selected_year} Olympics")

    st.table(medal_tally)

if user_menu == 'Overall Analysis':
    editions =df['Year'].unique().shape[0]-1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    regions = df['region'].unique().shape[0]
    st.title("Top Statistics")
    col1,col2,col3 = st.columns(3)
    with col1:
        st.header("Editions")
        st.title(editions)
    with col2:
        st.header("Hosts")
        st.title(cities)
    with col3:
        st.header("sports")
        st.title(sports)

    col4, col5, col6 = st.columns(3)
    with col4:
        st.header("Events")
        st.title(events)
    with col5:
        st.header("Nations")
        st.title(regions)
    with col6:
        st.header("Athletes")
        st.title(athletes)

    nations_over_time = helper.data_over_time(df,'region')
    fig = px.line(nations_over_time, x="Edition", y="region",labels={'Name':'No of Nations'})
    st.title("Participating Nations Over The Years")
    st.plotly_chart(fig)


    Events_over_time = helper.data_over_time(df, 'Event')
    fig = px.line(Events_over_time, x="Edition", y='Event',labels={'Name':'No of Events'})
    st.title("Participating Events Over The Years")
    st.plotly_chart(fig)

    Events_over_time = helper.data_over_time(df, 'Name')
    fig = px.line(Events_over_time, x="Edition", y='Name' , labels={'Name':'No of Athletes'})
    st.title("Athletes Over The Years")
    st.plotly_chart(fig)

    st.title("No of Events over time(Every Sport)")
    fig,ax = plt.subplots(figsize=(20,20))
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    ax = sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'),
                annot=True)
    st.pyplot(fig)

    st.title("Most succesfull Athletes")
    sport_list = df['Sport'].unique().tolist()
    sport_list.insert(0,'Overall')
    selected_sport = st.selectbox('Select a Sport',sport_list)
    x = helper.most_succesfull(df,selected_sport)
    st.table(x)

if user_menu == 'Country-wise Analysis':
    st.sidebar.title('Country-wise Analysis')
    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()

    selected_country =st.sidebar.selectbox('Select a Country',country_list)
    country_df = helper.yearwise_medal_tally(df,selected_country)
    fig = px.line(country_df, x="Year", y="Medal")
    st.title(f"{selected_country} Medal Tally over The Years")
    st.plotly_chart(fig)

    pt = helper.country_event_heat_map(df,selected_country)
    st.title(f"{selected_country} Excels in the following Sports")
    fig, ax = plt.subplots(figsize=(20, 20))
    ax = sns.heatmap(pt,annot=True)
    st.pyplot(fig)

    st.title(f'Top 10 Athletes of {selected_country}')
    top_10df = helper.most_succesfull_country_wise(df,selected_country)
    st.table(top_10df)

if user_menu == 'Athlete-wise Analysis':
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()
    fig = ff.create_distplot([x1, x2, x3, x4], ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],
                             show_hist=False, show_rug=False)
    fig.update_layout(autosize=False,width=1000,height=600)
    st.title('Distribution Of Age')
    st.plotly_chart(fig)

    x =[]
    name = []
    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                     'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                     'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                     'Water Polo', 'Hockey', 'Rowing', 'Fencing',
                     'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                     'Tennis', 'Golf', 'Softball', 'Archery',
                     'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                     'Rhythmic Gymnastics', 'Rugby Sevens',
                     'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']
    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport']==sport]
        x.append(temp_df[temp_df['Medal']=='Gold']['Age'].dropna())
        name.append(sport)
    fig = ig = ff.create_distplot(x, name,
                             show_hist=False, show_rug=False)
    fig.update_layout(autosize=False,width=1000,height=600)
    st.title('Distribution Of Age wrt Sports (Gold Medalist)')
    st.plotly_chart(fig)


    st.title('Height vs Weight')
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')
    selected_sport = st.selectbox('Select a Sport', sport_list)
    temp_df = helper.weight_v_height(df,selected_sport)
    fig,ax = plt.subplots()
    ax = sns.scatterplot(temp_df['Weight'],temp_df['Height'],hue=temp_df['Medal'],style = temp_df['Sex'],s=60)
    st.pyplot(fig)

    st.title('Men Vs Women Participation Over the Years')
    final = helper.men_vs_women(df)
    fig = px.line(final, x='Year', y=['Male', 'Female'])
    fig.update_layout(autosize=False, width=1000, height=600)
    st.plotly_chart(fig)
