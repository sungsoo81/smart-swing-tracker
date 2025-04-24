import yfinance as yf
import mplfinance as mpf
import pandas as pd
from datetime import datetime, timedelta
import logging

# 로깅 설정 (디버깅과 오류 확인을 위해)
logging.basicConfig(level=logging.INFO)

def generate_chart(ticker):
    try:
        # 날짜 설정
        end = datetime.today()
        start = end - timedelta(days=60)

        # 데이터 다운로드
        df = yf.download(ticker, start=start, end=end)
        
        # 데이터 유효성 검사
        if df.empty or not all(col in df.columns for col in ['Open', 'High', 'Low', 'Close', 'Volume']):
            logging.warning("필요한 데이터가 없습니다.")
            return None, "❌ 데이터가 없습니다: 필요한 열이 없습니다."

        # 필요한 열 선택 및 데이터 처리
        df = df[['Open', 'High', 'Low', 'Close', 'Volume']].dropna()

# ✅ 여기!
        logging.info(f"[DEBUG] df['Open'].dtypes: {df['Open'].dtypes}")
        logging.info(f"[DEBUG] df['Open'] head: {df['Open'].head(10)}")
        logging.info(f"[DEBUG] 타입 확인: {[type(val) for val in df['Open'].head(10)]}")

df = df.astype('float64')
df.index.name = 'Date'


        # 차트 파일 경로 설정
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
        logging.info(f"차트가 성공적으로 저장되었습니다: {chart_path}")
        return chart_path, None

    except ImportError as ie:
        logging.error(f"라이브러리 오류: {str(ie)}")
        return None, f"❌ 필요한 라이브러리를 설치하세요: {str(ie)}"
    except Exception as e:
        logging.error(f"차트 생성 중 오류 발생: {str(e)}")
        return None, f"❌ 차트 생성 실패: {str(e)}"

# 함수 테스트
if __name__ == "__main__":
    ticker = "AAPL"  # 원하는 티커 심볼 입력
    chart, error = generate_chart(ticker)
    if error:
        print(error)
    else:
        print(f"✅ 차트 파일 경로: {chart}")
