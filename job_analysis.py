import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import re
import numpy as np
import os

st.set_page_config(page_title="İş Analizi", layout="wide")
st.title("📊 İş Elanları Analizi")
st.write("Salam! Bu sizin iş elanları analiz app-inizdir.")

# Fayl yolu təyin et
FILE_PATH = "main_data.csv"  # və ya "job_data.xlsx"

def clean_city_name(city_text):
    """Şəhər adını təmizlə və standartlaşdır, Bakı rayonlarını ayrıca təsnif et"""
    if pd.isna(city_text):
        return "Digər"
    
    city_text = str(city_text).lower().strip()
    
    # Bakı rayonları mapping
    baku_district_mapping = {
        'nəsimi': 'Bakı (Nəsimi)',
        'nəsimi rayonu': 'Bakı (Nəsimi)',
        'nesimi': 'Bakı (Nəsimi)',
        'xətai': 'Bakı (Xətai)',
        'xətai rayonu': 'Bakı (Xətai)',
        'xetai': 'Bakı (Xətai)',
        'yasamal': 'Bakı (Yasamal)',
        'yasamal rayonu': 'Bakı (Yasamal)',
        'nərimanov': 'Bakı (Nərimanov)',
        'nərimanov rayonu': 'Bakı (Nərimanov)',
        'nerimanov': 'Bakı (Nərimanov)',
        'nermanov': 'Bakı (Nərimanov)',
        'səbail': 'Bakı (Səbail)',
        'səbail rayonu': 'Bakı (Səbail)',
        'sebail': 'Bakı (Səbail)',
        'nizami': 'Bakı (Nizami)',
        'nizami rayonu': 'Bakı (Nizami)',
        'sabunçu': 'Bakı (Sabunçu)',
        'sabunçu rayonu': 'Bakı (Sabunçu)',
        'sabuncu': 'Bakı (Sabunçu)',
        'qaradağ': 'Bakı (Qaradağ)',
        'qaradağ rayonu': 'Bakı (Qaradağ)',
        'garadag': 'Bakı (Qaradağ)',
        'xəzər': 'Bakı (Xəzər)',
        'xəzər rayonu': 'Bakı (Xəzər)',
        'xezer': 'Bakı (Xəzər)',
        'binəqədi': 'Bakı (Binəqədi)',
        'binəqədi rayonu': 'Bakı (Binəqədi)',
        'bineqedi': 'Bakı (Binəqədi)',
        'suraxanı': 'Bakı (Suraxanı)',
        'suraxanı rayonu': 'Bakı (Suraxanı)',
        'suraxani': 'Bakı (Suraxanı)',
    }
    
    # Əsas şəhər mapping
    city_mapping = {
        'bakı': 'Bakı (Digər)',
        'baki': 'Bakı (Digər)',
        'baku': 'Bakı (Digər)',
        'ganca': 'Gəncə',
        'gence': 'Gəncə', 
        'sumqayit': 'Sumqayıt',
        'sumgait': 'Sumqayıt',
        'mingəçevir': 'Mingəçevir',
        'mingecevir': 'Mingəçevir',
        'şəki': 'Şəki',
        'sheki': 'Şəki',
        'yevlax': 'Yevlax',
        'evlax': 'Yevlax',
        'naxçıvan': 'Naxçıvan',
        'naxcivan': 'Naxçıvan',
        'şirvan': 'Şirvan',
        'shirvan': 'Şirvan',
        'xankəndi': 'Xankəndi',
        'xankendi': 'Xankəndi',
        'lənkəran': 'Lənkəran',
        'lenkeran': 'Lənkəran',
        'azerbaijan': 'Bakı (Digər)',
        'azərbaycan': 'Bakı (Digər)',
        'abşeron': 'Abşeron',
        'absheron': 'Abşeron',
        'xırdalan': 'Abşeron',
        'xirdalan': 'Abşeron',
    }
    
    # Əvvəlcə Bakı rayonlarını yoxla
    for district_pattern, district_name in baku_district_mapping.items():
        if district_pattern in city_text:
            return district_name
    
    # Sonra digər şəhərləri yoxla
    for city_pattern, city_name in city_mapping.items():
        if city_pattern in city_text:
            return city_name
    
    # Ümumi Bakı axtarışı
    if 'bakı' in city_text or 'baki' in city_text or 'baku' in city_text:
        return 'Bakı (Digər)'
    
    return "Digər Şəhərlər"


def analyze_company_jobs(df):
    """Şirkətlərin iş elanı sayı analizi"""
    st.subheader("🏢 Şirkətlər üzrə İş Elanları")
    
    if 'company_b' not in df.columns:
        st.warning("⚠️ company_b sütunu tapılmadı")
        return
    
    company_stats = df['company_b'].value_counts().reset_index()
    company_stats.columns = ['Şirkət', 'İş Elanı Sayı']
    top_companies = company_stats.head(20)
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.bar(top_companies, 
                    x='İş Elanı Sayı', 
                    y='Şirkət',
                    orientation='h',
                    title='Ən Çox İş Elanı Paylaşan İlk 20 Şirkət',
                    color='İş Elanı Sayı',
                    color_continuous_scale='viridis')
        fig.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        top_10 = company_stats.head(10)
        fig_pie = px.pie(top_10, 
                        values='İş Elanı Sayı', 
                        names='Şirkət',
                        title='İş Elanlarının Şirkətlər üzrə Paylanması (Top 10)')
        st.plotly_chart(fig_pie, use_container_width=True)
    
    st.write("**Şirkət Statistikası:**")
    col3, col4 = st.columns(2)
    
    with col3:
        st.metric("Ümumi Şirkət Sayı", len(company_stats))
    
    with col4:
        avg_jobs_per_company = company_stats['İş Elanı Sayı'].mean()
        st.metric("Şirkət başına orta iş sayı", f"{avg_jobs_per_company:.1f}")

def analyze_job_categories(df):
    """İş kateqoriyaları üzrə analiz"""
    st.subheader("📊 İş Kateqoriyaları üzrə Statistikalar")
    
    if 'job_category_b' not in df.columns:
        st.warning("⚠️ job_category_b sütunu tapılmadı")
        return
    
    job_stats = df['job_category_b'].value_counts()
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.pie(values=job_stats.values, names=job_stats.index,
                    title='İş Kateqoriyalarının Paylanması')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig_bar = px.bar(x=job_stats.values, y=job_stats.index, 
                        orientation='h',
                        title='İş Kateqoriyaları (Say)',
                        labels={'x': 'İş sayı', 'y': 'Kateqoriya'})
        st.plotly_chart(fig_bar, use_container_width=True)

def analyze_baku_districts(df):
    """Bakı rayonları üzrə analiz"""
    st.subheader("🏙️ Bakı Rayonları üzrə Statistikalar")
    
    if 'temizlenmis_seher' not in df.columns:
        st.warning("⚠️ Təmizlənmiş şəhər sütunu tapılmadı")
        return
    
    baku_data = df[df['temizlenmis_seher'].str.startswith('Bakı', na=False)]
    
    if baku_data.empty:
        st.warning("Bakı məlumatı tapılmadı")
        return
    
    district_stats = baku_data['temizlenmis_seher'].value_counts()
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.bar(x=district_stats.values, y=district_stats.index,
                    orientation='h',
                    title='Bakı Rayonları üzrə İş Elanları',
                    labels={'x': 'İş sayı', 'y': 'Rayon'},
                    color=district_stats.values,
                    color_continuous_scale='blues')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig_pie = px.pie(values=district_stats.values, names=district_stats.index,
                        title='Bakı Rayonlarının Paylanması')
        st.plotly_chart(fig_pie, use_container_width=True)

def analyze_salary_by_category(df):
    """Kateqoriyalar üzrə ortalama maaş analizi"""
    st.subheader("💰 Kateqoriyalar üzrə Orta Maaş")
    
    if 'job_category_b' not in df.columns or 'salary_clean' not in df.columns:
        st.warning("⚠️ Maaş analizi üçün lazımlı sütunlar tapılmadı")
        return
    
    salary_data = df[df['salary_clean'].notna()]
    
    if salary_data.empty:
        st.warning("Maaş məlumatı tapılmadı")
        return
    
    avg_salary_by_category = salary_data.groupby('job_category_b')['salary_clean'].agg(['mean', 'count']).round(2)
    avg_salary_by_category = avg_salary_by_category[avg_salary_by_category['count'] >= 3]
    avg_salary_by_category = avg_salary_by_category.sort_values('mean', ascending=False)
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.bar(avg_salary_by_category, x=avg_salary_by_category.index, y='mean',
                    title='Kateqoriyalar üzrə Orta Maaş',
                    labels={'mean': 'Orta Maaş', 'job_category_b': 'Kateqoriya'})
        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.write("**Orta Maaş Statistikası:**")
        avg_salary_by_category_display = avg_salary_by_category.rename(
            columns={'mean': 'Orta Maaş', 'count': 'Nümunə Sayı'}
        )
        st.dataframe(avg_salary_by_category_display, use_container_width=True)

def analyze_salary_by_experience(df):
    """Təcrübəyə görə maaş analizi"""
    st.subheader("📈 Təcrübəyə görə Maaş Artımı")
    
    if 'experience' not in df.columns or 'salary_clean' not in df.columns:
        st.warning("⚠️ Təcrübə analizi üçün lazımlı sütunlar tapılmadı")
        return
    
    salary_exp_data = df[df['salary_clean'].notna() & df['experience'].notna()]
    
    if salary_exp_data.empty:
        st.warning("Təcrübə və maaş məlumatı tapılmadı")
        return
    
    avg_salary_by_exp = salary_exp_data.groupby('experience')['salary_clean'].agg(['mean', 'count']).round(2)
    avg_salary_by_exp = avg_salary_by_exp[avg_salary_by_exp['count'] >= 2]
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.line(avg_salary_by_exp, x=avg_salary_by_exp.index, y='mean',
                     markers=True, title='Təcrübəyə görə Orta Maaş')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.write("**Təcrübə Statistikası:**")
        avg_salary_by_exp_display = avg_salary_by_exp.rename(
            columns={'mean': 'Orta Maaş', 'count': 'Nümunə Sayı'}
        )
        st.dataframe(avg_salary_by_exp_display, use_container_width=True)
def analyze_gender_salary(df):
    """Cinsiyyətə görə maaş analizi"""
    st.subheader("⚧ Cinsiyyətə görə Maaş Fərqləri")
    
    if 'gender' not in df.columns or 'salary_clean' not in df.columns:
        st.warning("⚠️ Cinsiyyət analizi üçün lazımlı sütunlar tapılmadı")
        return
    
    gender_salary_data = df[df['salary_clean'].notna() & df['gender'].notna()]
    
    if gender_salary_data.empty:
        st.warning("Cinsiyyət və maaş məlumatı tapılmadı")
        return
    
    avg_salary_by_gender = gender_salary_data.groupby('gender')['salary_clean'].agg(['mean', 'count', 'std']).round(2)
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.bar(avg_salary_by_gender, x=avg_salary_by_gender.index, y='mean',
                    title='Cinsiyyətə görə Orta Maaş',
                    color=avg_salary_by_gender.index)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.write("**Cinsiyyət Statistikası:**")
        avg_salary_by_gender_display = avg_salary_by_gender.rename(
            columns={'mean': 'Orta Maaş', 'count': 'Nümunə Sayı', 'std': 'Standart Sapma'}
        )
        st.dataframe(avg_salary_by_gender_display, use_container_width=True)
        
        # Maaş fərqi hesabla
        if len(avg_salary_by_gender) >= 2:
            genders = avg_salary_by_gender.index.tolist()
            st.info(f"**Maaş fərqi:** {genders[0]}: {avg_salary_by_gender.iloc[0]['mean']} AZN vs {genders[1]}: {avg_salary_by_gender.iloc[1]['mean']} AZN")

def analyze_monthly_trends(df):
    """Aylıq trend analizi"""
    st.subheader("📅 Aylıq İş Elanları Trendi")
    
    if 'post_month_b' not in df.columns:
        st.warning("⚠️ Ay sütunu tapılmadı")
        return
    
    df_clean = df.copy()
    df_clean['post_month_b'] = df_clean['post_month_b'].astype(str)
    
    def filter_dates(date_str):
        try:
            if any(year in date_str for year in ['2020', '2021', '2022', '2023', '2024', '2025']):
                return date_str
            return None
        except:
            return None
    
    df_clean['filtered_month'] = df_clean['post_month_b'].apply(filter_dates)
    df_filtered = df_clean[df_clean['filtered_month'].notna()]
    
    if df_filtered.empty:
        st.warning("2020-2025 arası məlumat tapılmadı")
        return
    
    ay_stats = df_filtered['filtered_month'].value_counts().reset_index()
    ay_stats.columns = ['Ay', 'İş Sayı']
    
    def sort_months(month_year):
        try:
            year = int(month_year.split()[0])
            month_name = month_year.split()[1]
            
            month_order = {'Yanvar': 1, 'Fevral': 2, 'Mart': 3, 'Aprel': 4, 
                          'May': 5, 'İyun': 6, 'İyul': 7, 'Avqust': 8, 
                          'Sentyabr': 9, 'Oktyabr': 10, 'Noyabr': 11, 'Dekabr': 12}
            
            return year * 100 + month_order.get(month_name, 999)
        except:
            return 999999
    
    ay_stats['sort_key'] = ay_stats['Ay'].apply(sort_months)
    ay_stats = ay_stats.sort_values('sort_key').drop('sort_key', axis=1)
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_bar = px.bar(ay_stats, x='Ay', y='İş Sayı', 
                        title='Aylar üzrə iş elanları sayı (2025)',
                        color='İş Sayı',
                        color_continuous_scale='blues')
        fig_bar.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig_bar, use_container_width=True)
    
    with col2:
        fig_line = px.line(ay_stats, x='Ay', y='İş Sayı',
                          title='İş elanlarının aylıq dəyişimi',
                          markers=True)
        fig_line.update_traces(line=dict(width=3))
        fig_line.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig_line, use_container_width=True)

def analyze_skills(df):
    """Bacarıq analizi"""
    st.subheader("🛠️ Tələb Olunan Bacarıqlar")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if 'tech_skills_clean' in df.columns:
            st.write("**Ən çox tələb olunan 15 Texniki Bacarıq:**")
            
            all_tech_skills = []
            for skills in df['tech_skills_clean'].dropna():
                if isinstance(skills, str):
                    skill_list = [skill.strip() for skill in skills.split(',')]
                    all_tech_skills.extend(skill_list)
            
            tech_skills_count = pd.Series(all_tech_skills).value_counts().head(15)
            
            if not tech_skills_count.empty:
                fig = px.bar(x=tech_skills_count.values, y=tech_skills_count.index,
                            orientation='h', title='Top 15 Texniki Bacarıq')
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.write("Texniki bacarıq məlumatı tapılmadı")
    
    with col2:
        if 'soft_skills_clean' in df.columns:
            st.write("**Ən çox tələb olunan 10 Soft Bacarıq:**")
            
            all_soft_skills = []
            for skills in df['soft_skills_clean'].dropna():
                if isinstance(skills, str):
                    skill_list = [skill.strip() for skill in skills.split(',')]
                    all_soft_skills.extend(skill_list)
            
            soft_skills_count = pd.Series(all_soft_skills).value_counts().head(10)
            
            if not soft_skills_count.empty:
                fig = px.bar(x=soft_skills_count.values, y=soft_skills_count.index,
                            orientation='h', title='Top 10 Soft Bacarıq',
                            color=soft_skills_count.values)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.write("Soft bacarıq məlumatı tapılmadı")

# ƏSAS KOD
def main():
    # Faylın olub olmadığını yoxla
    if os.path.exists(FILE_PATH):
        try:
            if FILE_PATH.endswith('.csv'):
                df = pd.read_csv(FILE_PATH)
            else:
                df = pd.read_excel(FILE_PATH)
            
            st.success(f"✅ Fayl avtomatik yükləndi! {len(df)} sətir, {len(df.columns)} sütun")
            
            # Data önizləmə
            with st.expander("📋 Data Önizləmə"):
                st.dataframe(df.head(10), use_container_width=True)
                st.write(f"**Ümumi sütunlar:** {list(df.columns)}")
            
            # Şəhər sütununu təmizlə
            if 'location_b' in df.columns:
                df['temizlenmis_seher'] = df['location_b'].apply(clean_city_name)
            
            # ANALİZLƏR
            analyze_company_jobs(df)
            analyze_job_categories(df)
            analyze_baku_districts(df)
            analyze_salary_by_category(df)
            analyze_salary_by_experience(df)
            analyze_gender_salary(df)
            analyze_monthly_trends(df)
            analyze_skills(df)
            
            # ÜMUMİ STATİSTİK XÜLASƏ
            st.subheader("📈 Ümumi Statistik Xülasə")
            
            total_jobs = len(df)
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Ümumi İş Sayı", total_jobs)
            
            with col2:
                if 'temizlenmis_seher' in df.columns:
                    unique_cities = df['temizlenmis_seher'].nunique()
                    st.metric("Unikal Şəhərlər", unique_cities)
            
            with col3:
                if 'job_category_b' in df.columns:
                    unique_categories = df['job_category_b'].nunique()
                    st.metric("İş Kateqoriyaları", unique_categories)
            
            with col4:
                if 'company_b' in df.columns:
                    unique_companies = df['company_b'].nunique()
                    st.metric("Şirkətlər", unique_companies)
            
        except Exception as e:
            st.error(f"❌ Xəta: {e}")
            st.info("Fayl formatını və məlumatların düzgünlüyünü yoxlayın")
    else:
        st.warning(f"⚠️ {FILE_PATH} faylı tapılmadı")
        st.info("""
        **📖 İstifadə Təlimatı:**
        1. 'job_data.csv' və ya 'job_data.xlsx' faylını app-in olduğu qovluğa yerləşdirin
        2. Səhifəni yenidən yükləyin
        3. App avtomatik olaraq bütün analizləri göstərəcək
        
        **📊 ANALİZ XÜSUSİYYƏTLƏRİ:**
        - 🏢 Şirkətlər üzrə iş elanları
        - 📊 İş kateqoriyaları paylanması
        - 🏙️ Bakı rayonları analizi
        - 💰 Kateqoriyalar üzrə orta maaş
        - 📈 Təcrübəyə görə maaş artımı
        - 📅 Aylıq iş elanları trendi
        - 🛠️ Tələb olunan bacarıqlar
        """)

if __name__ == "__main__":
    main()