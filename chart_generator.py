import yfinance as yf
import mplfinance as mpf
import pandas as pd
from datetime import datetime, timedelta

def generate_chart(ticker):
    end = datetime.today()
    start = end - timedelta(days=60)

    df = yf.download(ticker, start=start, end=end)

    if df.empty:
        return None

    df = df[['Open', 'High', 'Low', 'Close', 'Volume']]

    # 모든 컬럼을 숫자형으로 강제 변환
    df = df.apply(pd.to_numeric, errors='coerce')
    df.dropna(inplace=True)

    df.index.name = 'Date'

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
