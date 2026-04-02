import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# 1. Sayfa Ayarları
st.set_page_config(page_title="Steam Veri Analizi", layout="wide")
st.title("🎮 Steam Market Analiz Uygulaması")

# 2. Veri Yükleme ve Akıllı Sütun Tespiti
dosya_adi = 'steam_kucuk.csv'

if os.path.exists(dosya_adi):
    try:
        # Veriyi yükle
        df = pd.read_csv(dosya_adi, on_bad_lines='skip')
        
        # SÜTUN TESPİT SİSTEMİ (Hata almamak için en kritik bölge)
        # Sütun isimlerini küçük harfe çevirip içinde anahtar kelime arıyoruz
        genre_col = [c for c in df.columns if 'genre' in c.lower()][0]
        pos_col = [c for c in df.columns if 'pos' in c.lower()][0]
        neg_col = [c for c in df.columns if 'neg' in c.lower()][0]
        
        st.sidebar.success(f"✅ Veri seti başarıyla bağlandı.")
        
    except (IndexError, Exception) as e:
        st.error(f"Kritik Hata: Veri setinde gerekli sütunlar bulunamadı veya dosya bozuk. Detay: {e}")
        st.stop()
else:
    st.sidebar.error(f"❌ Hata: '{dosya_adi}' bulunamadı!")
    st.info("Sistemin gördüğü dosyalar:")
    st.write(os.listdir())
    st.stop()

# 3. Sol Menü (Sidebar) Seçenekleri
st.sidebar.header("Analiz Kontrol Paneli")
secim = st.sidebar.selectbox("Görmek istediğiniz analizi seçin:", 
                             ["Ana Sayfa", "Oyun Sayısı (Nicelik)", "Puan Durumu (Nitelik)"])

# 4. Analiz Mantığı
if secim == "Ana Sayfa":
    st.subheader("📊 Veri Seti Genel Görünümü")
    st.write(f"Sistemde şu anda toplam **{len(df)}** adet oyun verisi analiz ediliyor.")
    st.dataframe(df.head(15))
    st.info("Bu çalışma, Yeni Medya bağlamında dijital oyun pazarı verilerinin görselleştirilmesini amaçlar.")

elif secim == "Oyun Sayısı (Nicelik)":
    st.subheader("📈 En Çok Üretilen 10 Oyun Türü")
    # Burada sabit isim yerine genre_col değişkenini kullanıyoruz (Hata buradaydı)
    veriler = df[genre_col].str.split(';').str[0].value_counts().head(10)
    
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(x=veriler.values, y=veriler.index, palette="magma", ax=ax)
    plt.xlabel("Oyun Sayısı")
    plt.ylabel("Türler")
    st.pyplot(fig)

elif secim == "Puan Durumu (Nitelik)":
    st.subheader("⭐ Türlere Göre Kullanıcı Memnuniyeti Skoru")
    
    # Skor hesaplama (Değişkenleri dinamik kullanıyoruz, KeyError riskini bitirdik)
    df['skor'] = df[pos_col] / (df[pos_col] + df[neg_col])
    df['ana_tur'] = df[genre_col].str.split(';').str[0]
    
    en_populer = df['ana_tur'].value_counts().head(10).index
    filtreli_df = df[df['ana_tur'].isin(en_populer)]
    
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.boxplot(x='skor', y='ana_tur', data=filtreli_df, palette="coolwarm", ax=ax)
    plt.xlabel("Memnuniyet Oranı (0-1)")
    plt.ylabel("Oyun Türü")
    st.pyplot(fig)
