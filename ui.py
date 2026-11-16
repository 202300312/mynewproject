"""학습 페이지에서 공통으로 사용하는 스타일과 소개 컴포넌트."""
import streamlit as st

CSS = """
<style>
:root { --ink:#15243b; --muted:#54647c; --line:#e4eaf2; --accent:#2962ff; }
.block-container {max-width: 1140px; padding-top: 2.2rem; padding-bottom: 3rem;}
html, body, [class*="css"] {font-family: 'Pretendard', 'Noto Sans KR', sans-serif;}
.hero {background:linear-gradient(120deg,#13294b 0%,#254e89 68%,#2c75b5 100%);color:#fff;
 border-radius:22px;padding:34px 36px;margin:0 0 24px;box-shadow:0 12px 30px rgba(20,51,91,.14)}
.hero .eyebrow {font-size:.8rem;font-weight:750;letter-spacing:.16em;color:#c2dbff;margin-bottom:12px}
.hero h1 {font-size:clamp(1.7rem,3vw,2.55rem);line-height:1.25;letter-spacing:-.035em;margin:0 0 10px;color:#fff}
.hero p {font-size:1rem;line-height:1.7;margin:0;color:#e0eafa}
.info-card {background:var(--secondary-background-color, #f8fafc);border:1px solid var(--line);border-radius:17px;
 padding:20px 22px;margin:8px 0 16px;min-height:115px}
.info-card h3 {font-size:1.03rem;margin:0 0 9px;color:var(--text-color, #15243b)}
.info-card p {margin:0;color:var(--text-color, #344256);line-height:1.7;font-size:.94rem}
.kicker {display:inline-block;border-radius:100px;background:#eaf2ff;color:#1e4a95;padding:6px 12px;
 font-size:.79rem;font-weight:750;margin-bottom:12px}
.lesson-note {background:rgba(40,110,200,.07);border-left:4px solid #367bd4;padding:16px 20px;border-radius:4px 13px 13px 4px;margin:14px 0;line-height:1.8}
.small-muted {font-size:.86rem;color:#697991;line-height:1.6}
@media(max-width:650px){.hero{padding:24px 22px;border-radius:16px}.block-container{padding-top:1.2rem}}
</style>
"""


def page_header(tag: str, title: str, subtitle: str) -> None:
    st.markdown(CSS, unsafe_allow_html=True)
    st.markdown(
        f'<div class="hero"><div class="eyebrow">{tag}</div>'
        f'<h1>{title}</h1><p>{subtitle}</p></div>',
        unsafe_allow_html=True,
    )


def info_card(title: str, body: str) -> None:
    st.markdown(f'<div class="info-card"><h3>{title}</h3><p>{body}</p></div>', unsafe_allow_html=True)
