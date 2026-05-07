from flask import Flask, request, render_template

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
import psycopg2

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("login.html")

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
                return render_template("dashboard.html", username=user[1], is_premium=user[3], user_id=user[0])
            return render_template("login.html", error="Wrong password", success=None)
                   
        except Exception as e:
            return f"login failed: {e}"
        finally:
            close_db_connection(conn, cursor)
    return render_template("login.html", error=None, success=None)


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
            user_id = request.form["user_id"]     
            is_premium = get_user_by_id(user_id, cursor=cursor)
            if is_premium[3] is True:
                return render_template("dashboard.html", error="already premium")              
            upgrade_user_to_premium(user_id, cursor=cursor)
            conn.commit()
            return render_template("dashboard.html", username="user", is_premium=True, user_id=user_id)
        except Exception as e:
            conn.rollback()
            return render_template("dashboard.html", error=str(e), success=None)
        finally:
            close_db_connection(conn, cursor)
    return render_template("dashboard.html", error=None, success=None)

if __name__ == "__main__":
    app.run(debug=True, port=5000)