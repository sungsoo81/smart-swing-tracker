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

        # 수치형으로 강제 변환 후 결측치 제거
        df = df.apply(pd.to_numeric, errors='coerce')
        df.dropna(inplace=True)

        # 모든 컬럼 float64로 통일 후 복사
        df = df.astype('float64').copy()
        df.index.name = 'Date'

        # 🔍 디버깅 로그 출력
        print("📋 [DEBUG] DataFrame dtypes:")
        print(df.dtypes)

        print("📋 [DEBUG] Open 컬럼 샘플 값:", df["Open"].head(5).tolist())
        print("📋 [DEBUG] Open 첫 값 타입:", type(df["Open"].iloc[0]))

        # 차트 저장
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
