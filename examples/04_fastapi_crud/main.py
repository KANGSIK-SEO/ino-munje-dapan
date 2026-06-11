from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, RedirectResponse

app = FastAPI()
MEMOS = []
NEXT_ID = 1


@app.get("/", response_class=HTMLResponse)
def home():
    return "<h1>메모 앱</h1><a href='/memos'>메모 목록</a> <a href='/memos/new'>새 메모</a>"


@app.get("/memos", response_class=HTMLResponse)
def list_memos():
    rows = "".join(f"<li><a href='/memos/{m['id']}'>{m['title']}</a></li>" for m in MEMOS)
    return f"<h1>메모 목록</h1><ul>{rows}</ul><a href='/memos/new'>새 메모</a>"


@app.get("/memos/new", response_class=HTMLResponse)
def new_memo():
    return """
    <h1>새 메모</h1>
    <form method="post" action="/memos">
      <input name="title" placeholder="제목">
      <textarea name="content" placeholder="내용"></textarea>
      <button>저장</button>
    </form>
    """


@app.post("/memos")
def create_memo(title: str = Form(), content: str = Form()):
    global NEXT_ID
    MEMOS.append({"id": NEXT_ID, "title": title, "content": content})
    NEXT_ID += 1
    return RedirectResponse("/memos", status_code=303)


@app.get("/memos/{memo_id}", response_class=HTMLResponse)
def detail_memo(memo_id: int):
    memo = next((m for m in MEMOS if m["id"] == memo_id), None)
    if not memo:
        return "<h1>메모 없음</h1>"
    return f"""
    <h1>{memo['title']}</h1>
    <p>{memo['content']}</p>
    <a href="/memos/{memo_id}/edit">수정</a>
    <form method="post" action="/memos/{memo_id}/delete"><button>삭제</button></form>
    """


@app.get("/memos/{memo_id}/edit", response_class=HTMLResponse)
def edit_memo(memo_id: int):
    memo = next((m for m in MEMOS if m["id"] == memo_id), None)
    if not memo:
        return "<h1>메모 없음</h1>"
    return f"""
    <h1>메모 수정</h1>
    <form method="post">
      <input name="title" value="{memo['title']}">
      <textarea name="content">{memo['content']}</textarea>
      <button>수정</button>
    </form>
    """


@app.post("/memos/{memo_id}/edit")
def update_memo(memo_id: int, title: str = Form(), content: str = Form()):
    for memo in MEMOS:
        if memo["id"] == memo_id:
            memo["title"] = title
            memo["content"] = content
            break
    return RedirectResponse(f"/memos/{memo_id}", status_code=303)


@app.post("/memos/{memo_id}/delete")
def delete_memo(memo_id: int):
    MEMOS[:] = [m for m in MEMOS if m["id"] != memo_id]
    return RedirectResponse("/memos", status_code=303)
