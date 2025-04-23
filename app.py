import streamlit as st
from sheet_manager import record_recommendation
from email_notifier import send_email
from chart_generator import generate_chart
from pdf_report import create_pdf_report
from drive_uploader import upload_to_drive

# ✅ 가장 먼저 위치해야 함!
st.set_page_config(
    page_title="SmartSwing Tracker",
    layout="wide",
    initial_sidebar_state="expanded"  # 사이드바 강제 열기
)

st.title("📈 SmartSwing Tracker")

# ✅ credentials.json 업로드 UI 추가
uploaded_file = st.sidebar.file_uploader("📤 여기에 credentials.json 파일 업로드", type="json")
if uploaded_file:
    with open("credentials.json", "wb") as f:
        f.write(uploaded_file.read())
    st.sidebar.success("✅ credentials.json 업로드 완료!")

# ✅ 조건 체크 시작
with st.spinner("🔍 조건 스캔 중..."):
    ticker = "NVDA"
    strategy = "RSI 반등 + MACD 골든크로스"

    st.success(f"✅ 추천 종목: {ticker} / 전략: {strategy}")
    record_recommendation(ticker, strategy)
    send_email(ticker, strategy)
    chart_path = generate_chart(ticker)
    st.image(chart_path, caption=f"{ticker} 기술 차트")
    pdf_path = create_pdf_report(ticker, strategy, chart_path)
    upload_to_drive(pdf_path)
    st.success("📄 PDF 리포트가 Google Drive에 저장되었습니다.")

chart_path = generate_chart(ticker)
if chart_path:
    st.image(chart_path, caption=f"{ticker} 기술 차트")
else:
    st.warning(f"{ticker} 차트 생성에 실패했습니다.")

