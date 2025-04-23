# app.py (Streamlit 기본 UI 체크)
import streamlit as st

def main():
    st.set_page_config(page_title="SmartSwing Tracker", layout="wide")
    
    st.title("✅ Streamlit 정상 작동 테스트")
    st.write("이게 보인다면 Streamlit은 정상입니다.")
    
    if st.button("테스트 버튼"):
        st.success("버튼이 정상 작동합니다!")

if __name__ == "__main__":
    main()
