import React, { useState } from "react";
import { createRoot } from "react-dom/client";

const seed = [
  { id: 1, title: "첫 프로젝트", body: "목록과 상세 화면 예제입니다." },
  { id: 2, title: "두 번째 프로젝트", body: "상태 변경을 확인합니다." },
];

function App() {
  const [route, setRoute] = useState("list");
  const [items, setItems] = useState(seed);
  const [selectedId, setSelectedId] = useState(1);
  const [title, setTitle] = useState("");

  const selected = items.find((item) => item.id === selectedId);

  function addItem(event) {
    event.preventDefault();
    if (!title.trim()) return;
    setItems([...items, { id: Date.now(), title, body: "새로 등록한 항목입니다." }]);
    setTitle("");
    setRoute("list");
  }

  return (
    <main>
      <h1>React SPA 예제</h1>
      <nav>
        <button onClick={() => setRoute("list")}>목록</button>
        <button onClick={() => setRoute("new")}>등록</button>
      </nav>

      {route === "list" && (
        <ul>
          {items.map((item) => (
            <li key={item.id}>
              <button onClick={() => { setSelectedId(item.id); setRoute("detail"); }}>
                {item.title}
              </button>
            </li>
          ))}
        </ul>
      )}

      {route === "detail" && selected && (
        <section>
          <h2>{selected.title}</h2>
          <p>{selected.body}</p>
        </section>
      )}

      {route === "new" && (
        <form onSubmit={addItem}>
          <input value={title} onChange={(event) => setTitle(event.target.value)} placeholder="제목" />
          <button>저장</button>
        </form>
      )}
    </main>
  );
}

createRoot(document.getElementById("root")).render(<App />);
