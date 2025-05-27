import streamlit as st
import yfinance as yf
import plotly.graph_objects as go

st.set_page_config(page_title="글로벌 시가총액 상위 10대 기업 주가", layout="wide")

st.title("📈 글로벌 시가총액 상위 10대 기업 주가 시각화")
st.markdown("최근 6개월간의 주가를 인터랙티브하게 확인해보세요.")

# 시가총액 상위 10개 기업 (사우디 아람코 제외, yfinance에서 데이터 불안정)
top_10_tickers = {
    "Apple": "AAPL",
    "Microsoft": "MSFT",
    "Nvidia": "NVDA",
    "Alphabet (Google)": "GOOGL",
    "Amazon": "AMZN",
    "Berkshire Hathaway": "BRK-B",
    "Meta (Facebook)": "META",
    "TSMC": "TSM",
    "Eli Lilly": "LLY",
    "Broadcom": "AVGO"  # 대체로 시총 기준 Top 10에 포함
}

# 사용자 선택
selected_companies = st.multiselect(
    "시각화할 회사를 선택하세요:",
    options=list(top_10_tickers.keys()),
    default=list(top_10_tickers.keys())
)

# 주가 데이터 다운로드
with st.spinner("📡 주가 데이터를 불러오는 중입니다..."):
    data = yf.download(
        [top_10_tickers[company] for company in selected_companies],
        period="6mo",
        group_by="ticker",
        auto_adjust=True,
        threads=True
    )

# Plotly 그래프 생성
fig = go.Figure()

for company in selected_companies:
    ticker = top_10_tickers[company]
    try:
        fig.add_trace(go.Scatter(
            x=data[ticker].index,
            y=data[ticker]['Close'],
            mode='lines',
            name=company
        ))
    except Exception as e:
        st.warning(f"{company} 데이터를 불러오는 중 오류 발생: {e}")

# 레이아웃 설정
fig.update_layout(
    title="최근 6개월간의 주가 변동",
    xaxis_title="날짜",
    yaxis_title="주가 (USD)",
    template="plotly_white",
    hovermode="x unified",
    height=600
)

# 그래프 출력
st.plotly_chart(fig, use_container_width=True)
