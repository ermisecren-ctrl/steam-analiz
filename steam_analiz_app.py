import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Sayfa Ayarları
st.set_page_config(page_title="Steam Veri Analizi", layout="wide")
st.title("🎮 Steam Market Analiz Uygulaması")

# 2. Veri Yükleme (Otomatik Okuma Sistemi)
# Bu bölüm, uygulamanın dosya beklemeden doğrudan çalışmasını sağlar.
dosya_adi = 'steam_kucuk.csv'

try:
    df = pd.read_csv(dosya_adi)
    st.sidebar.success(f"✅ {dosya_adi} başarıyla yüklendi.")
except FileNotFoundError:
    st.sidebar.error(f"❌ Hata: '{dosya_adi}' dosyası bulunamadı!")
    st.warning("Lütfen GitHub deponuzda 'steam_kucuk.csv' dosyasının olduğundan emin olun.")
    st.stop() # Dosya yoksa uygulamayı burada durdurur.

# 3. Sol Menü (Sidebar) Seçenekleri
st.sidebar.header("Analiz Kontrol Paneli")
secim = st.sidebar.selectbox("Görmek istediğiniz analizi seçin:", 
                             ["Ana Sayfa", "Oyun Sayısı (Nicelik)", "Puan Durumu (Nitelik)"])

# 4. Analiz Mantığı
if secim == "Ana Sayfa":
    st.subheader("📊 Veri Seti Genel Görünümü")
    st.write(f"Sistemde şu anda toplam **{len(df)}** adet seçilmiş oyun verisi analiz ediliyor.")
    st.dataframe(df.head(15)) # İlk 15 satırı gösterir
    st.info("Bu veri seti, 400 MB'lık ana veri setinden istatistiksel örnekleme yöntemiyle türetilmiştir.")

elif secim == "Oyun Sayısı (Nicelik)":
    st.subheader("📈 En Çok Üretilen 10 Oyun Türü")
    # Veri setindeki tür bilgisini ayıklıyoruz
    genre_col = 'Genres' if 'Genres' in df.columns else 'genres'
    veriler = df[genre_col].str.split(';').str[0].value_counts().head(10)
    
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(x=veriler.values, y=veriler.index, palette="magma", ax=ax)
    plt.xlabel("Oyun Sayısı")
    plt.ylabel("Türler")
    st.pyplot(fig)

elif secim == "Puan Durumu (Nitelik)":
    st.subheader("⭐ Türlere Göre Kullanıcı Memnuniyeti Skoru")
    # Puanlama sütunlarını kontrol ediyoruz
    pos = 'Positive' if 'Positive' in df.columns else 'positive_ratings'
    neg = 'Negative' if 'Negative' in df.columns else 'negative_ratings'
    genre_col = 'Genres' if 'Genres' in df.columns else 'genres'
    
    # Basit bir memnuniyet skoru hesaplıyoruz
    df['skor'] = df[pos] / (df[pos] + df[neg])
    df['ana_tur'] = df[genre_col].str.split(';').str[0]
    
    en_populer = df['ana_tur'].value_counts().head(10).index
    filtreli_df = df[df['ana_tur'].isin(en_populer)]
    
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.boxplot(x='skor', y='ana_tur', data=filtreli_df, palette="coolwarm", ax=ax)
    plt.xlabel("Memnuniyet Oranı (0-1)")
    plt.ylabel("Oyun Türü")
    st.pyplot(fig)