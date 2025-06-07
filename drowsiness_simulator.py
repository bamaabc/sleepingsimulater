
import streamlit as st
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# 초기 설정
st.set_page_config(page_title="졸음운전 방지 시뮬레이터", layout="centered")
st.title("🧠 실시간 졸음운전 방지 및 자율운전 시스템 시뮬레이터")

# 상태 초기화
if "running" not in st.session_state:
    st.session_state.running = False
if "data" not in st.session_state:
    st.session_state.data = []

# 졸음 상태 판단
def classify_drowsiness(theta, alpha):
    ratio = (theta / alpha) * 100
    if ratio < 30:
        return ratio, "각성", 0
    elif ratio < 60:
        return ratio, "경계", 1
    elif ratio < 80:
        return ratio, "졸음", 2
    else:
        return ratio, "위험", 3

# 운전 시작
if st.button("🚗 운전 시작"):
    st.session_state.running = True
    st.session_state.data = []

# 시뮬레이션 실행
if st.session_state.running:
    st.subheader("📡 실시간 EEG 데이터 측정 중...")
    chart = st.line_chart()

    for i in range(60):
        theta = np.random.uniform(10, 30)
        alpha = np.random.uniform(20, 50)
        drowsiness_score, state, level = classify_drowsiness(theta, alpha)

        st.session_state.data.append({
            "시간": pd.Timestamp.now().strftime("%H:%M:%S"),
            "세타": theta,
            "알파": alpha,
            "졸음지수": drowsiness_score,
            "상태": state,
            "자율단계": level
        })

        chart.add_rows({"졸음지수": [drowsiness_score]})
        st.markdown(f"**현재 졸음 상태:** `{state}` / **자율운전 단계:** `Level {level}`")

        if level == 3:
            st.error("⚠️ 졸음 위험! 자율정차 개입 중!")
        time.sleep(0.3)

    st.success("✅ 시뮬레이션 완료!")

    df = pd.DataFrame(st.session_state.data)
    st.line_chart(df[["졸음지수"]])
    st.dataframe(df)
