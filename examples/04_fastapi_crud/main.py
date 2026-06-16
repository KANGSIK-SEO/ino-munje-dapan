from __future__ import annotations

from dataclasses import dataclass

from fastapi import Depends, FastAPI, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse

app = FastAPI(title="evollard request CRUD")


@dataclass
class AuthenticationRequest:
    id: int
    client_name: str
    artwork_title: str
    artist_name: str
    medium: str
    risk_score: int
    status: str


class RequestRepository:
    def __init__(self):
        self.rows: list[AuthenticationRequest] = [
            AuthenticationRequest(1, "김컬렉터", "Sunflower Study", "Vincent van Gogh", "oil on canvas", 82, "reviewed")
        ]
        self.next_id = 2

    def list(self) -> list[AuthenticationRequest]:
        return list(self.rows)

    def get(self, request_id: int) -> AuthenticationRequest | None:
        return next((row for row in self.rows if row.id == request_id), None)

    def create(self, client_name: str, artwork_title: str, artist_name: str, medium: str, risk_score: int) -> AuthenticationRequest:
        row = AuthenticationRequest(self.next_id, client_name, artwork_title, artist_name, medium, risk_score, "submitted")
        self.next_id += 1
        self.rows.append(row)
        return row

    def update(self, request_id: int, client_name: str, artwork_title: str, artist_name: str, medium: str, risk_score: int, status: str) -> None:
        row = self.get(request_id)
        if not row:
            raise HTTPException(status_code=404, detail="감정 요청을 찾을 수 없습니다.")
        row.client_name = client_name
        row.artwork_title = artwork_title
        row.artist_name = artist_name
        row.medium = medium
        row.risk_score = risk_score
        row.status = status

    def delete(self, request_id: int) -> None:
        self.rows = [row for row in self.rows if row.id != request_id]


class RequestService:
    def __init__(self, repository: RequestRepository):
        self.repository = repository

    def create_request(self, client_name: str, artwork_title: str, artist_name: str, medium: str, risk_score: int) -> AuthenticationRequest:
        if not client_name or not artwork_title or not artist_name:
            raise HTTPException(status_code=400, detail="고객, 작품, 작가명은 필수입니다.")
        if risk_score < 0 or risk_score > 100:
            raise HTTPException(status_code=400, detail="위험도는 0~100 사이여야 합니다.")
        return self.repository.create(client_name, artwork_title, artist_name, medium, risk_score)


repository = RequestRepository()


def get_service() -> RequestService:
    return RequestService(repository)


def layout(title: str, body: str) -> str:
    return f"""
    <!doctype html>
    <html lang="ko">
    <head>
      <meta charset="utf-8">
      <title>{title}</title>
      <style>
        body {{ font-family: system-ui, sans-serif; max-width: 920px; margin: 40px auto; line-height: 1.5; }}
        nav a, button {{ margin-right: 8px; }}
        input, select {{ display: block; width: 100%; margin: 8px 0 14px; padding: 8px; }}
        table {{ width: 100%; border-collapse: collapse; }}
        th, td {{ border-bottom: 1px solid #ddd; padding: 8px; text-align: left; }}
      </style>
    </head>
    <body>
      <nav><a href="/">홈</a><a href="/requests">감정 요청</a><a href="/requests/new">신규 신청</a></nav>
      {body}
    </body>
    </html>
    """


@app.get("/", response_class=HTMLResponse)
def home():
    return layout(
        "evollard",
        """
        <h1>evollard 감정 요청 CRUD</h1>
        <p>작품 감정 신청을 등록하고, 분석 위험도와 진행 상태를 관리합니다.</p>
        <ul>
          <li>Router: 요청/응답과 Redirect 담당</li>
          <li>Service: 입력 검증과 비즈니스 규칙 담당</li>
          <li>Repository: 데이터 저장/조회 담당</li>
        </ul>
        """,
    )


@app.get("/requests", response_class=HTMLResponse)
def list_requests():
    rows = "".join(
        f"<tr><td>{row.id}</td><td><a href='/requests/{row.id}'>{row.artwork_title}</a></td>"
        f"<td>{row.artist_name}</td><td>{row.risk_score}</td><td>{row.status}</td></tr>"
        for row in repository.list()
    )
    return layout("감정 요청", f"<h1>감정 요청 목록</h1><table><tr><th>ID</th><th>작품</th><th>작가</th><th>위험도</th><th>상태</th></tr>{rows}</table>")


@app.get("/requests/new", response_class=HTMLResponse)
def new_request():
    return layout(
        "신규 감정 신청",
        """
        <h1>신규 감정 신청</h1>
        <form method="post" action="/requests">
          <label>고객명<input name="client_name"></label>
          <label>작품명<input name="artwork_title"></label>
          <label>작가명<input name="artist_name"></label>
          <label>재료<input name="medium" value="oil on canvas"></label>
          <label>초기 위험도<input name="risk_score" type="number" min="0" max="100" value="0"></label>
          <button>신청 저장</button>
        </form>
        """,
    )


@app.post("/requests")
def create_request(
    client_name: str = Form(),
    artwork_title: str = Form(),
    artist_name: str = Form(),
    medium: str = Form(),
    risk_score: int = Form(),
    service: RequestService = Depends(get_service),
):
    service.create_request(client_name, artwork_title, artist_name, medium, risk_score)
    return RedirectResponse("/requests", status_code=303)


@app.get("/requests/{request_id}", response_class=HTMLResponse)
def detail_request(request_id: int):
    row = repository.get(request_id)
    if not row:
        raise HTTPException(status_code=404, detail="감정 요청을 찾을 수 없습니다.")
    return layout(
        row.artwork_title,
        f"""
        <h1>{row.artwork_title}</h1>
        <p>고객: {row.client_name}</p>
        <p>작가: {row.artist_name}</p>
        <p>재료: {row.medium}</p>
        <p>위험도: {row.risk_score}</p>
        <p>상태: {row.status}</p>
        <a href="/requests/{row.id}/edit">수정</a>
        <form method="post" action="/requests/{row.id}/delete"><button>삭제</button></form>
        """,
    )


@app.get("/requests/{request_id}/edit", response_class=HTMLResponse)
def edit_request(request_id: int):
    row = repository.get(request_id)
    if not row:
        raise HTTPException(status_code=404, detail="감정 요청을 찾을 수 없습니다.")
    return layout(
        "감정 요청 수정",
        f"""
        <h1>감정 요청 수정</h1>
        <form method="post">
          <label>고객명<input name="client_name" value="{row.client_name}"></label>
          <label>작품명<input name="artwork_title" value="{row.artwork_title}"></label>
          <label>작가명<input name="artist_name" value="{row.artist_name}"></label>
          <label>재료<input name="medium" value="{row.medium}"></label>
          <label>위험도<input name="risk_score" type="number" min="0" max="100" value="{row.risk_score}"></label>
          <label>상태<select name="status">
            <option>submitted</option><option>analyzing</option><option>reviewed</option><option>paid_report_issued</option><option>rejected</option>
          </select></label>
          <button>수정</button>
        </form>
        """,
    )


@app.post("/requests/{request_id}/edit")
def update_request(
    request_id: int,
    client_name: str = Form(),
    artwork_title: str = Form(),
    artist_name: str = Form(),
    medium: str = Form(),
    risk_score: int = Form(),
    status: str = Form(),
):
    repository.update(request_id, client_name, artwork_title, artist_name, medium, risk_score, status)
    return RedirectResponse(f"/requests/{request_id}", status_code=303)


@app.post("/requests/{request_id}/delete")
def delete_request(request_id: int):
    repository.delete(request_id)
    return RedirectResponse("/requests", status_code=303)
