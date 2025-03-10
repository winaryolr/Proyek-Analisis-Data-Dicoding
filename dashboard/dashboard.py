import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler

# Load data
allData = pd.read_csv("all-data.csv")

# Konversi kolom datetime
allData['dteday'] = pd.to_datetime(allData['dteday'])

# Judul Dashboard
st.title("Dashboard Analisis Penyewaan Sepeda (Jam)")

# Visualisasi 1: Rata-rata Penyewaan Sepeda per Jam
st.subheader("Rata-rata Penyewaan Sepeda per Jam")
hour_avg = allData.groupby("hr")["cnt"].mean()
fig, ax = plt.subplots()
sns.lineplot(x=hour_avg.index, y=hour_avg.values, marker='o', ax=ax)
ax.set_title("Rata-rata Penyewaan Sepeda per Jam")
ax.set_xlabel("Jam (0-23)")
ax.set_ylabel("Rata-rata Penyewaan")
st.pyplot(fig)

# Visualisasi 2: Rata-rata Penyewaan Sepeda berdasarkan Musim
st.subheader("Rata-rata Penyewaan Sepeda berdasarkan Musim")
season_avg = allData.groupby("season")["cnt"].mean()
fig, ax = plt.subplots()
sns.lineplot(x=season_avg.index, y=season_avg.values, marker='o', ax=ax)
ax.set_title("Rata-rata Penyewaan Sepeda berdasarkan Musim")
ax.set_xlabel("Musim (1: Spring, 2: Summer, 3: Fall, 4: Winter)")
ax.set_ylabel("Rata-rata Penyewaan")
ax.set_xticks([1, 2, 3, 4])
ax.set_xticklabels(['Spring', 'Summer', 'Fall', 'Winter'])
st.pyplot(fig)

# Visualisasi 3: Rata-rata Penyewaan Sepeda berdasarkan Cuaca
st.subheader("Rata-rata Penyewaan Sepeda berdasarkan Cuaca")
weather_avg = allData.groupby("weathersit")["cnt"].mean()
fig, ax = plt.subplots()
sns.lineplot(x=weather_avg.index, y=weather_avg.values, marker='o', ax=ax)
ax.set_title("Rata-rata Penyewaan Sepeda berdasarkan Cuaca")
ax.set_xlabel("Cuaca (1: Cerah, 2: Berawan, 3: Hujan Ringan)")
ax.set_ylabel("Rata-rata Penyewaan")
ax.set_xticks([1, 2, 3, 4])
ax.set_xticklabels(['Cerah', 'Berawan', 'Hujan Ringan', 'Hujan Lebat'])
st.pyplot(fig)

# Visualisasi 4: Kondisi Ideal Penyewaan Sepeda (Normalized)
st.subheader("Kondisi Ideal Penyewaan Sepeda (Normalized)")
hour_avg = allData.groupby("hr")["cnt"].mean().reset_index()
season_avg = allData.groupby("season")["cnt"].mean().reset_index()
weather_avg = allData.groupby("weathersit")["cnt"].mean().reset_index()
scaler = MinMaxScaler()
hour_avg["cnt_normalized"] = scaler.fit_transform(hour_avg[["cnt"]])
season_avg["cnt_normalized"] = scaler.fit_transform(season_avg[["cnt"]])
weather_avg["cnt_normalized"] = scaler.fit_transform(weather_avg[["cnt"]])
combined_df = pd.concat([
    hour_avg.rename(columns={"hr": "category", "cnt_normalized": "value"}).assign(feature="hour"),
    season_avg.rename(columns={"season": "category", "cnt_normalized": "value"}).assign(feature="season"),
    weather_avg.rename(columns={"weathersit": "category", "cnt_normalized": "value"}).assign(feature="weather")
])
fig, ax = plt.subplots(figsize=(15, 8))
sns.scatterplot(x="category", y="value", hue="feature", data=combined_df, ax=ax)
ax.set_title("Kondisi Ideal Penyewaan Sepeda (Normalized)")
ax.tick_params(axis='x', rotation=45)
ax.axhline(y=0.8, color='r', linestyle='--', label='Garis y = 0.8')
ax.legend()
st.pyplot(fig)

# Clustering Kondisi Penyewaan Sepeda (Binning)
st.subheader("Clustering Kondisi Penyewaan Sepeda (Binning)")
bins = [0, 0.3, 0.7, 1]
labels = ["Rendah", "Sedang", "Tinggi"]
combined_df["cluster"] = pd.cut(combined_df["value"], bins=bins, labels=labels)
fig, ax = plt.subplots(figsize=(15, 8))
sns.scatterplot(x="category", y="value", hue="cluster", data=combined_df, ax=ax)
ax.set_title("Clustering Kondisi Penyewaan Sepeda (Binning)")
ax.tick_params(axis='x', rotation=45)
st.pyplot(fig)

# Rata-rata Penyewaan Sepeda per Fitur
st.subheader("Rata-rata Penyewaan Sepeda per Fitur")
grouped_df = combined_df.groupby("feature")["value"].mean().reset_index()
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x="feature", y="value", data=grouped_df, ax=ax)
ax.set_title("Rata-rata Penyewaan Sepeda per Fitur")
ax.tick_params(axis='x', rotation=45)
st.pyplot(fig)

st.caption("Dashboard ini menampilkan analisis penyewaan sepeda berdasarkan data jam.")
