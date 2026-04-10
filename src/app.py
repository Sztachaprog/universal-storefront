from flask import Flask, request, jsonify, render_template_string
from src.application import register_user, get_user_by_name, upgrade_user_to_premium
import bcrypt

app = Flask(__name__)

LOGIN_PAGE = """
<!DOCTYPE html>
<html>
<head><title>Storefront</title></head>
<body>
    <h2>Login</h2>
    <form method="POST" action="/login">
        <input type="text" name="username" placeholder="Username" required><br><br>
        <input type="password" name="password" placeholder="Password" required><br><br>
        <button type="submit">Login</button>
    </form>
    <p><a href="/register">Register</a></p>
</body>
</html>
"""

REGISTER_PAGE = """
<!DOCTYPE html>
<html>
<head><title>Register</title></head>
<body>
    <h2>Register</h2>
    <form method="POST" action="/register">
        <input type="text" name="username" placeholder="Username" required><br><br>
        <input type="password" name="password" placeholder="Password" required><br><br>
        <input type="email" name="email" placeholder="Email" required><br><br>
        <button type="submit">Register</button>
    </form>
    <p><a href="/">Login</a></p>
</body>
</html>
"""

DASHBOARD_PAGE = """
<!DOCTYPE html>
<html>
<head><title>Dashboard</title></head>
<body>
    <h2>Welcome, {username}!</h2>
    <p>Premium status: {is_premium}</p>
    {% if not is_premium %}
    <form method="POST" action="/upgrade">
        <input type="hidden" name="user_id" value="{user_id}">
        <button type="submit">Upgrade to Premium</button>
    </form>
    {% else %}
    <p id="premium-status">You are a Premium member!</p>
    {% endif %}
    <p><a href="/">Logout</a></p>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(LOGIN_PAGE)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        email = request.form["email"]
        try:
            register_user(username, password, email)
            return '<p id="register-success">Registration successful! <a href="/">Login</a></p>'
        except Exception as e:
            return f'<p id="register-error">Error: {e}</p>'
    return render_template_string(REGISTER_PAGE)

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    user = get_user_by_name(username)
    if user is None:
        return '<p id="login-error">User not found</p>'
    from src.application import get_user_password_hash
    stored_hash = get_user_password_hash(user[0])
    if bcrypt.checkpw(password.encode("utf-8"), stored_hash.encode("utf-8")):
        return render_template_string(
            DASHBOARD_PAGE,
            username=user[1],
            is_premium=user[3],
            user_id=user[0]
        )
    return '<p id="login-error">Invalid password</p>'

@app.route("/upgrade", methods=["POST"])
def upgrade():
    user_id = request.form["user_id"]
    upgrade_user_to_premium(user_id)
    return '<p id="upgrade-success">Upgrade successful! You are now a Premium member.</p>'

if __name__ == "__main__":
    app.run(debug=True, port=5000)