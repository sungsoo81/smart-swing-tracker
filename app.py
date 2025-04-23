# Streamlit 메인 앱
import streamlit as st

st.set_page_config(page_title="SmartSwing Tracker", layout="wide")

# ---------------- UI ---------------- #
try:
    st.title("📈 SmartSwing Tracker")
    st.markdown("이 앱은 미국 주식 자동 추천 및 전략 기반 트래킹 시스템입니다.")
    st.markdown("---")

    with st.sidebar:
        st.header("📊 메뉴")
        st.write("아래 버튼을 눌러 테스트 데이터를 확인하거나 기능을 점검하세요.")

    if st.button("📈 샘플 전략 보기"):
        st.success("샘플 전략: RSI + MACD + 볼밴 골든크로스 → 예상 수익률 +5%")

    st.info("✅ 시스템 정상 작동 중입니다. 조건을 설정하면 자동으로 추천 종목이 표시됩니다.")

    # 여기에 추후 데이터 로직 (예: 추천종목, 차트 등) 추가 가능

except Exception as e:
    st.error(f"❗ 오류가 발생했습니다: {e}")
