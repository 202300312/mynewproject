"""AX 전환에 따른 학생 인식 조사: 문항과 DB 저장 함수."""
from auth import db_connection, kst_now

QUESTIONS = [
    "나는 AX(인공지능 전환)가 무엇을 의미하는지 이해하고 있다.",
    "나는 AX가 학교 수업과 학습 방식에 변화를 가져올 것이라고 생각한다.",
    "나는 AI 기반 도구가 학습에 도움이 될 수 있다고 생각한다.",
    "나는 학습 과정에서 AI 도구를 적절하게 활용할 자신이 있다.",
    "나는 AX 시대에 AI 관련 지식을 배우는 것이 중요하다고 생각한다.",
    "나는 AI가 제공한 정보의 정확성을 스스로 확인할 필요가 있다고 생각한다.",
    "나는 AI를 사용할 때 개인정보와 저작권을 보호하는 것이 중요하다고 생각한다.",
    "나는 AX가 미래 직업과 진로 선택에 영향을 줄 것이라고 생각한다.",
    "나는 AX로 인해 발생할 수 있는 공정성·편향 문제에 관심이 있다.",
    "나는 앞으로 AI 관련 학습 활동에 적극적으로 참여할 의향이 있다.",
]
CHOICES = ["1 · 전혀 그렇지 않다", "2 · 그렇지 않다", "3 · 보통이다", "4 · 그렇다", "5 · 매우 그렇다"]

def save_response(userid: str, responses: list[int]) -> None:
    if len(responses) != 10 or any(type(v) is not int or not 1 <= v <= 5 for v in responses):
        raise ValueError("10개 문항에 대해 1~5점으로 모두 응답해야 합니다.")
    cols = ", ".join(["userid"] + [f"q{i}" for i in range(1, 11)] + ["created_at"])
    marks = ",".join("?" for _ in range(12))
    with db_connection() as conn:
        conn.execute(f"INSERT INTO inventory ({cols}) VALUES ({marks})", [userid, *responses, kst_now()])

def response_count(userid: str) -> int:
    with db_connection() as conn:
        return conn.execute("SELECT COUNT(*) FROM inventory WHERE userid=?", (userid,)).fetchone()[0]
