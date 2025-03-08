import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Judul Dashboard
st.title("Analisis Penggunaan Sepeda (Bike Sharing)")
st.write("Dashboard ini menampilkan analisis penggunaan sepeda berdasarkan tren musiman, kondisi cuaca, dan pola penggunaan pada hari weekend.")

day_df = pd.read_csv('dashboard/main_data.csv') 
day_df['dteday'] = pd.to_datetime(day_df['dteday'])
day_df['month'] = day_df['dteday'].dt.month

# Sidebar Filter Rentang Bulan
st.sidebar.header("Filter Data")
month_options = sorted(day_df['month'].unique())
start_month, end_month = st.sidebar.select_slider("Pilih Rentang Bulan:", options=month_options, value=(month_options[0], month_options[-1]))
filtered_df = day_df[(day_df['month'] >= start_month) & (day_df['month'] <= end_month)]
# Fungsi untuk visualisasi tren penggunaan sepeda per bulan
def plot_monthly_trend(day_df, start_month, end_month):
    
    monthly_trend = filtered_df.groupby('month')['cnt'].mean()
    
    plt.figure(figsize=(10, 6))
    sns.lineplot(x=monthly_trend.index, y=monthly_trend.values, marker='o')
    plt.title('Tren Penggunaan Sepeda per Bulan')
    plt.xlabel('Bulan')
    plt.ylabel('Rata-rata Pengguna Sepeda')
    st.pyplot(plt)

# Tampilkan Visualisasi
st.subheader("Visualisasi Tren Penggunaan Sepeda")
plot_monthly_trend(day_df, start_month, end_month)
st.markdown("""
Dari pertanyaan pertama yaitu : Bagaimana pola jumlah pengguna sepeda per hari dalam setahun terakhir? (Tren musiman)

Dapat disimpulkan bahwa penggunaan sepeda sangat dipengaruhi oleh musim, dengan puncak penggunaan pada bulan-bulan dengan cuaca hangat.
""")



# Sidebar Filter Musim
st.sidebar.header("Filter Musim")
selected_season = st.sidebar.selectbox("Pilih Musim:", options=day_df['season'].unique())

# Fungsi untuk visualisasi distribusi pengguna sepeda berdasarkan kondisi cuaca
def plot_weather_distribution(day_df, selected_season):
    
        # Definisikan season dalam bentuk dictionary
    season_mapping = {
        1: "Musim Salju",
        2: "Musim Semi",
        3: "Musim Panas",
        4: "Musim Gugur"
    }

    # Tambahkan kolom baru dengan label musim
    day_df["season_label"] = day_df["season"].map(season_mapping)

    # Sidebar Filter Musim
    st.sidebar.header("Filter Data")
    selected_season = st.sidebar.selectbox("Pilih Musim:", options=season_mapping.values())

    # Konversi pilihan musim kembali ke angka
    selected_season_num = {v: k for k, v in season_mapping.items()}[selected_season]

    # Filter Data Berdasarkan Musim yang Dipilih
    filtered_df = day_df[day_df['season'] == selected_season_num]

    
    weather_distribution = filtered_df.groupby('weathersit')['cnt'].mean()
    
    plt.figure(figsize=(10, 6))
    sns.barplot(x=weather_distribution.index, y=weather_distribution.values)
    plt.title('Distribusi Pengguna Sepeda Berdasarkan Kondisi Cuaca')
    plt.xlabel('Kondisi Cuaca')
    plt.ylabel('Rata-rata Pengguna Sepeda')
    st.pyplot(plt)

# Tampilkan Visualisasi
st.subheader("Distribusi Pengguna Sepeda Berdasarkan Kondisi Cuaca")
plot_weather_distribution(day_df, selected_season)
st.markdown("""
Dari pertanyaan kedua yaitu : Bagaimana distribusi jumlah pengguna sepeda berdasarkan kondisi cuaca yang berbeda?

Dapat disimpulkan bahwa kondisi cuaca cerah mendorong penggunaan sepeda yang lebih tinggi, sementara cuaca buruk menjadi penghalang.
""")

# Fungsi untuk visualisasi penggunaan sepeda pada weekday dan weekend

def plot_weekday_weekend_usage(filtered_df):
    latest_date = filtered_df['dteday'].max()
    six_months_ago = latest_date - pd.DateOffset(months=6)
    df_last_six_months = filtered_df[filtered_df['dteday'] >= six_months_ago]
    df_last_six_months['is_weekend'] = df_last_six_months['weekday'].apply(lambda x: 1 if x in [5, 6] else 0)
    weekend_usage = df_last_six_months[df_last_six_months['is_weekend'] == 1]['cnt']
    weekday_usage = df_last_six_months[df_last_six_months['is_weekend'] == 0]['cnt']
    
    # Visualisasi 1: Perbandingan penggunaan weekend vs weekday
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(x=['Weekend', 'Weekday'], y=[weekend_usage.mean(), weekday_usage.mean()], ax=ax)
    ax.set_title('Perbandingan Rata-rata Penggunaan Sepeda: Weekend vs Weekday')
    ax.set_ylabel('Rata-rata Pengguna Sepeda')
    st.pyplot(fig)
    
    # Visualisasi 2: Tren penggunaan sepeda pada weekend
    fig, ax = plt.subplots(figsize=(10, 6))
    df_weekend = df_last_six_months[df_last_six_months['is_weekend'] == 1]
    sns.lineplot(x=df_weekend['dteday'], y=df_weekend['cnt'], ax=ax)
    ax.set_title('Tren Penggunaan Sepeda pada Weekend (Enam Bulan Terakhir)')
    ax.set_xlabel('Tanggal')
    ax.set_ylabel('Jumlah Pengguna Sepeda')
    st.pyplot(fig)

# Tampilkan Visualisasi
st.subheader("Visualisasi Penggunaan Sepeda pada Weekday dan Weekend")
plot_weekday_weekend_usage(filtered_df)
st.markdown("""
Dari pertanyaan ketiga yaitu : Bagaimana pola penggunaan sepeda pada akhir pekan dalam enam bulan terakhir?

Dapat disimpulkan bahwa penggunaan sepeda pada hari weekend lebih tinggi dibandingkan hari weekday, terutama pada bulan-bulan dengan cuaca yang baik.
""")

st.markdown("© 2025 Alivia Vinca Kustaryono. All Rights Reserved.")

