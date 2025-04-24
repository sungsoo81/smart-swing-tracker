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

        # 수치형 강제 변환
        df = df.apply(pd.to_numeric, errors='coerce')
        df.dropna(inplace=True)

        # 핵심 해결책: float64 + .copy() 로 완전 복사
        df = df.astype('float64').copy()
        df.index.name = 'Date'

        # 디버깅용 출력 (Streamlit 콘솔에)
        print("🧪 dtypes:", df.dtypes)
        print("🧪 head:\n", df.head())

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
