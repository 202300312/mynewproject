# 머신러닝 교실 + SQLite 로그인 + AX 실태조사

## 실행
Python 3.10 이상 권장. Anaconda Prompt에서 프로젝트 폴더로 이동하여 다음을 실행합니다.

```bash
conda activate mynewproject
python -m pip install -r requirements.txt
python -m streamlit run run.py
```

접속 시 `run.py`가 랜딩페이지로 작동합니다. 로그인 전에는 **로그인 / 신규등록** 탭만 표시됩니다. 회원가입 후 로그인하면 왼쪽 메뉴에 기존 머신러닝 학습 3개 페이지와 **실태조사**가 나타납니다. 로그아웃 버튼도 사이드바에 있습니다.

## DB
* DB 파일: 프로젝트 루트의 `myproject.db` (첫 실행 시 자동 생성)
* SQLite 연결: `check_same_thread=False`, 단, 모든 DB 작업은 작업별 연결을 생성하고 종료합니다.
* `users`: `id_num`(INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL), `username`, `userid`(UNIQUE), `passwd`(PBKDF2-SHA256 해시), `created_at`
* `inventory`: `id_num`(INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL), `userid`, `q1`~`q10`(1~5 정수), `created_at`; `users.userid` 외래키
* 등록/응답 날짜는 `Asia/Seoul`과 동일한 고정 UTC+09:00 KST 오프셋을 포함한 ISO 8601 형식입니다. (요청의 KTC는 KST로 해석.)
* 설문 문항/척도는 `survey.py`에서 수정할 수 있습니다. 제출할 때마다 새로운 행으로 저장합니다.

## 보안 및 데이터 보호
- 비밀번호는 원문이 아닌 무작위 salt가 포함된 PBKDF2-SHA256으로 저장하며 SQL은 파라미터 바인딩으로 실행합니다.
- 로그인 상태는 Streamlit 세션 단위로 유지하며, 로그인하지 않은 사용자가 직접 페이지 URL을 열어도 접근이 차단됩니다.
- 교육용 최소 구현입니다. 공개 인터넷 운영 전에는 HTTPS, 접근 통제, 로그인 시도 제한, 개인정보 수집 고지·동의, 데이터 보관/삭제 정책, 관리자 접근권한 및 백업 계획을 추가하세요.
- `.gitignore`가 DB 파일의 Git 업로드를 막아주지만, 운영 중에는 별도 파일 접근권한을 설정해야 합니다.
- 기존 가입 데이터가 있는 DB를 덮어쓰지 않으며, 기존 테이블이 없다면 자동 생성합니다.

## 구조
```text
run.py                    # 진입점, 랜딩, 로그인/회원가입, 메뉴
ui.py                     # 공통 CSS
 auth.py                  # DB/인증/비밀번호 해시/접근제어
survey.py                 # AX 인식 10문항과 응답 저장
data.csv, ml.txt          # 기존 부속파일
pages/
  0_머신러닝의개념.py
  1_머신러닝의사례.py
  2_머신러닝시뮬레이터.py
  3_실태조사.py
```

실제 운영 전에 학생 안내문 및 개인정보 수집에 대한 적법한 절차를 마련하세요.
