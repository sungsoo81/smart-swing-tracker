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

    # 1. 모든 컬럼 float 변환
    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # 2. 숫자형 아닌 컬럼 제거 (예외 처리까지 포함)
    for col in df.columns:
        if not pd.api.types.is_numeric_dtype(df[col]):
            df.drop(columns=[col], inplace=True)

    # 3. 필수 컬럼이 누락된 경우 예외 처리
    required_cols = {'Open', 'High', 'Low', 'Close', 'Volume'}
    if not required_cols.issubset(df.columns):
        return None  # 차트 생성을 중단

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
