import streamlit as st
import rasterio
import numpy as np
import folium
from folium import plugins
from streamlit_folium import st_folium
from rasterio.windows import from_bounds
from shapely.geometry import box
import tempfile
import os

st.set_page_config(layout="wide")
st.title("🌃 대한민국 야간 조도 지도 (2024 VIIRS + Folium 지도 시각화)")

import streamlit as st
import rasterio
import numpy as np
import folium
from folium import plugins
from streamlit_folium import st_folium
from rasterio.windows import from_bounds
from shapely.geometry import box

st.set_page_config(layout="wide")
st.title("🌃 대한민국 야간 조도 지도 (2024 VIIRS + Folium 지도 시각화)")

# 👉 업로드로 파일 받기
uploaded_file = st.file_uploader("🎯 GeoTIFF (.tif) 파일을 업로드하세요", type=["tif"])

if uploaded_file is not None:
    try:
        with rasterio.open(uploaded_file) as src:
            # 대한민국 대략적 범위 자르기
            korea_bounds = box(124.5, 33.0, 131.0, 39.5)
            window = from_bounds(*korea_bounds.bounds, transform=src.transform)
            clipped = src.read(1, window=window)
            clipped_transform = src.window_transform(window)

            # 좌표 계산
            rows, cols = clipped.shape
            xs = np.arange(cols) * clipped_transform.a + clipped_transform.c
            ys = np.arange(rows) * clipped_transform.e + clipped_transform.f
            xs, ys = np.meshgrid(xs, ys)

            mask = clipped > 0
            x_points = xs[mask]
            y_points = ys[mask]
            values = clipped[mask]

            m = folium.Map(location=[36.5, 127.5], zoom_start=6, tiles="CartoDB dark_matter")
            heat_data = [[y, x, float(v)] for x, y, v in zip(x_points, y_points, values)]
            plugins.HeatMap(heat_data, radius=8, blur=10, max_zoom=10).add_to(m)

            st.markdown("✅ 대한민국 위에 야간 조도 히트맵이 표시됩니다.")
            st_folium(m, width=900, height=600)

    except Exception as e:
        st.error(f"❌ 에러 발생: {e}")
else:
    st.info("👆 GeoTIFF (.tif) 파일을 업로드해주세요.")

# 대한민국 위경도 박스
korea_bounds = box(124.5, 33.0, 131.0, 39.5)

try:
    with rasterio.open(tif_path) as src:
        # 클립 영역 만들기
        window = from_bounds(*korea_bounds.bounds, transform=src.transform)
        clipped = src.read(1, window=window)
        clipped_transform = src.window_transform(window)

        # 좌표 계산
        rows, cols = clipped.shape
        xs = np.arange(cols) * clipped_transform.a + clipped_transform.c
        ys = np.arange(rows) * clipped_transform.e + clipped_transform.f
        xs, ys = np.meshgrid(xs, ys)

        # 유효값만 추출 (0 이하 제외)
        mask = clipped > 0
        x_points = xs[mask]
        y_points = ys[mask]
        values = clipped[mask]

        # 지도 생성
        center = [36.5, 127.5]
        m = folium.Map(location=center, zoom_start=6, tiles="CartoDB dark_matter")

        # 조도값을 HeatMapData로 변환
        heat_data = [[y, x, float(v)] for x, y, v in zip(x_points, y_points, values)]
        plugins.HeatMap(heat_data, radius=8, blur=10, max_zoom=10).add_to(m)

        st.markdown("✅ 대한민국 위에 야간 조도 히트맵이 표시됩니다.")
        st_data = st_folium(m, width=900, height=600)

except FileNotFoundError:
    st.error("❗ GeoTIFF 경로가 잘못되었습니다.")
