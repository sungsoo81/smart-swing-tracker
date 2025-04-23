import yfinance as yf
import mplfinance as mpf
import pandas as pd
from datetime import datetime, timedelta

def generate_chart(ticker):
    try:
        end = datetime.today()
        start = end - timedelta(days=60)
        df = yf.download(ticker, start=start, end=end)

        if df.empty:
            return None, "❌ 데이터가 없습니다."

        df = df[['Open', 'High', 'Low', 'Close', 'Volume']]

        # 모든 컬럼 숫자화 + NaN 제거
        df = df.apply(pd.to_numeric, errors='coerce')
        df.dropna(inplace=True)

        # 핵심: 전체 DataFrame을 float64로 강제
        df = df.astype('float64')
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
        return chart_path, None

    except Exception as e:
        return None, f"❌ 차트 생성 실패: {str(e)}"
