import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

sns.set(style='dark')

def create_weekday_avg(df):
    """Menghitung rata-rata penyewaan sepeda per hari."""
    weekday_avg = df.groupby("weekday")["cnt"].mean().reset_index()
    weekday_avg.rename(columns={"cnt": "average_cnt"}, inplace=True)
    return weekday_avg

def create_month_avg(df):
    """Menghitung rata-rata penyewaan sepeda per bulan."""
    month_avg = df.groupby("mnth")["cnt"].mean().reset_index()
    month_avg.rename(columns={"cnt": "average_cnt"}, inplace=True)
    return month_avg

def create_hour_avg(df):
    """Menghitung rata-rata penyewaan sepeda per jam."""
    hour_avg = df.groupby("hr")["cnt"].mean().reset_index()
    hour_avg.rename(columns={"cnt": "average_cnt"}, inplace=True)
    return hour_avg

def create_season_avg(df):
    """Menghitung rata-rata penyewaan sepeda per musim."""
    season_avg = df.groupby("season")["cnt"].mean().reset_index()
    season_avg.rename(columns={"cnt": "average_cnt"}, inplace=True)
    return season_avg

def create_weather_avg(df):
    """Menghitung rata-rata penyewaan sepeda per kondisi cuaca."""
    weather_avg = df.groupby("weathersit")["cnt"].mean().reset_index()
    weather_avg.rename(columns={"cnt": "average_cnt"}, inplace=True)
    return weather_avg

theData_df = pd.read_csv("all-data.csv")

#Proses membuat filtering
theData_df['dteday'] = pd.to_datetime(theData_df['dteday'])

min_date = theData_df["dteday"].min()
max_date = theData_df["dteday"].max()

with st.sidebar:
    start_date, end_date = st.date_input(
        label='Jangka Hari', min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = theData_df[(theData_df["dteday"] >= start_date) & (theData_df["dteday"] <= end_date)]

weekday_avg = create_weekday_avg(theData_df)
month_avg = create_month_avg(theData_df)
hour_avg = create_hour_avg(theData_df)
season_avg = create_season_avg(theData_df)
weather_avg = create_weather_avg(theData_df)

st.header('Proyek Analisis Data')
st.subheader('Statistik Penyewaan Sepeda')

# Visualisas 1: terkena filter
col1, col2 = st.columns(2)

with col1:
    total_avg_weekday = weekday_avg['average_cnt'].mean()
    st.metric("Rata-rata Penyewaan per Hari", value=round(total_avg_weekday, 2))

with col2:
    total_avg_month = month_avg['average_cnt'].mean()
    st.metric("Rata-rata Penyewaan per Bulan", value=round(total_avg_month, 2))

# Plot
st.subheader("Rata-rata Penyewaan Sepeda")

fig, axes = plt.subplots(5, 1, figsize=(16, 20))

# Plot 1: Rata-rata Penyewaan Sepeda per-hari
sns.lineplot(x=weekday_avg['weekday'], y=weekday_avg['average_cnt'], marker='o', ax=axes[0])
axes[0].set_title("Rata-rata Penyewaan Sepeda per-hari")
axes[0].set_xlabel("Hari")
axes[0].set_ylabel("Rata-rata Penyewaan")
axes[0].set_xticks([0, 1, 2, 3, 4, 5, 6])
axes[0].set_xticklabels(['Minggu', 'Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu'], rotation=45)
axes[0].grid(True)

# Plot 2: Rata-rata Penyewaan Sepeda per Bulan
sns.lineplot(x=month_avg['mnth'], y=month_avg['average_cnt'], marker='o', ax=axes[1])
axes[1].set_title("Rata-rata Penyewaan Sepeda per Bulan")
axes[1].set_xlabel("Bulan (1-12)")
axes[1].set_ylabel("Rata-rata Penyewaan")
axes[1].grid(True)

# Plot 3: Rata-rata Penyewaan Sepeda per Jam
sns.lineplot(x=hour_avg['hr'], y=hour_avg['average_cnt'], marker='o', ax=axes[2])
axes[2].set_title("Rata-rata Penyewaan Sepeda per Jam")
axes[2].set_xlabel("Jam (0-23)")
axes[2].set_ylabel("Rata-rata Penyewaan")
axes[2].grid(True)

# Plot 4: Rata-rata Penyewaan Sepeda berdasarkan Musim
sns.lineplot(x=season_avg['season'], y=season_avg['average_cnt'], marker='o', ax=axes[3])
axes[3].set_title("Rata-rata Penyewaan Sepeda berdasarkan Musim")
axes[3].set_xlabel("Musim")
axes[3].set_ylabel("Rata-rata Penyewaan")
axes[3].set_xticks([1, 2, 3, 4])
axes[3].set_xticklabels(['Spring', 'Summer', 'Fall', 'Winter'], rotation=45)
axes[3].grid(True)

# Plot 5: Rata-rata Penyewaan Sepeda berdasarkan Cuaca
sns.lineplot(x=weather_avg['weathersit'], y=weather_avg['average_cnt'], marker='o', ax=axes[4])
axes[4].set_title("Rata-rata Penyewaan Sepeda berdasarkan Cuaca")
axes[4].set_xlabel("Cuaca")
axes[4].set_ylabel("Rata-rata Penyewaan")
axes[4].set_xticks([1, 2, 3])
axes[4].set_xticklabels(['Cerah', 'Berawan', 'Hujan Ringan'], rotation=45)
axes[4].grid(True)

plt.tight_layout()
st.pyplot(fig)

# Visualisasi ini seharusnya tidak kena filter, melainkan hanya untuk melihat kondisi yang paling sibuk
# Ada salah call kemarin, sudah dibenarkan

# Membuat Kategori jam/waktu
def kategori_jam_baru(jam):
    if 0 <= jam <= 5:
        return "Malam"
    elif 6 <= jam <= 11:
        return "Pagi"
    elif 12 <= jam <= 17:
        return "Siang"
    else:
        return "Sore"

theData_df['waktu'] = theData_df['hr'].apply(kategori_jam_baru)

# Ubah variabel hari dari angka ke char
def day(weekday):
    daftar_hari = ['Minggu', 'Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu']
    if 0 <= weekday <= 6:
        return daftar_hari[weekday]
    else:
        return None

theData_df['hari'] = theData_df['weekday'].apply(day)

# Ubah variabel season dari angka ke char
def seasons_cat(season):
    daftar_musim = ['Semi', 'Panas', 'Gugur', 'Salju']
    if 1 <= season <= 4:
        return daftar_musim[season - 1]  # Mengurangi 1 dari indeks musim
    else:
        return None

theData_df['musim'] = theData_df['season'].apply(seasons_cat)

# Ubah variabel holiday dari angka ke char
def hol(holiday):
    if holiday == 0:
        return 'Tidak'
    else:
        return 'Ya'

theData_df['liburan'] = theData_df['holiday'].apply(hol)

# Pivot tables
pivot_kategori_waktu_hari = theData_df.pivot_table(values='cnt', index='waktu', columns='hari', aggfunc='mean')
pivot_kategori_musim_liburan = theData_df.pivot_table(values='cnt', index='liburan', columns='musim', aggfunc='mean')

# Membuat kolom kiri dan kanan
col1, col2 = st.columns(2)

# Heatmap 1: Kategori jam baru dan hari (di kolom kiri)
with col1:
    st.subheader("Rata-rata Penyewaan Sepeda per Waktu dan Hari")
    fig1, ax1 = plt.subplots(figsize=(8, 6))  # Ukuran plot disesuaikan
    urutan = ['Minggu', 'Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu']
    sns.heatmap(pivot_kategori_waktu_hari[urutan], cmap='YlGnBu', annot=True, fmt=".1f", ax=ax1)
    ax1.set_xlabel("Hari")
    ax1.set_ylabel("Waktu")
    st.pyplot(fig1)

# Heatmap 2: Kategori jam baru dan musim (di kolom kanan)
with col2:
    st.subheader("Rata-rata Penyewaan Sepeda per Kategori Jam Baru dan Musim")
    fig2, ax2 = plt.subplots(figsize=(8, 6))  # Ukuran plot disesuaikan
    runtutan = ['Semi', 'Panas', 'Gugur', 'Salju']
    sns.heatmap(pivot_kategori_musim_liburan[runtutan], cmap='YlGnBu', annot=True, fmt=".1f", ax=ax2)
    ax2.set_xlabel("Musim (1=Spring, 4=Winter)")
    ax2.set_ylabel("Kategori Jam")
    st.pyplot(fig2)

    st.caption('made by Loveta Ramyhaidar Winaryo - MC010D5Y1099')
