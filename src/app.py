from flask import Flask, request, render_template, redirect, session, url_for, jsonify

from src.database.database import (
    get_db_connection,
    close_db_connection
)
from src.application import (
register_user, 
get_user_by_name, 
upgrade_user_to_premium, 
get_user_password_hash,
get_user_by_id
)
import bcrypt
import jwt

app = Flask(__name__)
app.secret_key = "dev-secret-key"


@app.route("/")
def home():
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if "username" in session:
        return render_template("dashboard.html", 
            username=session["username"],
            is_premium=session["is_premium"],
            user_id=session["user_id"]
        )
    else:
        return redirect(url_for("login")) # if fail change url for /login


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        conn = get_db_connection()
        cursor = conn.cursor()
        try: 
            username = request.form["username"] 
            password = request.form["password"] 
            user = get_user_by_name(username, cursor=cursor)
            if user is None:
                return render_template("login.html", error="User not found", success=None)       
            stored_hash = get_user_password_hash(user[0], cursor=cursor)
            
            if bcrypt.checkpw(password.encode("utf-8"), stored_hash.encode("utf-8")):
                session["username"] = user[1]
                session["user_id"] = user[0]
                session["is_premium"] = user[3]
                return redirect(url_for("dashboard"))
            return render_template("login.html", error="Wrong password", success=None)
                   
        except Exception as e:
            return f"login failed: {e}"
        finally:
            close_db_connection(conn, cursor)
    return render_template("login.html", error=None, success=None)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))
    
    
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            username = request.form["username"] 
            password = request.form["password"] 
            email = request.form["email"]
            register_user(username, password, email, cursor=cursor)
            conn.commit()
            return render_template("register.html", error=None, success="Succesfully registered")
        except Exception as e:
            conn.rollback()
            return render_template("register.html", error=str(e), success=None)
        finally:
            close_db_connection(conn, cursor)
    return render_template("register.html", error=None, success=None)
        
        

@app.route("/upgrade", methods=["POST"])
def upgrade():
    if request.method == "POST":
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            user_id = session["user_id"]   
            is_premium = get_user_by_id(user_id, cursor=cursor)
            if is_premium[3] is True:
                return render_template("dashboard.html", error="already premium")              
            upgrade_user_to_premium(user_id, cursor=cursor)
            conn.commit()
            session["is_premium"] = True
            return redirect(url_for("dashboard"))
        except Exception as e:
            conn.rollback()
            return render_template("dashboard.html", error=str(e), success=None)
        finally:
            close_db_connection(conn, cursor)
    return render_template("dashboard.html", error=None, success=None)

if __name__ == "__main__":
    app.run(debug=True, port=5000)



# API routes for tests purpose

@app.route("/api/users", methods=["POST"])
def post_user_api():
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        username = request.json["username"] 
        password = request.json["password"]
        email = request.json["email"]
        register_user(username, password, email, is_premium=False, cursor = cursor)
        conn.commit()
        return jsonify({"message": "created"}), 201
    except ValueError as e:                             # to dokładniej co to
        if "already exists" in str(e):                  # to tez 
            return jsonify({"error": str(e)}), 409
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
        
    finally:
        close_db_connection(conn, cursor)

@app.route("/api/users/<int:id>")
def get_user_api(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        user = get_user_by_id(id, cursor=cursor)
        if user is None:
            return jsonify({"error": "User not found"}), 404
        return jsonify({
            "id": user[0],
            "username": user[1],
            "email": user[2],
            "is_premium": user[3]
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        close_db_connection(conn, cursor)

@app.route("/api/login", methods=["POST"])
def post_login_api():
    conn = get_db_connection()
    cursor = conn.cursor()
    try: 
        username = request.json["username"] 
        password = request.json["password"] 
        user = get_user_by_name(username, cursor=cursor)
        if user is None:
            return jsonify({"error": "Invalid credentials"}), 401
        stored_hash = get_user_password_hash(user[0], cursor=cursor)
            
        if bcrypt.checkpw(password.encode("utf-8"), stored_hash.encode("utf-8")):
            payload = {"user_id": user[0]}
            token = jwt.encode(payload, app.secret_key, "HS256")
            return jsonify({"token": token}), 200
        return jsonify({"error": "Invalid credentials"}), 401
                   
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        close_db_connection(conn, cursor)
