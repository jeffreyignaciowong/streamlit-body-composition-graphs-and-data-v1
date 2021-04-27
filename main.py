import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from matplotlib import pyplot as plt
import altair as alt
import requests



def rolling7Dayavg(df):
    df['just_date'] = df['Date'].dt.date
    df_avg = df.groupby('just_date').mean().reset_index()
    df_avg['avgLB'] = df_avg['Weight(lb)'].rolling(window=7).mean()
    df_avg = df_avg[['just_date', 'avgLB']]
    df = pd.merge(df, df_avg, how='left')
    # st.dataframe(df)
    return df
    # print(df_avg[['avgLB', 'Date']])
    # print(df_avg.columns)


    # st.line_chart(avgLB.rename(columns={'just_date': 'index'}).set_index('index'))
    # for index, row in df.iterrows():
    #     #currentDate = df['Date'].head(1).tolist()
    #     currentDate = row['Date']
    #     currentDate = currentDate.date()
    #     past7 = currentDate - timedelta(days=6)
    #     #print(type(currentDate.date()))


def averageChange7Day(df):
    currentDate = df['Date'].head(1).tolist()
    if len(currentDate) != 0:
        currentDate = currentDate[0]
    # currentDate = currentDate.date()
    # currentDate.date()
    # print(type(currentDate))
    # print(currentDate.date())
    currentDate = currentDate.date()
    past7 = currentDate - timedelta(days=6)
    past14 = past7 - timedelta(days=7)
    # print(past7)
    index = 0
    workingDate = df.loc[index, 'Date'].date()
    totalRows = len(df.index)
    # print(totalRows)
    past7avg = 0
    while index < totalRows and workingDate >= past7:
        past7avg += df.loc[index, 'Weight(lb)']
        # print(workingDate)
        index += 1
        workingDate = df.loc[index, 'Date'].date()
    if index != 0:
        past7avg = past7avg / index
    # print("past7avg: ")
    # print(past7avg)
    index14Start = index
    count = 0
    past14avg = 0
    while index < totalRows and workingDate >= past14:
        past14avg += df.loc[index, 'Weight(lb)']
        # print(workingDate)
        count += 1
        index += 1
        workingDate = df.loc[index, 'Date'].date()
    if index != 0:
        past14avg = past14avg / (index - index14Start)
    avgGrowth = past7avg - past14avg
    # print("past14avg: ")
    # print(past14avg)
    # print("past7:")
    # print(past7)
    # print(past14)
    # print(avgGrowth)
    st.write(f'Average change from this week to last week is {avgGrowth}')


def graphs(df):
    # date_range_list = ['2 weeks', '1 month', '6 months', '1 year', 'all']
    date_range_list = ['all', '1 year', '6 months', '1 month', '2 weeks']
    date_range = st.sidebar.selectbox('Date Range', date_range_list)
    df = rolling7Dayavg(df)
    # print(df)

    df_displayed = df
    if date_range == '2 weeks':
        # start_date = datetime.today() - timedelta(days=6)
        start_date = datetime.today() - timedelta(days=13)
        print(start_date)
        mask = (df['Date'] > start_date)
        # mask = (df['Date'] == datetime.today())
        print(df.loc[mask])
        df_displayed = df.loc[mask]
    elif date_range == '1 month':
        start_date = datetime.today() - timedelta(days=31)
        print(start_date)
        mask = (df['Date'] > start_date)
        # mask = (df['Date'] == datetime.today())
        print(df.loc[mask])
        df_displayed = df.loc[mask]
    elif date_range == '6 months':
        start_date = datetime.today() - timedelta(days=183)
        print(start_date)
        mask = (df['Date'] > start_date)
        # mask = (df['Date'] == datetime.today())
        print(df.loc[mask])
        df_displayed = df.loc[mask]
    elif date_range == '1 year':
        start_date = datetime.today() - timedelta(days=365)
        print(start_date)
        mask = (df['Date'] > start_date)
        # mask = (df['Date'] == datetime.today())
        print(df.loc[mask])
        df_displayed = df.loc[mask]



    averageChange7Day(df)
    # dfWeight = df_displayed[['Weight(lb)', 'Date']]
    # st.area_chart(dfWeight.rename(columns={'Date': 'index'}).set_index('index'))
    # st.line_chart(dfWeight.rename(columns={'Date': 'index'}).set_index('index'))

    # alt_graph = alt.Chart(df).mark_area(opacity=1).encode(alt.Y('Acceleration:Q', scale=alt.Scale(domain=(140, 100))),
    #                                                       x='Date',
    #                                                       y='Weight(lb)')  # .configure_mark(opacity=0.2, color='red')
    alt_graph = alt.Chart(df_displayed).mark_area(opacity=1).encode(x='Date', y=alt.Y('Weight(lb)', scale=alt.Scale(domain=(120, 150))), tooltip=['Weight(lb)', 'Date'])
    st.altair_chart(alt_graph, use_container_width=True)

    # rolling 7 Day avg graph
    avgLB = df_displayed[['avgLB', 'just_date']]
    avgLB = avgLB.groupby('just_date').mean().reset_index()
    alt_graph_avg = alt.Chart(avgLB).mark_area(opacity=1).encode(x='just_date', y=alt.Y('avgLB', scale=alt.Scale(
        domain=(120, 150))), tooltip=['avgLB', 'just_date'])
    st.altair_chart(alt_graph_avg, use_container_width=True)

    # df_display_body_fat = df_displayed[['Body Fat(%)', 'Date']]
    # df_display_body_fat = df_display_body_fat[df_display_body_fat['Body Fat(%)'] != '--'].reset_index()
    # df_display_body_fat = df_display_body_fat.groupby('just_date').mean().reset_index()

    # df_display_body_fat = df_displayed[df_displayed['Body Fat(%)'] != '--']
    # alt_graph_body_fat = alt.Chart(df_display_body_fat).mark_area(opacity=1).encode(x='Date', y=alt.Y('Body Fat(%)', scale=alt.Scale(
    #     domain=(9, 12))), tooltip=['Body Fat(%)', 'Date'])
    # alt_graph_body_fat = alt.Chart(df_display_body_fat).mark_area(opacity=1).encode(x='Date', y=alt.Y('Body Fat(%)', scale=alt.Scale(domain=(10, 12)), tooltip=['Body Fat(%)', 'Date']))
    # st.altair_chart(alt_graph_body_fat, use_container_width=True)

    # df_display_body_fat = df_displayed[['just_date', 'Body Fat(%)']]
    # print(df_display_body_fat)
    # df_display_body_fat = df_display_body_fat[df_display_body_fat['Body Fat(%)'] != '--']
    # df_display_body_fat.drop_duplicates(subset="just_date", keep='first', inplace=True)

    # df_display_body_fat = df_display_body_fat.rename(columns={'just_date': 'index'}).set_index('index')
    # st.dataframe(df_display_body_fat)
    # print(df_display_body_fat)
    # st.area_chart(df_display_body_fat)
    # st.area_chart(df_display_body_fat.rename(columns={'just_date': 'index'}).set_index('index'))
    # st.line_chart(df_display_body_fat)
    # st.line_chart(df_display_body_fat['Body Fat(%)'])

    # avgLB = df_displayed[['avgLB', 'just_date']]
    # avgLB = avgLB.groupby('just_date').mean().reset_index()
    # st.area_chart(avgLB.rename(columns={'just_date': 'index'}).set_index('index'))




def upload():
    st.subheader("Upload Data")
    data_file = st.file_uploader("Upload CSV", type=["csv"])
    if data_file is not None:
        # st.write(type(data_file))
        df = pd.read_csv(data_file)
        df['Date'] = pd.to_datetime(df['Time of Measurement'])
        graphs(df)
        # st.dataframe(df)
        # st.bar_chart(df['Weight(lb)'].head(50))

        # st.line_chart(df['Weight(lb)'].head(50))
        # alt.chart(df).encode(x='Weight(lb)')
        # plt.plot(df['Weight(lb)'], df.index, label='Weight')
        # st.write(plt)


def jeffSynced():
    st.subheader("Jeff's synced data")
    conversion_kg_lbs = 2.20462262185
    access_token = 'eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyM0I0OUwiLCJzdWIiOiI5Q1lRQ04iLCJpc3MiOiJGaXRiaXQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZXMiOiJ3aHIgd251dCB3cHJvIHdzbGUgd3dlaSB3c29jIHdzZXQgd2FjdCB3bG9jIiwiZXhwIjoxNjUxMDA5ODIwLCJpYXQiOjE2MTk0NzM4MjB9.QzwIB0O4J84NS5Yb2TNiJLboAbZz5W_h-_L5ONF0d8c'
    header = {'Authorization': 'Bearer {}'.format(access_token)}
    response_weight = requests.get('https://api.fitbit.com/1/user/-/body/weight/date/today/1y.json', headers=header).json()
    # response_body_fat = requests.get('https://api.fitbit.com/1/user/-/body/fat/date/today/1y.json', headers=header).json()
    df = pd.json_normalize(response_weight, record_path=['body-weight'])
    # print(response_body_fat)
    # df_body_fat = pd.json_normalize(response_body_fat, record_path=['body-fat'])
    df.rename(columns={'value': 'Weight(lb)'}, inplace=True)
    df['Weight(lb)'] = df['Weight(lb)'].astype(float)
    df['Weight(lb)'] = df['Weight(lb)'] *conversion_kg_lbs
    df['Date'] = pd.to_datetime(df['dateTime'])
    dfWeight = df[['Weight(lb)', 'Date']]
    st.area_chart(dfWeight.rename(columns={'Date': 'index'}).set_index('index'))
    print(df)
    # graphs(df)

def exampleData():
    st.subheader("Example Data")
    df = pd.read_csv('Renpho-Jeff-data#2.csv')
    df['Date'] = pd.to_datetime(df['Time of Measurement'])
    graphs(df)

def main():
    st.title("Body Composition Graphs and Data")
    menu = ["Example Data", "Jeff Synced Data", "Upload"]
    choice = st.sidebar.selectbox("Menu", menu)
    if choice == "Example Data":
        exampleData()
    if choice == "Jeff Synced Data":
        jeffSynced()
    elif choice == "Upload":
        upload()
    # print("hello")


if __name__ == '__main__':
    main()
