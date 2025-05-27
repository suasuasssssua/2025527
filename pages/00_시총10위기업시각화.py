import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
from datetime import date

st.set_page_config(page_title="Top 10 시가총액 주식 시각화", layout="wide")

st.title("📈 2024년 시가총액 상위 10개 기업 주가 시각화")
st.markdown("데이터 출처: [Yahoo Finance](https://finance.yahoo.com)")

# 시가총액 상위 10개 기업 티커
top10_tickers = {
    "Apple": "AAPL",
    "Microsoft": "MSFT",
    "Alphabet (Google)": "GOOGL",
    "Amazon": "AMZN",
    "NVIDIA": "NVDA",
    "Berkshire Hathaway": "BRK-B",
    "Meta (Facebook)": "META",
    "Tesla": "TSLA",
    "TSMC": "TSM",
    "UnitedHealth": "UNH"
}

# 날짜 선택
start_date = st.date_input("시작 날짜", date(2024, 1, 1))
end_date = st.date_input("종료 날짜", date.today())

# 사용자 선택
selected_companies = st.multiselect(
    "기업 선택 (최대 10개)", list(top10_tickers.keys()), default=list(top10_tickers.keys())
)

if selected_companies:
    fig = go.Figure()
    for company in selected_companies:
        ticker = top10_tickers[company]
        data = yf.download(ticker, start=start_date, end=end_date)
        if not data.empty:
            fig.add_trace(go.Scatter(x=data.index, y=data["Adj Close"], mode="lines", name=company))
        else:
            st.warning(f"{company} ({ticker})의 데이터를 가져올 수 없습니다.")
    
    fig.update_layout(
        title="선택한 기업들의 주가 추이",
        xaxis_title="날짜",
        yaxis_title="조정 종가 (USD)",
        height=600,
        template="plotly_dark"
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("하단에서 하나 이상의 기업을 선택하세요.")
