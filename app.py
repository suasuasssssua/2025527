import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static

st.title("전국 장애인 편의시설 지도")
uploaded_file = st.file_uploader("CSV 파일을 업로드하세요 (예: 전국장애인편의시설정보.csv)", type="csv")

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file, encoding='cp949')
    except UnicodeDecodeError:
        df = pd.read_csv(uploaded_file, encoding='utf-8')

    df = df.dropna(subset=["위도", "경도"])

    # 필터
    selected_sido = st.selectbox("시도 선택", sorted(df["시도명"].dropna().unique()))
    facility_options = df["편의시설명"].dropna().unique()
    selected_facilities = st.multiselect("시설 유형 선택", facility_options, default=list(facility_options))

    filtered = df[(df["시도명"] == selected_sido) & (df["편의시설명"].isin(selected_facilities))]

    # 지도
    m = folium.Map(location=[filtered["위도"].mean(), filtered["경도"].mean()], zoom_start=11)
    for _, row in filtered.iterrows():
        folium.Marker(
            location=[row["위도"], row["경도"]],
            popup=f"{row['편의시설명']}<br>{row['상세위치']}",
            icon=folium.Icon(color="blue", icon="info-sign")
        ).add_to(m)

    folium_static(m)
    st.subheader("편의시설 목록")
    st.dataframe(filtered[["편의시설명", "시군구명", "상세위치"]].reset_index(drop=True))
else:
    st.warning("CSV 파일을 먼저 업로드하세요.")
