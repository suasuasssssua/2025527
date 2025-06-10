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

# GeoTIFF 직접 경로 입력
tif_path = "C:/Users/YourName/Downloads/VNL_npp_2024_global_vcmslcfg_v2_c202502261200.average_masked.dat.tif"  # ← 본인 경로로 수정

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
