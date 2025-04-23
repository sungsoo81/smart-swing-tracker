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

    try:
        df = df[['Open', 'High', 'Low', 'Close', 'Volume']]
        df = df.apply(pd.to_numeric, errors='coerce')
        df.dropna(inplace=True)
        df.index.name = 'Date'
        df = df.astype({
            'Open': 'float',
            'High': 'float',
            'Low': 'float',
            'Close': 'float',
            'Volume': 'float'
        })
    except Exception as e:
        print("데이터 전처리 에러:", e)
        return None

    chart_path = f"{ticker}_chart.png"
    try:
        mpf.plot(
            df,
            type='candle',
            mav=(5, 20),
            volume=True,
            style='yahoo',
            savefig=chart_path
        )
        return chart_path
    except Exception as e:
        print("차트 생성 실패:", e)
        return None