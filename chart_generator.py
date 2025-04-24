import yfinance as yf
import mplfinance as mpf
import pandas as pd
from datetime import datetime, timedelta
import logging

# 로깅 설정 (Streamlit에서는 콘솔에서 확인 가능)
logging.basicConfig(level=logging.INFO)

def generate_chart(ticker):
    try:
        # 1. 날짜 설정
        end = datetime.today()
        start = end - timedelta(days=60)

        # 2. 데이터 다운로드
        df = yf.download(ticker, start=start, end=end)

        # 3. 필수 컬럼 유무 확인
        required_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
        if df.empty or not all(col in df.columns for col in required_columns):
            logging.warning("❌ 필요한 컬럼이 누락되었습니다.")
            return None, "❌ 데이터가 없습니다: 필요한 열이 없습니다."

        # 4. 필수 컬럼만 추출 + 결측치 제거
        df = df[required_columns].dropna()

        # 5. Open 컬럼만 Series로 분리해서 디버깅
        open_series = df["Open"]
        logging.info(f"[DEBUG] Open dtype: {open_series.dtype}")
        logging.info(f"[DEBUG] Open values (head):\n{open_series.head()}")
        logging.info(f"[DEBUG] Open types:\n{[type(x) for x in open_series.head()]}")

        # 6. 전체 float64로 강제 변환 후 복사
        df = df.astype("float64").copy()
        df.index.name = "Date"

        # 7. 차트 경로 생성
        chart_path = f"{ticker}_{datetime.now().strftime('%Y%m%d%H%M%S')}_chart.png"

        # 8. 차트 생성
        mpf.plot(
            df,
            type="candle",
            mav=(5, 20),
            volume=True,
            style="yahoo",
            savefig=chart_path
        )

        logging.info(f"✅ 차트 생성 완료: {chart_path}")
        return chart_path, None

    except Exception as e:
        logging.error(f"차트 생성 중 예외 발생: {str(e)}")
        return None, f"❌ 차트 생성 실패: {str(e)}"
