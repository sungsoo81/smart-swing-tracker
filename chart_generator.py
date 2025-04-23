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

        # 컬럼별로 숫자형만 남기고 아닌 건 row 자체 삭제
        for col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

        df.dropna(inplace=True)

        # 마지막 double-check: 모든 row가 float인지 검사
        for col in df.columns:
            if not all(isinstance(x, (int, float)) for x in df[col]):
                return None, f"❌ {col} 컬럼에 숫자 외의 값이 존재합니다."

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
