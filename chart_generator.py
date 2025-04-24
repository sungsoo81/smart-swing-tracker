import yfinance as yf
import mplfinance as mpf
import pandas as pd
from datetime import datetime, timedelta
import logging

# 로깅 설정
logging.basicConfig(level=logging.INFO)

def generate_chart(ticker):
    try:
        # 날짜 범위 설정
        end = datetime.today()
        start = end - timedelta(days=60)

        # 주가 데이터 다운로드
        df = yf.download(ticker, start=start, end=end)

        # 필수 컬럼 확인
        required_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
        if df.empty or not all(col in df.columns for col in required_columns):
            logging.warning("❌ 필요한 컬럼이 누락되었습니다.")
            return None, "❌ 데이터가 없습니다: 필요한 열이 없습니다."

        # 필요한 열만 추출 후 결측치 제거
        df = df[required_columns].dropna()

        # 🔍 디버깅: 'Open' 컬럼 타입과 샘플 확인
        lopen_series = df["Open"]
        logging.info(f"[DEBUG] df['Open'].dtype: {open_series.dtype}")
        logging.info(f"[DEBUG] df['Open'].head():\n{open_series.head(10)}")
        logging.info(f"[DEBUG] 값 타입:\n{[type(x) for x in open_series.head(10)]}")

        # 모든 열을 float64로 변환
        df = df.astype('float64').copy()
        df.index.name = 'Date'

        # 차트 파일 경로 생성
        chart_path = f"{ticker}_{datetime.now().strftime('%Y%m%d%H%M%S')}_chart.png"

        # 차트 생성
        mpf.plot(
            df,
            type='candle',
            mav=(5, 20),
            volume=True,
            style='yahoo',
            savefig=chart_path
        )

        logging.info(f"✅ 차트 생성 완료: {chart_path}")
        return chart_path, None

    except Exception as e:
        logging.error(f"차트 생성 중 예외 발생: {str(e)}")
        return None, f"❌ 차트 생성 실패: {str(e)}"
