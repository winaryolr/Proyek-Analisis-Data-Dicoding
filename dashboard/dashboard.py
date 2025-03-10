import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("all-data.csv")
    df['dteday'] = pd.to_datetime(df['dteday'])
    return df

allData = load_data()

# Fungsi untuk visualisasi
def plot_hour_avg(df):
    hour_avg = df.groupby("hr")["cnt"].mean().reset_index()
    fig, ax = plt.subplots()
    sns.lineplot(x="hr", y="cnt", data=hour_avg, marker='o', ax=ax)
    ax.set_title("Rata-rata Penyewaan Sepeda per Jam")
    ax.set_xlabel("Jam (0-23)")
    ax.set_ylabel("Rata-rata Penyewaan")
    st.pyplot(fig)

def plot_season_avg(df):
    season_avg = df.groupby("season")["cnt"].mean().reset_index()
    fig, ax = plt.subplots()
    sns.barplot(x="season", y="cnt", data=season_avg, ax=ax)
    ax.set_title("Rata-rata Penyewaan Sepeda berdasarkan Musim")
    ax.set_xlabel("Musim")
    ax.set_ylabel("Rata-rata Penyewaan")
    ax.set_xticklabels(['Spring', 'Summer', 'Fall', 'Winter'])
    st.pyplot(fig)

def plot_weather_avg(df):
    weather_avg = df.groupby("weathersit")["cnt"].mean().reset_index()
    fig, ax = plt.subplots()
    sns.barplot(x="weathersit", y="cnt", data=weather_avg, ax=ax)
    ax.set_title("Rata-rata Penyewaan Sepeda berdasarkan Cuaca")
    ax.set_xlabel("Cuaca")
    ax.set_ylabel("Rata-rata Penyewaan")
    ax.set_xticklabels(['Cerah', 'Berawan', 'Hujan Ringan', 'Hujan Lebat'])
    st.pyplot(fig)

def plot_normalized_data(df):
    scaler = MinMaxScaler()
    
    hour_avg = df.groupby("hr")["cnt"].mean().reset_index()
    season_avg = df.groupby("season")["cnt"].mean().reset_index()
    weather_avg = df.groupby("weathersit")["cnt"].mean().reset_index()
    
    hour_avg["cnt_normalized"] = scaler.fit_transform(hour_avg[["cnt"]])
    season_avg["cnt_normalized"] = scaler.fit_transform(season_avg[["cnt"]])
    weather_avg["cnt_normalized"] = scaler.fit_transform(weather_avg[["cnt"]])

    combined_df = pd.concat([
        hour_avg.rename(columns={"hr": "category", "cnt_normalized": "value"}).assign(feature="hour"),
        season_avg.rename(columns={"season": "category", "cnt_normalized": "value"}).assign(feature="season"),
        weather_avg.rename(columns={"weathersit": "category", "cnt_normalized": "value"}).assign(feature="weather")
    ])

    fig, ax = plt.subplots(figsize=(12, 6))
    sns.scatterplot(data=combined_df, x="category", y="value", hue="feature", ax=ax)
    ax.set_title("Kondisi Ideal Penyewaan Sepeda (Normalized)")
    ax.axhline(y=0.8, color='r', linestyle='--', label='Garis y = 0.8')
    ax.legend()
    st.pyplot(fig)

def plot_clustered_data(df):
    scaler = MinMaxScaler()

    hour_avg = df.groupby("hr")["cnt"].mean().reset_index()
    season_avg = df.groupby("season")["cnt"].mean().reset_index()
    weather_avg = df.groupby("weathersit")["cnt"].mean().reset_index()
    
    hour_avg["cnt_normalized"] = scaler.fit_transform(hour_avg[["cnt"]])
    season_avg["cnt_normalized"] = scaler.fit_transform(season_avg[["cnt"]])
    weather_avg["cnt_normalized"] = scaler.fit_transform(weather_avg[["cnt"]])

    combined_df = pd.concat([
        hour_avg.rename(columns={"hr": "category", "cnt_normalized": "value"}).assign(feature="hour"),
        season_avg.rename(columns={"season": "category", "cnt_normalized": "value"}).assign(feature="season"),
        weather_avg.rename(columns={"weathersit": "category", "cnt_normalized": "value"}).assign(feature="weather")
    ])

    bins = [0, 0.3, 0.7, 1]
    labels = ["Rendah", "Sedang", "Tinggi"]
    combined_df["cluster"] = pd.cut(combined_df["value"], bins=bins, labels=labels)

    fig, ax = plt.subplots(figsize=(12, 6))
    sns.scatterplot(data=combined_df, x="category", y="value", hue="cluster", ax=ax)
    ax.set_title("Clustering Kondisi Penyewaan Sepeda (Binning)")
    st.pyplot(fig)

def plot_feature_avg(df):
    scaler = MinMaxScaler()

    hour_avg = df.groupby("hr")["cnt"].mean().reset_index()
    season_avg = df.groupby("season")["cnt"].mean().reset_index()
    weather_avg = df.groupby("weathersit")["cnt"].mean().reset_index()
    
    hour_avg["cnt_normalized"] = scaler.fit_transform(hour_avg[["cnt"]])
    season_avg["cnt_normalized"] = scaler.fit_transform(season_avg[["cnt"]])
    weather_avg["cnt_normalized"] = scaler.fit_transform(weather_avg[["cnt"]])

    combined_df = pd.concat([
        hour_avg.rename(columns={"hr": "category", "cnt_normalized": "value"}).assign(feature="hour"),
        season_avg.rename(columns={"season": "category", "cnt_normalized": "value"}).assign(feature="season"),
        weather_avg.rename(columns={"weathersit": "category", "cnt_normalized": "value"}).assign(feature="weather")
    ])

    grouped_df = combined_df.groupby("feature")["value"].mean().reset_index()

    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(data=grouped_df, x="feature", y="value", ax=ax)
    ax.set_title("Rata-rata Penyewaan Sepeda per Fitur")
    st.pyplot(fig)

# Dashboard
st.title("Dashboard Analisis Penyewaan Sepeda")

st.subheader("Rata-rata Penyewaan Sepeda per Jam")
plot_hour_avg(allData)

st.subheader("Rata-rata Penyewaan Sepeda berdasarkan Musim")
plot_season_avg(allData)

st.subheader("Rata-rata Penyewaan Sepeda berdasarkan Cuaca")
plot_weather_avg(allData)

st.subheader("Kondisi Ideal Penyewaan Sepeda (Normalized)")
plot_normalized_data(allData)

st.subheader("Clustering Kondisi Penyewaan Sepeda (Binning)")
plot_clustered_data(allData)

st.subheader("Rata-rata Penyewaan Sepeda per Fitur")
plot_feature_avg(allData)

st.caption("Dashboard ini menampilkan analisis penyewaan sepeda berdasarkan data historis.")
