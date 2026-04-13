from flask import Flask, request, render_template_string
from src.application import register_user, get_user_by_name, upgrade_user_to_premium, get_user_password_hash
import bcrypt

app = Flask(__name__)

BASE_STYLE = """
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

:root {
    --bg: #0a0a0f;
    --surface: #111118;
    --border: #1e1e2e;
    --accent: #c8ff00;
    --accent-dim: rgba(200,255,0,0.1);
    --text: #e8e8f0;
    --muted: #555570;
    --error: #ff4444;
    --success: #00ff88;
}

body {
    background: var(--bg);
    color: var(--text);
    font-family: 'DM Mono', monospace;
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 2rem;
}

body::before {
    content: '';
    position: fixed;
    inset: 0;
    background: radial-gradient(ellipse 80% 60% at 50% -10%, rgba(200,255,0,0.07), transparent);
    pointer-events: none;
}

.card {
    background: var(--surface);
    border: 1px solid var(--border);
    padding: 3rem;
    width: 100%;
    max-width: 420px;
    position: relative;
    animation: slideUp 0.4s ease;
}

.card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: var(--accent);
}

@keyframes slideUp {
    from { opacity: 0; transform: translateY(16px); }
    to { opacity: 1; transform: translateY(0); }
}

.logo {
    font-family: 'Syne', sans-serif;
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 0.3em;
    text-transform: uppercase;
    color: var(--accent);
    margin-bottom: 2.5rem;
}

h1 {
    font-family: 'Syne', sans-serif;
    font-size: 2rem;
    font-weight: 800;
    line-height: 1.1;
    margin-bottom: 0.5rem;
    color: var(--text);
}

.subtitle {
    font-size: 0.75rem;
    color: var(--muted);
    margin-bottom: 2rem;
    letter-spacing: 0.05em;
}

.field {
    margin-bottom: 1rem;
}

label {
    display: block;
    font-size: 0.65rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 0.4rem;
}

input {
    width: 100%;
    background: var(--bg);
    border: 1px solid var(--border);
    color: var(--text);
    font-family: 'DM Mono', monospace;
    font-size: 0.875rem;
    padding: 0.75rem 1rem;
    outline: none;
    transition: border-color 0.2s;
}

input:focus {
    border-color: var(--accent);
}

button {
    width: 100%;
    background: var(--accent);
    color: #0a0a0f;
    border: none;
    font-family: 'Syne', sans-serif;
    font-size: 0.8rem;
    font-weight: 700;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    padding: 0.875rem;
    cursor: pointer;
    margin-top: 1.5rem;
    transition: opacity 0.2s, transform 0.1s;
}

button:hover { opacity: 0.85; }
button:active { transform: scale(0.99); }

button.secondary {
    background: transparent;
    color: var(--accent);
    border: 1px solid var(--accent);
    margin-top: 0.75rem;
}

.link {
    display: block;
    text-align: center;
    margin-top: 1.5rem;
    font-size: 0.75rem;
    color: var(--muted);
    text-decoration: none;
    letter-spacing: 0.05em;
}

.link a { color: var(--accent); text-decoration: none; }
.link a:hover { text-decoration: underline; }

.alert {
    padding: 0.75rem 1rem;
    font-size: 0.75rem;
    margin-bottom: 1.5rem;
    border-left: 3px solid;
}

.alert.error { background: rgba(255,68,68,0.08); border-color: var(--error); color: var(--error); }
.alert.success { background: rgba(0,255,136,0.08); border-color: var(--success); color: var(--success); }

.status-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    font-size: 0.7rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    padding: 0.3rem 0.75rem;
    margin-bottom: 2rem;
}

.status-badge.active {
    background: rgba(0,255,136,0.1);
    color: var(--success);
    border: 1px solid rgba(0,255,136,0.3);
}

.status-badge.inactive {
    background: rgba(85,85,112,0.2);
    color: var(--muted);
    border: 1px solid var(--border);
}

.status-badge::before {
    content: '';
    width: 6px; height: 6px;
    border-radius: 50%;
    background: currentColor;
}

.divider {
    border: none;
    border-top: 1px solid var(--border);
    margin: 2rem 0;
}

.welcome-name {
    color: var(--accent);
}

.dashboard-card {
    max-width: 480px;
}
"""

LOGIN_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Storefront — Login</title>
<style>""" + BASE_STYLE + """</style>
</head>
<body>
<div class="card">
    <div class="logo">Universal Storefront</div>
    <h1>Sign<br>in.</h1>
    <p class="subtitle">Access your account</p>
    {% if error %}
    <div class="alert error" id="login-error">{{ error }}</div>
    {% endif %}
    <form method="POST" action="/login">
        <div class="field">
            <label>Username</label>
            <input type="text" name="username" placeholder="your_username" required>
        </div>
        <div class="field">
            <label>Password</label>
            <input type="password" name="password" placeholder="••••••••" required>
        </div>
        <button type="submit">Continue →</button>
    </form>
    <p class="link">No account? <a href="/register">Register here</a></p>
</div>
</body>
</html>
"""

REGISTER_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Storefront — Register</title>
<style>""" + BASE_STYLE + """</style>
</head>
<body>
<div class="card">
    <div class="logo">Universal Storefront</div>
    <h1>Create<br>account.</h1>
    <p class="subtitle">Join the platform</p>
    {% if error %}
    <div class="alert error" id="register-error">{{ error }}</div>
    {% endif %}
    {% if success %}
    <div class="alert success" id="register-success">{{ success }}</div>
    {% endif %}
    <form method="POST" action="/register">
        <div class="field">
            <label>Username</label>
            <input type="text" name="username" placeholder="your_username" required>
        </div>
        <div class="field">
            <label>Password</label>
            <input type="password" name="password" placeholder="••••••••" required>
        </div>
        <div class="field">
            <label>Email</label>
            <input type="email" name="email" placeholder="you@example.com" required>
        </div>
        <button type="submit">Create Account →</button>
    </form>
    <p class="link">Already have an account? <a href="/">Sign in</a></p>
</div>
</body>
</html>
"""

DASHBOARD_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Storefront — Dashboard</title>
<style>""" + BASE_STYLE + """</style>
</head>
<body>
<div class="card dashboard-card">
    <div class="logo">Universal Storefront</div>
    <h1>Welcome,<br><span class="welcome-name">{{ username }}</span>.</h1>
    <hr class="divider">
    {% if is_premium %}
    <div class="status-badge active" id="premium-status">Premium Active</div>
    <p style="font-size:0.8rem; color: var(--muted);">You have full access to all content.</p>
    {% else %}
    <div class="status-badge inactive" id="premium-status">Standard Plan</div>
    <p style="font-size:0.8rem; color: var(--muted); margin-bottom: 1.5rem;">Upgrade to unlock all premium content.</p>
    <form method="POST" action="/upgrade">
        <input type="hidden" name="user_id" value="{{ user_id }}">
        <button type="submit" id="upgrade-btn">Upgrade to Premium →</button>
    </form>
    {% endif %}
    <a href="/" class="link" style="margin-top:2rem;">← Sign out</a>
</div>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(LOGIN_PAGE, error=None)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        email = request.form["email"]
        try:
            register_user(username, password, email)
            return render_template_string(REGISTER_PAGE, error=None, success="Registration successful! You can now sign in.")
        except Exception as e:
            return render_template_string(REGISTER_PAGE, error=str(e), success=None)
    return render_template_string(REGISTER_PAGE, error=None, success=None)

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    user = get_user_by_name(username)
    if user is None:
        return render_template_string(LOGIN_PAGE, error="User not found.")
    stored_hash = get_user_password_hash(user[0])
    if bcrypt.checkpw(password.encode("utf-8"), stored_hash.encode("utf-8")):
        return render_template_string(DASHBOARD_PAGE, username=user[1], is_premium=user[3], user_id=user[0])
    return render_template_string(LOGIN_PAGE, error="Invalid password.")

@app.route("/upgrade", methods=["POST"])
def upgrade():
    user_id = request.form["user_id"]
    upgrade_user_to_premium(user_id)
    return render_template_string(DASHBOARD_PAGE, username="user", is_premium=True, user_id=user_id)

if __name__ == "__main__":
    app.run(debug=True, port=5000)