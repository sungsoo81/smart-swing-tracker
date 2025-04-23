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

    # 완벽하게 float32로 변환 (강제 형 지정)
    df = df.astype({
        'Open': 'float32',
        'High': 'float32',
        'Low': 'float32',
        'Close': 'float32',
        'Volume': 'float32'
    })

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
