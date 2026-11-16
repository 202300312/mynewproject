"""랜딩 페이지 + 로그인/회원가입 + 로그인 전용 학습/설문 페이지 내비게이션."""
import streamlit as st
from auth import initialize_db, authenticate, register_user, logged_in, logout
from ui import page_header

st.set_page_config(page_title="ML 교실 | AX 인식 조사", page_icon="🎓", layout="wide", initial_sidebar_state="expanded")
initialize_db()

def landing():
    page_header("WELCOME · MACHINE LEARNING", "머신러닝 교실", "머신러닝을 알아보고 붓꽃 품종을 예측하며, AX 전환에 대한 생각을 공유해 보세요.")
    if logged_in():
        st.success(f"{st.session_state.get('username', '학생')}님, 로그인되었습니다.")
        st.markdown("### 학습 안내")
        st.markdown("왼쪽 메뉴에서 **머신러닝의 개념 → 사례 → 시뮬레이터** 순으로 학습한 다음 **실태조사**에 참여하세요.")
        cols = st.columns(3)
        for col, title, desc in zip(cols, ["🧠 머신러닝의 개념", "🌍 머신러닝의 사례", "🌸 붓꽃 SVM 시뮬레이터"],
                                    ["학습 방법과 핵심 용어", "생활 속 활용과 주의점", "4개 변수로 직접 품종 예측"]):
            with col:
                st.info(f"**{title}**\n\n{desc}")
        return
    st.markdown("### 시작하기")
    st.caption("기존 회원은 로그인, 처음 방문한 학생은 신규등록 탭을 선택하세요.")
    login_tab, signup_tab = st.tabs(["🔐 로그인", "📝 신규등록"])
    with login_tab:
        with st.form("login_form", clear_on_submit=False):
            userid = st.text_input("아이디", key="login_id", max_chars=30)
            password = st.text_input("비밀번호", type="password", key="login_pw")
            submitted = st.form_submit_button("로그인", type="primary", width="stretch")
        if submitted:
            user = authenticate(userid, password)
            if user:
                st.session_state.update({"logged_in": True, **user})
                st.rerun()
            else:
                st.error("아이디 또는 비밀번호를 확인해 주세요.")
    with signup_tab:
        with st.form("signup_form", clear_on_submit=True):
            name = st.text_input("이름", max_chars=40)
            new_id = st.text_input("사용할 아이디 (영문/숫자/밑줄 4~30자)", max_chars=30)
            pw = st.text_input("비밀번호 (8자 이상)", type="password")
            pw_check = st.text_input("비밀번호 확인", type="password")
            st.caption("가입정보와 설문 응답은 학습 운영을 위해 저장됩니다. 관리 담당자에게 개인정보 보관 기간 및 처리 방침을 확인하세요.")
            registered = st.form_submit_button("신규등록", type="primary", width="stretch")
        if registered:
            if pw != pw_check:
                st.error("비밀번호 확인 값이 일치하지 않습니다.")
            else:
                ok, message = register_user(name, new_id, pw)
                (st.success if ok else st.error)(message)

home = st.Page(landing, title="홈 · 로그인", icon="🏠", default=True)
if logged_in():
    sections = {
        "시작": [home],
        "머신러닝 학습": [
            st.Page("pages/0_머신러닝의개념.py", title="머신러닝의 개념", icon="🧠"),
            st.Page("pages/1_머신러닝의사례.py", title="머신러닝의 사례", icon="🌍"),
            st.Page("pages/2_머신러닝시뮬레이터.py", title="머신러닝 시뮬레이터", icon="🌸"),
        ],
        "참여": [st.Page("pages/3_실태조사.py", title="실태조사", icon="📋")],
    }
    with st.sidebar:
        st.write(f"👤 **{st.session_state.get('username')}** (`{st.session_state.get('userid')}`)")
        if st.button("로그아웃", width="stretch"):
            logout()
            st.rerun()
else:
    sections = [home]

nav = st.navigation(sections, position="sidebar")
nav.run()
