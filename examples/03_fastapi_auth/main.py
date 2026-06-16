from __future__ import annotations

from dataclasses import dataclass

from fastapi import Depends, FastAPI, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from starlette.middleware.sessions import SessionMiddleware

app = FastAPI(title="evollard protected reports")
app.add_middleware(SessionMiddleware, secret_key="replace-with-env-secret")

USERS = {
    "collector": {"password": "demo123", "role": "client"},
    "operator": {"password": "demo123", "role": "operator"},
}


@dataclass
class Report:
    id: int
    owner: str
    artwork_title: str
    artist_name: str
    verdict: str
    risk_score: int
    status: str
    price: int


REPORTS = [
    Report(1, "collector", "Sunflower Study", "Vincent van Gogh", "high_risk_fake", 82, "reviewed", 49000),
    Report(2, "collector", "Dot Composition", "Kim Whanki", "likely_authentic", 27, "paid_report_issued", 129000),
]


def current_user(request: Request) -> dict:
    username = request.session.get("user")
    if not username:
        raise HTTPException(status_code=401, detail="로그인이 필요합니다.")
    return {"username": username, **USERS[username]}


def require_operator(user: dict = Depends(current_user)) -> dict:
    if user["role"] != "operator":
        raise HTTPException(status_code=403, detail="운영자 권한이 필요합니다.")
    return user


def layout(request: Request, title: str, body: str) -> str:
    username = request.session.get("user")
    auth_link = "<a href='/logout'>로그아웃</a>" if username else "<a href='/login'>로그인</a>"
    return f"""
    <!doctype html>
    <html lang="ko">
    <head>
      <meta charset="utf-8">
      <title>{title}</title>
      <style>
        body {{ font-family: system-ui, sans-serif; max-width: 920px; margin: 40px auto; line-height: 1.5; }}
        nav a {{ margin-right: 10px; }}
        article {{ border: 1px solid #ddd; padding: 16px; margin: 12px 0; }}
        .risk {{ font-size: 24px; font-weight: 700; }}
      </style>
    </head>
    <body>
      <nav><a href="/">홈</a><a href="/reports">내 리포트</a><a href="/operator">운영자</a>{auth_link}</nav>
      <p>현재 사용자: {username or "로그인 전"}</p>
      {body}
    </body>
    </html>
    """


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return layout(
        request,
        "evollard reports",
        """
        <h1>evollard 유료 감정 리포트</h1>
        <p>로그인한 고객만 감정 리포트를 조회하고, 운영자만 리포트 발행 상태를 변경합니다.</p>
        <p>테스트 계정: collector/demo123, operator/demo123</p>
        """,
    )


@app.get("/login", response_class=HTMLResponse)
def login_form(request: Request):
    return layout(
        request,
        "로그인",
        """
        <h1>로그인</h1>
        <form method="post">
          <label>아이디<input name="username" value="collector"></label>
          <label>비밀번호<input name="password" type="password" value="demo123"></label>
          <button>로그인</button>
        </form>
        """,
    )


@app.post("/login")
def login(request: Request, username: str = Form(), password: str = Form()):
    user = USERS.get(username)
    if not user or user["password"] != password:
        raise HTTPException(status_code=400, detail="아이디 또는 비밀번호가 틀렸습니다.")
    request.session["user"] = username
    return RedirectResponse("/reports", status_code=303)


@app.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/", status_code=303)


@app.get("/reports", response_class=HTMLResponse)
def reports(request: Request, user: dict = Depends(current_user)):
    visible = REPORTS if user["role"] == "operator" else [row for row in REPORTS if row.owner == user["username"]]
    rows = "".join(
        f"""
        <article>
          <h2>{row.artwork_title}</h2>
          <p>{row.artist_name} / {row.verdict}</p>
          <p class="risk">Risk {row.risk_score}/100</p>
          <p>상태: {row.status} / 가격: {row.price:,}원</p>
        </article>
        """
        for row in visible
    )
    return layout(request, "리포트", f"<h1>감정 리포트</h1>{rows or '<p>조회 가능한 리포트가 없습니다.</p>'}")


@app.get("/operator", response_class=HTMLResponse)
def operator_page(request: Request, user: dict = Depends(require_operator)):
    rows = "".join(
        f"""
        <article>
          <h2>{row.artwork_title}</h2>
          <p>{row.status}</p>
          <form method="post" action="/reports/{row.id}/issue">
            <button>유료 리포트 발행</button>
          </form>
        </article>
        """
        for row in REPORTS
    )
    return layout(request, "운영자", f"<h1>운영자 검수</h1>{rows}")


@app.post("/reports/{report_id}/issue")
def issue_report(report_id: int, user: dict = Depends(require_operator)):
    for row in REPORTS:
        if row.id == report_id:
            row.status = "paid_report_issued"
            return RedirectResponse("/operator", status_code=303)
    raise HTTPException(status_code=404, detail="리포트를 찾을 수 없습니다.")
