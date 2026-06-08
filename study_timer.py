import streamlit as st
import pandas as pd
import random
import os
from datetime import datetime

# ------------------------
# 페이지 설정
# ------------------------

st.set_page_config(
    page_title="집중 공부 타이머",
    page_icon="📚",
    layout="wide"
)

# ------------------------
# 데이터 저장 파일
# ------------------------

DATA_FILE = "study_data.csv"

if not os.path.exists(DATA_FILE):
    pd.DataFrame(
        columns=["Date", "Subject", "Minutes"]
    ).to_csv(DATA_FILE, index=False)

# ------------------------
# 명언
# ------------------------

quotes = [
    "오늘의 노력이 내일의 실력이다.",
    "꾸준함이 가장 큰 재능이다.",
    "시작이 반이다.",
    "포기하지 않는 사람이 결국 성공한다.",
    "작은 습관이 큰 변화를 만든다."
]

st.title("📚 집중 공부 타이머")

st.info(random.choice(quotes))

# ------------------------
# 사이드바
# ------------------------

st.sidebar.header("⚙ 설정")

subject = st.sidebar.selectbox(
    "과목 선택",
    ["수학", "영어", "국어", "과학", "사회", "기타"]
)

study_time = st.sidebar.slider(
    "공부 시간 (분)",
    10,
    120,
    50
)

break_time = st.sidebar.slider(
    "쉬는 시간 (분)",
    1,
    30,
    10
)

pomodoro_count = st.sidebar.slider(
    "반복 횟수",
    1,
    8,
    4
)

goal_hour = st.sidebar.number_input(
    "오늘 목표 공부 시간 (시간)",
    1,
    24,
    4
)

goal_text = st.sidebar.text_input(
    "오늘의 목표"
)

# ------------------------
# 목표 표시
# ------------------------

st.subheader("🎯 오늘의 목표")

if goal_text:
    st.write(goal_text)

# ------------------------
# 예상 종료 시간
# ------------------------

total_minutes = (study_time + break_time) * pomodoro_count

end_time = datetime.now()

st.write(
    f"⏳ 예상 종료 시각 : 약 {total_minutes}분 후"
)

# ------------------------
# 공부 시작
# ------------------------

if st.button("▶ 공부 완료 기록하기"):

    df = pd.read_csv(DATA_FILE)

    new_row = {
        "Date": datetime.now().strftime("%Y-%m-%d"),
        "Subject": subject,
        "Minutes": study_time
    }

    df.loc[len(df)] = new_row

    df.to_csv(DATA_FILE, index=False)

    st.success("공부 기록 저장 완료!")

# ------------------------
# 데이터 불러오기
# ------------------------

df = pd.read_csv(DATA_FILE)

today = datetime.now().strftime("%Y-%m-%d")

today_df = df[df["Date"] == today]

today_minutes = today_df["Minutes"].sum()

today_hours = round(today_minutes / 60, 2)

# ------------------------
# 현황
# ------------------------

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "오늘 공부 시간",
        f"{today_minutes}분"
    )

with col2:
    st.metric(
        "목표 시간",
        f"{goal_hour}시간"
    )

with col3:
    st.metric(
        "달성률",
        f"{min(today_hours/goal_hour*100,100):.0f}%"
    )

# ------------------------
# 진행률
# ------------------------

progress = min(today_hours / goal_hour, 1.0)

st.progress(progress)

# ------------------------
# 목표 달성 여부
# ------------------------

if today_hours >= goal_hour:
    st.success("🎉 목표 달성!")
else:
    remain = round(goal_hour - today_hours, 1)
    st.warning(f"목표까지 {remain}시간 남음")

# ------------------------
# 과목별 통계
# ------------------------

st.subheader("📊 과목별 공부 시간")

if len(today_df) > 0:

    subject_data = (
        today_df
        .groupby("Subject")["Minutes"]
        .sum()
    )

    st.bar_chart(subject_data)

# ------------------------
# 최근 기록
# ------------------------

st.subheader("📅 공부 기록")

st.dataframe(
    df.sort_values(
        by="Date",
        ascending=False
    ),
    use_container_width=True
)

# ------------------------
# 총 공부 시간
# ------------------------

st.subheader("🏆 전체 누적 공부 시간")

total_minutes_all = df["Minutes"].sum()

total_hours_all = round(
    total_minutes_all / 60,
    1
)

st.success(
    f"총 {total_hours_all}시간 공부했습니다!"
)
