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

        df = df.apply(pd.to_numeric, errors='coerce')
        df.dropna(inplace=True)
        df = df.astype('float64').copy()
        df.index.name = 'Date'

        # ✅ 디버깅 로그 (확실한 Series 형태 사용)
        open_series = df["Open"]
        print("📋 Sample Open values:", open_series.head(5).tolist())  # ✅ 이게 정답
        print("📋 Open 타입:", type(open_series))
        print("📋 값 타입:", type(open_series.iloc[0]))

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
