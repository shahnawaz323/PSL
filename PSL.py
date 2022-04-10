import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import streamlit as st
import numpy as np
import seaborn as sns


st.set_page_config(layout='wide')
st.title('Pakistan Super League Analysis')
st.write('This analysis was performed using the data avalaible on PSL 2019')


Headers=['Over_Ball','Batting_Team','Striking_Batsman','Non_Striking_Batsman','Bowler','Runs_Scored','Extras','Fallen_Wickets','Stadium','Cumulative_Runs_Scored','Bowling_Team','Final_Score']
df=pd.read_csv('psl.csv',names=Headers)
df.head()

df.dropna( subset=['Batting_Team','Striking_Batsman','Non_Striking_Batsman','Bowler','Runs_Scored','Extras','Fallen_Wickets','Stadium','Cumulative_Runs_Scored','Bowling_Team','Final_Score'],axis=0, inplace=True)


corr=df.corr()
fig = plt.figure(figsize=(12,8))
sns.heatmap(corr,vmax=.3, square=True,annot=True)
st.pyplot(fig)
st.set_option('deprecation.showPyplotGlobalUse', False)


if isinstance(df, (pd.DatetimeIndex, pd.MultiIndex)):
	df = df.to_frame(index=False)

# remove any pre-existing indices for ease of use , but this is not required
df = df.reset_index().drop('index', axis=1, errors='ignore')
df.columns = [str(c) for c in df.columns]  # update columns to strings in case they are numbers

chart_data = pd.concat([
	df['Batting_Team'],
	df['Final_Score'],
], axis=1)
chart_data = chart_data.sort_values(['Batting_Team'])
chart_data = chart_data.rename(columns={'Batting_Team': 'x'})
chart_data = chart_data.groupby(['x'])[['Final_Score']].mean().reset_index()
chart_data = chart_data.dropna()

import plotly.graph_objs as go

charts = []
charts.append(go.Bar(
    x=chart_data['x'],
    y=chart_data['Final_Score']
))
figure = go.Figure(data=charts, layout=go.Layout({
    'barmode': 'group',
    'legend': {'orientation': 'h'},
    'title': {'text': 'Final_Score by Batting_Team (Mean)'},
    'xaxis': {'title': {'text': 'Batting_Team'}},
    'yaxis': {'tickformat': '.0f', 'title': {'text': 'Final_Score (Mean)'}}
}))


st.plotly_chart(figure)



df['Fallen_Wickets'] = df['Fallen_Wickets'] / 100

select_names = st.sidebar.multiselect('Select a Batter for chart # 1', df['Striking_Batsman'].unique(),
                                      help='Select one or many')

                                      
if len(select_names) > 0:
    select_names = select_names
else:
    select_names = df['Striking_Batsman'].unique()

st.subheader("Chart # 1")
fig = px.scatter(data_frame=df[df['Striking_Batsman'].isin(select_names)], 
                x='Final_Score', 
                y='Over_Ball', 
                size='Cumulative_Runs_Scored',
                hover_name='Striking_Batsman',
                marginal_x='box',
                marginal_y='box',
                title='Overs faced by Batters'
)

fig.update_yaxes(tickformat='%')

st.plotly_chart(fig)
# 
names = st.selectbox('Select a Stadium for the below chart', df['Stadium'].unique(),
                                      help='Select one or many')
  
st.subheader("Chart # 2")                                     
fig = px.scatter(data_frame=df[df['Stadium'].isin([names])],
                x='Extras',
                y='Final_Score',
                size='Fallen_Wickets',
                color='Batting_Team',
                hover_name='Bowler',
                title='Extras effect on Final Score at different stadiums'
)

fig.update_yaxes(tickformat=".")

st.plotly_chart(fig)
# 


bowler = st.selectbox('Select a Batting team', df['Batting_Team'].unique(),
                                      help='Select one or many')
# 
select_cols = ['Batting_Team', 'Striking_Batsman','Runs_Scored', 'Fallen_Wickets', 'Stadium',
       'Cumulative_Runs_Scored', 'Bowling_Team', 'Final_Score']
# 
fg_by_distance = df[select_cols]
#fg_distance_df = (pd.melt(fg_by_distance, id_vars=['Striking_Batsman', 'Bowling_Team'], 
 #                        var_name='Extras', value_name='Final_Score'))
                           
                           
st.subheader("Chart # 3") 
fig= px.scatter(data_frame=fg_by_distance[fg_by_distance['Batting_Team'].isin([bowler])],
            x='Striking_Batsman',
            y='Final_Score',
            color='Bowling_Team',
             title='Team batting performance against each team'
)
# 
fig.update_yaxes(tickformat='.')
# 
st.plotly_chart(fig)     

batsman =  st.radio('Select a Bowling team', df['Bowling_Team'].unique(),
                                      help='Select one or many')

st.subheader("Chart # 4") 
fig= px.scatter(data_frame=df[df['Bowling_Team'].isin([batsman])],
            x='Bowler',
            y='Final_Score',
            color='Batting_Team',
             title='Team Bowling performance against each team'
)
# 
fig.update_yaxes(tickformat='.')
# 
st.plotly_chart(fig) 

st.markdown("The Data for the above charts")
st.dataframe(df)

