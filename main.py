import streamlit as st
import folium
from streamlit_folium import st_folium

# 랜드마크 정보
landmarks = {
    "France": {
        "name": "Eiffel Tower",
        "location": [48.8584, 2.2945],
        "description": "An iconic symbol of France located in Paris."
    },
    "USA": {
        "name": "Statue of Liberty",
        "location": [40.6892, -74.0445],
        "description": "A gift from France, located in New York."
    },
    "China": {
        "name": "Great Wall of China",
        "location": [40.4319, 116.5704],
        "description": "A historic wall stretching across northern China."
    },
    "India": {
        "name": "Taj Mahal",
        "location": [27.1751, 78.0421],
        "description": "A white marble mausoleum in Agra."
    },
    "Brazil": {
        "name": "Christ the Redeemer",
        "location": [-22.9519, -43.2105],
        "description": "A massive statue overlooking Rio de Janeiro."
    }
}

# 사이드바에서 국가 선택
selected_country = st.sidebar.selectbox("Choose a Country", list(landmarks.keys()))

# 지도 생성
m = folium.Map(location=landmarks[selected_country]["location"], zoom_start=4)

# 모든 랜드마크 추가
for country, info in landmarks.items():
    folium.Marker(
        location=info["location"],
        popup=f"{info['name']}: {info['description']}",
        tooltip=info["name"],
        icon=folium.Icon(color="blue" if country != selected_country else "red")
    ).add_to(m)

st.title("🌍 World Landmarks Map")
st.markdown(f"### Selected: {selected_country} - {landmarks[selected_country]['name']}")

# 지도 표시
st_folium(m, width=700, height=500)
