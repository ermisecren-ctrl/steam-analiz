import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# 1. Sayfa Ayarları
st.set_page_config(page_title="Steam Veri Analizi", layout="wide")
st.title("🎮 Steam Market Analiz Uygulaması")

# 2. Veri Yükleme
dosya_adi = 'steam_kucuk.csv'

if os.path.exists(dosya_adi):
    df = pd.read_csv(dosya_adi, on_bad_lines='skip')
    
    # MEVCUT SÜTUNLARI TESPİT ET (Hata Ayıklama Modu)
    mevcut_sutunlar = [str(c).lower() for c in df.columns]
    
    # Sütunları güvenli bir şekilde eşleştirelim
    genre_col = next((c for c in df.columns if 'genre' in str(c).lower()), None)
    pos_col = next((c for c in df.columns if 'pos' in str(c).lower()), None)
    neg_col = next((c for c in df.columns if 'neg' in str(c).lower()), None)

    # Eğer sütunlar bulunamazsa, manuel olarak ilk uygun sütunları ata (Çökmemesi için)
    if not genre_col: genre_col = df.columns[1] if len(df.columns) > 1 else df.columns[0]
    if not pos_col: pos_col = df.columns[2] if len(df.columns) > 2 else df.columns[0]
    if not neg_col: neg_col = df.columns[3] if len(df.columns) > 3 else df.columns[0]

    st.sidebar.success("✅ Veri seti yüklendi.")
else:
    st.error(f"❌ {dosya_adi} bulunamadı!")
    st.stop()

# 3. Menü
secim = st.sidebar.selectbox("Analiz Seçin:", ["Ana Sayfa", "Oyun Sayısı", "Puan Durumu"])

# 4. Analizler
if secim == "Ana Sayfa":
    st.subheader("📊 Veri Seti Önizleme")
    st.write("Sistemdeki sütunlar:", list(df.columns)) # Hangi sütunların olduğunu görmeniz için
    st.dataframe(df.head(10))

elif secim == "Oyun Sayısı":
    st.subheader("📈 En Çok Üretilen Türler")
    try:
        veriler = df[genre_col].astype(str).str.split(';').str[0].value_counts().head(10)
        fig, ax = plt.subplots()
        sns.barplot(x=veriler.values, y=veriler.index, ax=ax, palette="viridis")
        st.pyplot(fig)
    except Exception as e:
        st.error(f"Grafik çizilemedi. Sütun hatası olabilir: {e}")

elif secim == "Puan Durumu":
    st.subheader("⭐ Memnuniyet Analizi")
    try:
        # Sayısal dönüşüm zorlaması
        df[pos_col] = pd.to_numeric(df[pos_col], errors='coerce').fillna(0)
        df[neg_col] = pd.to_numeric(df[neg_col], errors='coerce').fillna(0)
        
        df['skor'] = df[pos_col] / (df[pos_col] + df[neg_col] + 1e-5)
        df['ana_tur'] = df[genre_col].astype(str).str.split(';').str[0]
        
        tur_ozet = df.groupby('ana_tur')['skor'].mean().sort_values(ascending=False).head(10)
        fig, ax = plt.subplots()
        tur_ozet.plot(kind='barh', ax=ax, color='skyblue')
        st.pyplot(fig)
    except Exception as e:
        st.error(f"Puan analizi yapılamadı: {e}")
