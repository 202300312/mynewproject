"""AX 전환 관련 인식 조사: 로그인 후 설문 응답 저장."""
import sqlite3
import streamlit as st
from auth import require_login
from survey import QUESTIONS, CHOICES, save_response, response_count
from ui import page_header

require_login()
page_header("SURVEY · AX AWARENESS", "AX 전환에 따른 학생 인식 실태조사", "인공지능 전환(AX)에 대한 이해, 활용 인식, 윤리 의식과 학습 의향을 조사합니다.")
st.markdown("**AX(AI Transformation)** 는 교육, 업무, 사회의 활동과 절차가 인공지능을 중심으로 변화하는 것을 뜻합니다.")
st.info("총 10문항 · 5점 리커트 척도 · 정답 없음 · 모든 문항 필수 응답")
st.caption("응답은 계정 아이디와 연결되어 SQLite 데이터베이스에 저장됩니다. 중복 제출도 별도의 응답으로 저장됩니다.")
userid = st.session_state["userid"]
st.write(f"현재까지 제출한 응답: **{response_count(userid)}회**")
with st.form("ax_survey", clear_on_submit=True):
    choices = []
    for i, question in enumerate(QUESTIONS, start=1):
        choice = st.radio(f"{i}. {question}", CHOICES, index=None, key=f"ax_q{i}", horizontal=False)
        choices.append(choice)
    submitted = st.form_submit_button("설문 제출하기", type="primary", width="stretch")
if submitted:
    if any(value is None for value in choices):
        st.error("모든 문항에 응답해 주세요. 미응답 항목이 있습니다.")
    else:
        values = [CHOICES.index(value) + 1 for value in choices]
        try:
            save_response(userid, values)
        except (sqlite3.Error, ValueError):
            st.error("설문 저장 중 오류가 발생했습니다. 관리자에게 문의해 주세요.")
        else:
            st.success("응답이 정상적으로 저장되었습니다. 참여해 주셔서 감사합니다.")
            st.balloons()
