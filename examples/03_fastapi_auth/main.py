from fastapi import Depends, FastAPI, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from starlette.middleware.sessions import SessionMiddleware

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="change-me")

USERS = {"demo": "demo123"}
TASKS = [{"id": 1, "owner": "demo", "title": "첫 작업", "status": "TODO"}]


def current_user(request: Request) -> str:
    user = request.session.get("user")
    if not user:
        raise HTTPException(status_code=401, detail="로그인이 필요합니다.")
    return user


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    user = request.session.get("user")
    return f"""
    <h1>FastAPI 인증 예제</h1>
    <p>현재 사용자: {user or "로그인 전"}</p>
    <a href="/login">로그인</a> | <a href="/tasks">작업 목록</a> | <a href="/logout">로그아웃</a>
    """


@app.get("/login", response_class=HTMLResponse)
def login_form():
    return """
    <h1>로그인</h1>
    <form method="post">
      <input name="username" placeholder="demo">
      <input name="password" placeholder="demo123" type="password">
      <button>로그인</button>
    </form>
    """


@app.post("/login")
def login(request: Request, username: str = Form(), password: str = Form()):
    if USERS.get(username) != password:
        raise HTTPException(status_code=400, detail="아이디 또는 비밀번호가 틀렸습니다.")
    request.session["user"] = username
    return RedirectResponse("/tasks", status_code=303)


@app.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/", status_code=303)


@app.get("/tasks", response_class=HTMLResponse)
def task_list(user: str = Depends(current_user)):
    rows = "".join(
        f"<li>{task['title']} - {task['status']} "
        f"<form style='display:inline' method='post' action='/tasks/{task['id']}/done'>"
        f"<button>완료</button></form></li>"
        for task in TASKS
        if task["owner"] == user
    )
    return f"<h1>{user}의 작업</h1><ul>{rows}</ul><a href='/'>홈</a>"


@app.post("/tasks/{task_id}/done")
def mark_done(task_id: int, user: str = Depends(current_user)):
    for task in TASKS:
        if task["id"] == task_id and task["owner"] == user:
            task["status"] = "DONE"
            return RedirectResponse("/tasks", status_code=303)
    raise HTTPException(status_code=404, detail="작업을 찾을 수 없습니다.")
