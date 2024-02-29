import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
sns.set(style='dark')


## Load data
day_df = pd.read_csv("day_data.csv")
hour_df = pd.read_csv("hour_data.csv")

datetime_columns = ["dteday"]
day_df.sort_values(by="dteday", inplace=True)
day_df.reset_index(inplace=True)

for column in datetime_columns:
    day_df[column] = pd.to_datetime(day_df[column])

min_date = day_df["dteday"].min()
max_date = day_df["dteday"].max()

with st.sidebar:
    st.image("https://raw.githubusercontent.com/redshoes11/DatasetProyekAkhirDicoding/main/robot_1693881.png")

    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu', min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )


# Melengkapi dashboard dengan berbagai visualisasi data

st.header('Bike Sharing Dashboard :sparkles:')

# Menampilkan Sialy Bike Sharing 2011
st.subheader('Daily Bike Sharing 2011')

monthly2011_df = day_df[day_df['dteday'].dt.year == 2011]

monthly2011_sharing_df = monthly2011_df.resample(rule='M', on='dteday').agg({
    "instant": "nunique",
    "cnt": "sum"
})
monthly2011_sharing_df.index = monthly2011_sharing_df.index.strftime('%B') # mengubah format order date menjadi nama bulan

monthly2011_sharing_df = monthly2011_sharing_df.reset_index()
monthly2011_sharing_df.rename(columns={
    "instant": "sharing_id",
    "cnt": "total_sharing"
}, inplace=True)

col1, col2 = st.columns(2)

with col1:
    total_sharing = monthly2011_df.cnt.sum()
    st.metric("Total Sharing", value=total_sharing)

with col2:
    highest_count = monthly2011_sharing_df.total_sharing.max()
    st.metric("Highest Sharing (Month) : ", value=highest_count)

fig, ax = plt.subplots(figsize=(16, 8))

ax.plot(
    monthly2011_sharing_df["dteday"],
    monthly2011_sharing_df["total_sharing"],
    marker='o',
    linewidth=2,
    color='C3'
)

ax.set_title("Number of Sharing per Month (2011)", loc="center", fontsize=30)
ax.set_ylabel("Count Sharing", fontsize=18)
ax.set_xlabel("Months", fontsize=18)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)


st.pyplot(fig)

# Menampilkan Sialy Bike Sharing 2012

st.subheader('Daily Bike Sharing 2012')

monthly2012_df = day_df[day_df['dteday'].dt.year == 2012]

monthly2012_sharing_df = monthly2012_df.resample(rule='M', on='dteday').agg({
    "instant": "nunique",
    "cnt": "sum"
})
monthly2012_sharing_df.index = monthly2012_sharing_df.index.strftime('%B') # mengubah format order date menjadi nama bulan

monthly2012_sharing_df = monthly2012_sharing_df.reset_index()
monthly2012_sharing_df.rename(columns={
    "instant": "sharing_id",
    "cnt": "total_sharing"
}, inplace=True)

col1, col2 = st.columns(2)

with col1:
    total_sharing = monthly2012_df.cnt.sum()
    st.metric("Total Sharing", value=total_sharing)

with col2:
    highest_count = monthly2012_sharing_df.total_sharing.max()
    st.metric("Highest Sharing (Month) ", value=highest_count)

fig, ax = plt.subplots(figsize=(16, 8))

ax.plot(
    monthly2012_sharing_df["dteday"],
    monthly2012_sharing_df["total_sharing"],
    marker='o',
    linewidth=2,
    color='C3'
)

ax.set_title("Number of Sharing per Month (2012)", loc="center", fontsize=30)
ax.set_ylabel("Count Sharing", fontsize=18)
ax.set_xlabel("Months", fontsize=18)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)

st.pyplot(fig)

# Menampilkan The Influence of Weather on Bike Sharing Rates
st.subheader('The Influence of Weather on Bike Sharing Rates')
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(16, 8))

sns.barplot(data=day_df, x="weathersit", y="cnt", hue="yr", errorbar=None, palette='magma', ax=ax[0])
ax[0].set_ylabel('Count')
ax[0].set_xlabel('Weathersit')
ax[0].set_title("Weathersit vs Count in Bike Sharing 2011-2012", loc="center", fontsize=15)

plt.legend(title='Year', labels=['2011', '2012'])

sns.scatterplot(x='temp', y='cnt', hue='yr', data=day_df, palette='magma', ax=ax[1])
ax[1].set_ylabel('Count')
ax[1].set_xlabel('Temperature')
ax[1].set_title("Temperature vs Count in Bike Sharing 2011-2012", loc="center", fontsize=15)

plt.legend(title='Year', labels=['', '2012', '2013'])

st.pyplot(fig)

#
st.subheader('Best and worst Performing Season by Number of Bike Sharing 2011-2012')

season_sharing_df = day_df.groupby("season").cnt.sum().sort_values(ascending=False).reset_index()
season_sharing_df['season'] = season_sharing_df['season'].astype(str)
category_mapping = {'1': 'Spring', '2': 'Summer', '3': 'Fall', '4': 'Winter'}
season_sharing_df['season'].replace(category_mapping, inplace=True)
season_sharing_df['season'] = season_sharing_df['season'].astype('category')

col1, col2 = st.columns(2)


with col1:
    best_season = season_sharing_df.cnt.max()
    st.write("Best Season")
    s = f"<p style='font-size:30px;'>{'FALL'}</p>"
    st.markdown(s, unsafe_allow_html=True)
    st.metric("Total ", value=best_season)


with col2:
    worst_season = season_sharing_df.cnt.min()
    st.write("Worst Season")
    s = f"<p style='font-size:30px;'>{'SPRING'}</p>"
    st.markdown(s, unsafe_allow_html=True)
    st.metric("Total ", value=worst_season)

fig, ax= plt.subplots(nrows=1, ncols=1, figsize=(15, 7))

sns.barplot(x="cnt", y="season", data=season_sharing_df, palette='magma')
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis ='y', labelsize=12)

plt.suptitle("Best and Worst Performing Season by Number of Sharing", fontsize=20)
plt.show()

st.pyplot(fig)


# Menampilkan Hour vs Count in Bike Sharing 2011-2012
st.subheader('Hour vs Count in Bike Sharing 2011-2012')

f, ax = plt.subplots(figsize=(10, 5))

sns.lineplot(x='hr', y='cnt', data=hour_df, hue='yr', errorbar=None, palette='magma')
ax.set_ylabel('Count')
ax.set_xlabel('Hour')
ax.set_title("Hour vs Count in Bike Sharing 2011-2012", loc="center", fontsize=15)

plt.legend(title='Year', labels=['2011', '2012'])

st.pyplot(f)

st.caption('Copyright (c) Tessa Agitha 2023')


