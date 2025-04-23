import streamlit as st
from sheet_manager import record_recommendation
from email_notifier import send_email
from chart_generator import generate_chart
from pdf_report import create_pdf_report
from drive_uploader import upload_to_drive

st.set_page_config(page_title="SmartSwing Tracker", layout="wide")
st.title("📈 SmartSwing Tracker")

with st.spinner("🔍 조건 스캔 중..."):
    ticker = "NVDA"
    strategy = "RSI 반등 + MACD 골든크로스"

    st.success(f"✅ 추천 종목: {ticker} / 전략: {strategy}")
    record_recommendation(ticker, strategy)
    send_email(ticker, strategy)
    chart_path = generate_chart(ticker)
    st.image(chart_path)
    pdf_path = create_pdf_report(ticker, strategy, chart_path)
    upload_to_drive(pdf_path)
    st.success("📄 PDF 리포트가 Google Drive에 저장되었습니다.")