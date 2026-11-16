"""SQLite 계정 생성/로그인과 공통 접근 제어."""
from __future__ import annotations
import hashlib
import hmac
import os
import re
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone, timedelta
from pathlib import Path
import streamlit as st

DB_PATH = Path(__file__).resolve().parent / "myproject.db"
KST = timezone(timedelta(hours=9))  # 한국 표준시(KST), UTC+09:00
ITERATIONS = 310_000

def kst_now() -> str:
    return datetime.now(KST).isoformat(timespec="seconds")

@contextmanager
def db_connection():
    # 요청 조건: check_same_thread=False. 연결을 전역 공유하지 않고 작업마다 생성/종료합니다.
    conn = sqlite3.connect(str(DB_PATH), check_same_thread=False, timeout=15)
    try:
        conn.execute("PRAGMA busy_timeout=15000")
        conn.execute("PRAGMA foreign_keys=ON")
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

def initialize_db() -> None:
    with db_connection() as conn:
        conn.execute("""CREATE TABLE IF NOT EXISTS users (
            id_num INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            username TEXT NOT NULL,
            userid TEXT NOT NULL UNIQUE,
            passwd TEXT NOT NULL,
            created_at TEXT NOT NULL
        )""")
        conn.execute("""CREATE TABLE IF NOT EXISTS inventory (
            id_num INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            userid TEXT NOT NULL,
            q1 INTEGER NOT NULL CHECK(q1 BETWEEN 1 AND 5),
            q2 INTEGER NOT NULL CHECK(q2 BETWEEN 1 AND 5),
            q3 INTEGER NOT NULL CHECK(q3 BETWEEN 1 AND 5),
            q4 INTEGER NOT NULL CHECK(q4 BETWEEN 1 AND 5),
            q5 INTEGER NOT NULL CHECK(q5 BETWEEN 1 AND 5),
            q6 INTEGER NOT NULL CHECK(q6 BETWEEN 1 AND 5),
            q7 INTEGER NOT NULL CHECK(q7 BETWEEN 1 AND 5),
            q8 INTEGER NOT NULL CHECK(q8 BETWEEN 1 AND 5),
            q9 INTEGER NOT NULL CHECK(q9 BETWEEN 1 AND 5),
            q10 INTEGER NOT NULL CHECK(q10 BETWEEN 1 AND 5),
            created_at TEXT NOT NULL,
            FOREIGN KEY(userid) REFERENCES users(userid)
        )""")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_inventory_userid ON inventory(userid)")

def hash_password(password: str) -> str:
    salt = os.urandom(16)
    key = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, ITERATIONS)
    return f"pbkdf2_sha256${ITERATIONS}${salt.hex()}${key.hex()}"

def verify_password(password: str, stored: str) -> bool:
    try:
        algo, rounds, salt_hex, expected_hex = stored.split("$")
        if algo != "pbkdf2_sha256":
            return False
        rounds = int(rounds)
        if not 100_000 <= rounds <= 1_000_000:
            return False
        expected = bytes.fromhex(expected_hex)
        digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), bytes.fromhex(salt_hex), rounds)
        return hmac.compare_digest(digest, expected)
    except (ValueError, TypeError, AttributeError):
        return False

def register_user(username: str, userid: str, password: str) -> tuple[bool, str]:
    username, userid = username.strip(), userid.strip()
    if not 2 <= len(username) <= 40:
        return False, "이름은 2~40자로 입력해 주세요."
    if not re.fullmatch(r"[A-Za-z0-9_]{4,30}", userid):
        return False, "아이디는 영문, 숫자, 밑줄(_)로 4~30자여야 합니다."
    if len(password) < 8 or len(password) > 128:
        return False, "비밀번호는 8~128자로 설정해 주세요."
    try:
        with db_connection() as conn:
            conn.execute("INSERT INTO users (username,userid,passwd,created_at) VALUES (?,?,?,?)",
                         (username, userid, hash_password(password), kst_now()))
        return True, "회원가입이 완료되었습니다. 로그인해 주세요."
    except sqlite3.IntegrityError:
        return False, "이미 사용 중인 아이디입니다."

def authenticate(userid: str, password: str) -> dict | None:
    with db_connection() as conn:
        row = conn.execute("SELECT id_num,username,userid,passwd FROM users WHERE userid=?", (userid.strip(),)).fetchone()
    if row and verify_password(password, row[3]):
        return {"id_num": row[0], "username": row[1], "userid": row[2]}
    return None

def logged_in() -> bool:
    return bool(st.session_state.get("logged_in") and st.session_state.get("userid"))

def require_login() -> None:
    if not logged_in():
        st.warning("로그인이 필요한 페이지입니다. 먼저 홈에서 로그인해 주세요.")
        st.stop()

def logout() -> None:
    for key in ("logged_in", "userid", "username", "id_num"):
        st.session_state.pop(key, None)
