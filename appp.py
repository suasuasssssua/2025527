import streamlit as st
import folium
from streamlit_folium import st_folium

st.title("🗺️ 지도 테스트")

m = folium.Map(location=[36.5, 127.5], zoom_start=6)
st_data = st_folium(m, width=700, height=500)
