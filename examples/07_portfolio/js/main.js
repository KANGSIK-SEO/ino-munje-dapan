const themeBtn = document.querySelector("#themeBtn");
const form = document.querySelector("#contactForm");
const repoList = document.querySelector("#repoList");
const savedTheme = localStorage.getItem("theme");

if (savedTheme) {
  document.documentElement.dataset.theme = savedTheme;
}

themeBtn.addEventListener("click", () => {
  const next = document.documentElement.dataset.theme === "dark" ? "light" : "dark";
  document.documentElement.dataset.theme = next;
  localStorage.setItem("theme", next);
});

form.addEventListener("submit", (event) => {
  event.preventDefault();
  const email = document.querySelector("#email").value;
  const message = document.querySelector("#message").value;
  document.querySelector("#formResult").textContent =
    email && message ? "메시지 형식이 확인되었습니다." : "입력값을 확인하세요.";
});

async function loadRepos() {
  try {
    const response = await fetch("https://api.github.com/users/KANGSIK-SEO/repos");
    const repos = await response.json();
    repoList.innerHTML = repos.slice(0, 6).map((repo) =>
      `<article class="repo"><h3>${repo.name}</h3><a href="${repo.html_url}">보기</a></article>`
    ).join("");
  } catch (error) {
    repoList.textContent = "프로젝트를 불러오지 못했습니다.";
  }
}

loadRepos();
