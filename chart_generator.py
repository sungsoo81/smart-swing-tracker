import yfinance as yf
import mplfinance as mpf
from datetime import datetime, timedelta

def generate_chart(ticker):
    end = datetime.today()
    start = end - timedelta(days=60)

    df = yf.download(ticker, start=start, end=end)

    if df.empty:
        return None  # 데이터 없을 경우 처리

    df.index.name = 'Date'
    df = df[['Open', 'High', 'Low', 'Close', 'Volume']]

    chart_path = f"{ticker}_chart.png"
    mpf.plot(
        df,
        type='candle',
        mav=(5, 20),
        volume=True,
        style='yahoo',
        savefig=chart_path
    )
    return chart_path
