import { createRoot } from "react-dom/client";
import { FormEvent, useEffect, useState } from "react";
import "./styles.css";

const apiBase = import.meta.env.VITE_API_BASE_URL ?? "/api/v1";

type User = { username: string; role: string };

async function request<T>(path: string, init: RequestInit = {}, token?: string): Promise<T> {
  const response = await fetch(`${apiBase}${path}`, {
    ...init,
    headers: { "Content-Type": "application/json", ...(token ? { Authorization: `Bearer ${token}` } : {}), ...init.headers },
  });
  if (!response.ok) throw new Error(response.status === 401 ? "Неверные учётные данные" : "Не удалось выполнить запрос");
  return response.json() as Promise<T>;
}

function Login({ onAuthenticated }: { onAuthenticated: (token: string) => void }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function submit(event: FormEvent) {
    event.preventDefault();
    setLoading(true); setError("");
    try {
      const result = await request<{ access_token: string }>("/auth/login", { method: "POST", body: JSON.stringify({ username, password }) });
      localStorage.setItem("vpn-panel-token", result.access_token);
      onAuthenticated(result.access_token);
    } catch (cause) { setError(cause instanceof Error ? cause.message : "Ошибка входа"); }
    finally { setLoading(false); }
  }

  return <main className="login-shell"><form className="login-card" onSubmit={submit}>
    <span className="eyebrow">VPN PANEL</span><h1>Добро пожаловать</h1><p>Войдите, чтобы управлять инфраструктурой.</p>
    <label>Логин<input value={username} onChange={e => setUsername(e.target.value)} minLength={3} required autoComplete="username" /></label>
    <label>Пароль<input value={password} onChange={e => setPassword(e.target.value)} type="password" minLength={8} required autoComplete="current-password" /></label>
    {error && <p className="form-error" role="alert">{error}</p>}
    <button disabled={loading}>{loading ? "Выполняется вход…" : "Войти"}</button>
  </form></main>;
}

function Dashboard({ user, onLogout }: { user: User; onLogout: () => void }) {
  const [health, setHealth] = useState("Проверяем");
  useEffect(() => { request<{ status: string }>("/health").then(() => setHealth("Работает")).catch(() => setHealth("Недоступен")); }, []);
  return <main className="dashboard-shell"><aside><div className="brand">VPN Panel</div><nav><a className="active">Обзор</a><a>Серверы</a><a>Клиенты</a><a>Мониторинг</a><a>Аудит</a></nav><button className="secondary" onClick={onLogout}>Выйти</button></aside>
    <section className="dashboard"><header><div><span className="eyebrow">ПАНЕЛЬ УПРАВЛЕНИЯ</span><h1>Здравствуйте, {user.username}</h1></div><span className="role">{user.role}</span></header>
      <div className="metric-grid"><article><span>API</span><strong>{health}</strong><small>Backend и база данных</small></article><article><span>VPN-серверы</span><strong>0</strong><small>Добавьте первый сервер</small></article><article><span>Клиенты</span><strong>0</strong><small>Нет активных подключений</small></article></div>
      <article className="empty-state"><h2>Инфраструктура готова к настройке</h2><p>Подключите HostAgent и добавьте первый VPN-сервер, чтобы начать управление клиентами.</p><button>Добавить сервер</button></article>
    </section></main>;
}

function App() {
  const [token, setToken] = useState(() => localStorage.getItem("vpn-panel-token"));
  const [user, setUser] = useState<User | null>(null);
  useEffect(() => { if (token) request<User>("/users/me", {}, token).then(setUser).catch(() => setToken(null)); }, [token]);
  if (!token || !user) return <Login onAuthenticated={setToken} />;
  return <Dashboard user={user} onLogout={() => { localStorage.removeItem("vpn-panel-token"); setToken(null); }} />;
}

createRoot(document.getElementById("root")!).render(<App />);
