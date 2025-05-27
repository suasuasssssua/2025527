import yfinance as yf
import plotly.graph_objects as go

# 시가총액 상위 10개 기업 티커
tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'BRK-B', 'META', 'TSLA', 'TSM', 'UNH']

# 기간 설정
start_date = "2024-01-01"
end_date = "2024-05-27"

# 그래프 객체 초기화
fig = go.Figure()

# 각 티커에 대해 주가 데이터 가져오기 및 시각화
for ticker in tickers:
    data = yf.download(ticker, start=start_date, end=end_date)
    fig.add_trace(go.Scatter(x=data.index, y=data['Adj Close'], mode='lines', name=ticker))

# 레이아웃 설정
fig.update_layout(
    title="2024년 시가총액 상위 10개 기업의 주가 추이",
    xaxis_title="날짜",
    yaxis_title="조정 종가 (USD)",
    template="plotly_dark",
    height=600
)

fig.show()
