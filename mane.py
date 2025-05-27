import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static

# 데이터 불러오기
@st.cache_data
def load_data():
    df = pd.read_csv("data/편의시설정보.csv", encoding='cp949')  # 인코딩 주의
    df = df.dropna(subset=["위도", "경도"])  # 위경도 없는 행 제거
    return df

df = load_data()

st.title("전국 장애인 편의시설 지도")
st.markdown("공공데이터 기반으로 시각화한 전국의 장애인 편의시설 분포입니다.")

# 필터: 시도 선택
sido_options = df["시도명"].unique()
selected_sido = st.selectbox("시도 선택", sorted(sido_options))
filtered_df = df[df["시도명"] == selected_sido]

# 필터: 시설 유형
facility_types = filtered_df["편의시설명"].unique()
selected_facilities = st.multiselect("시설 유형 선택", facility_types, default=list(facility_types))
filtered_df = filtered_df[filtered_df["편의시설명"].isin(selected_facilities)]

# 지도 생성
m = folium.Map(location=[filtered_df["위도"].mean(), filtered_df["경도"].mean()], zoom_start=11)

for _, row in filtered_df.iterrows():
    folium.Marker(
        location=[row["위도"], row["경도"]],
        popup=f"{row['편의시설명']}<br>{row['상세위치']}",
        icon=folium.Icon(color="blue", icon="info-sign")
    ).add_to(m)

folium_static(m)

# 데이터 테이블
st.subheader("편의시설 목록")
st.dataframe(filtered_df[["편의시설명", "시군구명", "상세위치"]].reset_index(drop=True))
