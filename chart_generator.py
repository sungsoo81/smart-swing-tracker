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

        # 디버깅 로그 출력
        print("📋 dtypes:")
        print(df.dtypes)
        print("📋 Sample Open values:", df['Open'].head(5).tolist())
        print("📋 Open type example:", type(df['Open'].iloc[0]))

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
