import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Sayfa Ayarları
st.set_page_config(page_title="Steam Veri Analizi", layout="wide")
st.title("🎮 Steam Market Analiz Uygulaması")

# Sol Menü (Sidebar)
st.sidebar.header("Veri Girişi")
yuklenen_dosya = st.sidebar.file_uploader("Steam CSV dosyasını (games) buraya yükleyin", type=["csv"])

if yuklenen_dosya is not None:
    df = pd.read_csv(yuklenen_dosya)
    st.sidebar.success("Veri yüklendi!")
    
    # Analiz Seçenekleri
    secim = st.sidebar.selectbox("Görmek istediğiniz analizi seçin:", 
                                 ["Ana Sayfa", "Oyun Sayısı (Nicelik)", "Puan Durumu (Nitelik)"])
    
    if secim == "Ana Sayfa":
        st.subheader("Veri Seti Önizlemesi")
        st.dataframe(df.head(10)) 
        st.write(f"Sistemde toplam **{len(df)}** adet oyun verisi analiz ediliyor.")

    elif secim == "Oyun Sayısı (Nicelik)":
        st.subheader("En Çok Üretilen 10 Oyun Türü")
        genre_col = 'Genres' if 'Genres' in df.columns else 'genres'
        veriler = df[genre_col].str.split(';').str[0].value_counts().head(10)
        
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.barplot(x=veriler.values, y=veriler.index, palette="magma", ax=ax)
        st.pyplot(fig)

    elif secim == "Puan Durumu (Nitelik)":
        st.subheader("Türlere Göre Kullanıcı Memnuniyeti")
        pos = 'Positive' if 'Positive' in df.columns else 'positive_ratings'
        neg = 'Negative' if 'Negative' in df.columns else 'negative_ratings'
        genre_col = 'Genres' if 'Genres' in df.columns else 'genres'
        
        df['skor'] = df[pos] / (df[pos] + df[neg])
        df['ana_tur'] = df[genre_col].str.split(';').str[0]
        
        en_populer = df['ana_tur'].value_counts().head(10).index
        filtreli_df = df[df['ana_tur'].isin(en_populer)]
        
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.boxplot(x='skor', y='ana_tur', data=filtreli_df, palette="coolwarm", ax=ax)
        st.pyplot(fig)
else:
    st.warning("Lütfen sol menüden 'games' adlı CSV dosyasını yükleyerek analizi başlatın.")