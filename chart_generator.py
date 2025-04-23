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

        # 필요한 컬럼만 추출
        df = df[['Open', 'High', 'Low', 'Close', 'Volume']]

        # 모든 컬럼을 수치형으로 강제 변환 + NaN 처리
        for col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

        # 마지막으로 전체가 float 인지 확인하고 필터링
        df = df.dropna()
        for col in df.columns:
            if not pd.api.types.is_numeric_dtype(df[col]):
                return None, f"❌ 컬럼 {col} 데이터가 float/int 형식이 아닙니다."

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
