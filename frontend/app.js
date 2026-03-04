// frontend/app.js
const API = "";  // same origin

let token = localStorage.getItem("token") || null;

const $ = id => document.getElementById(id);

function setView(view) {
  ["auth-view", "tasks-view"].forEach(v => $(v).classList.add("hidden"));
  $(`${view}-view`).classList.remove("hidden");
}

async function api(method, path, body) {
  const headers = { "Content-Type": "application/json" };
  if (token) headers["Authorization"] = `Bearer ${token}`;
  const resp = await fetch(API + path, { method, headers, body: body ? JSON.stringify(body) : undefined });
  if (resp.status === 204) return null;
  return resp.json().then(data => ({ status: resp.status, data }));
}

async function loadTasks() {
  const r = await api("GET", "/api/tasks");
  if (r.status !== 200) return logout();
  renderTasks(r.data);
}

function renderTasks(tasks) {
  const list = $("task-list");
  list.innerHTML = "";
  tasks.forEach(t => {
    const div = document.createElement("div");
    div.className = "task-item";
    div.innerHTML = `
      <input type="checkbox" ${t.done ? "checked" : ""} data-id="${t.id}">
      <span class="task-title ${t.done ? "done" : ""}">${t.title}</span>
      <button class="btn-danger" style="padding:.3rem .7rem;font-size:.8rem" data-del="${t.id}">✕</button>
    `;
    div.querySelector("[data-id]").addEventListener("change", async e => {
      await api("PATCH", `/api/tasks/${t.id}`, { done: e.target.checked });
      loadTasks();
    });
    div.querySelector("[data-del]").addEventListener("click", async () => {
      await api("DELETE", `/api/tasks/${t.id}`);
      loadTasks();
    });
    list.appendChild(div);
  });
}

$("login-btn").addEventListener("click", async () => {
  const email = $("email").value, password = $("password").value;
  const r = await api("POST", "/api/auth/login", { email, password });
  if (r.status === 200) { token = r.data.token; localStorage.setItem("token", token); setView("tasks"); loadTasks(); }
  else $("auth-error").textContent = r.data.detail || "Login failed";
});

$("register-btn").addEventListener("click", async () => {
  const email = $("email").value, password = $("password").value;
  const r = await api("POST", "/api/auth/register", { email, password });
  if (r.status === 201) { token = r.data.token; localStorage.setItem("token", token); setView("tasks"); loadTasks(); }
  else $("auth-error").textContent = r.data.detail || "Registration failed";
});

$("logout-btn").addEventListener("click", async () => {
  await api("POST", "/api/auth/logout");
  logout();
});

function logout() {
  token = null; localStorage.removeItem("token"); setView("auth");
}

$("add-btn").addEventListener("click", async () => {
  const title = $("new-task").value.trim();
  if (!title) return;
  await api("POST", "/api/tasks", { title });
  $("new-task").value = "";
  loadTasks();
});

$("new-task").addEventListener("keydown", e => { if (e.key === "Enter") $("add-btn").click(); });

// Init
if (token) { setView("tasks"); loadTasks(); }
else setView("auth");
