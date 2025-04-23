import streamlit as st
from strategy_checker import get_recommended_stocks
from sheet_manager import record_recommendation, check_exit_conditions
from email_notifier import send_email_notification

st.set_page_config(page_title="SmartSwing Tracker", layout="wide")
st.title("📈 SmartSwing Tracker")
st.markdown("자동화된 미국 주식 추천 및 전략 기반 트래킹 시스템입니다.")
st.markdown("---")

if st.button("📊 조건 만족 종목 스캔"):
    st.info("조건을 확인 중입니다...")
    stocks = get_recommended_stocks()
    if not stocks:
        st.warning("조건에 맞는 종목이 없습니다.")
    else:
        for stock in stocks:
            st.success(f"✅ 추천 종목: {stock['ticker']} / 전략: {stock['strategy']}")
            record_recommendation(stock)
            send_email_notification(stock['ticker'], stock['strategy'])

if st.button("🧾 수익률 조건 체크 및 알림"):
    results = check_exit_conditions()
    if results:
        for res in results:
            st.info(f"📬 알림 전송됨: {res}")
    else:
        st.success("조건에 해당하는 종목이 없습니다.")