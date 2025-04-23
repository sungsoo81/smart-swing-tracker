import yfinance as yf
import mplfinance as mpf
from datetime import datetime, timedelta

def generate_chart(ticker):
    end = datetime.today()
    start = end - timedelta(days=60)

    df = yf.download(ticker, start=start, end=end)

    if df.empty:
        return None

    # 필요한 컬럼만 선택
    df = df[['Open', 'High', 'Low', 'Close', 'Volume']]

    # 결측치 제거
    df.dropna(inplace=True)

    # 모든 열을 float 또는 int로 강제 변환
    for col in ['Open', 'High', 'Low', 'Close', 'Volume']:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    df.dropna(inplace=True)  # 변환 후 NaN 제거

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
