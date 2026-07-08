import os
from flask import Flask, render_template, request, redirect, session, url_for, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from db import get_db_connection

app = Flask(__name__)
app.secret_key = os.environ.get(
    "FLASK_SECRET_KEY",
    "gujju_games_secret_key"
)

# ============================================
# PRODUCTION CONFIGURATION
# ============================================

app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['PERMANENT_SESSION_LIFETIME'] = 86400  # 24 hours

# ============================================
# HOME
# ============================================

@app.route("/")
def home():
    return redirect(url_for("index"))


# ============================================
# REGISTRATION
# ============================================

@app.route("/registration", methods=["GET", "POST"])
def registration():

    if request.method == "POST":

        username = request.form["Username"]
        email = request.form["Email"]
        phone = request.form["Phone_Number"]
        password = request.form["Password"]
        confirm = request.form["Confirm_password"]

        if password != confirm:
            return "Passwords do not match"

        hashed_password = generate_password_hash(password)

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT * FROM users
            WHERE Username=%s OR Email=%s
            """,
            (username, email)
        )

        existing = cursor.fetchone()

        if existing:
            cursor.close()
            conn.close()
            return "User already exists"

        cursor.execute(
            """
            INSERT INTO users
            (Username, Email, Phone_Number, Password)
            VALUES (%s,%s,%s,%s)
            """,
            (
                username,
                email,
                phone,
                hashed_password
            )
        )

        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for("login"))

    return render_template("registration.html")


# ============================================
# LOGIN
# ============================================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["Username"]
        password = request.form["Password"]

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # ---------------- ADMIN LOGIN ----------------

        cursor.execute(
            """
            SELECT * FROM admins
            WHERE Username=%s
            """,
            (username,)
        )

        admin = cursor.fetchone()

        if admin:

            valid = admin["Password"] == password

            if valid:

                session.clear()
                session["admin_username"] = admin["Username"]

                cursor.close()
                conn.close()

                return redirect(
                    url_for("admin_dashboard")
                )

            cursor.close()
            conn.close()

            return "Admin password incorrect"

        # ---------------- USER LOGIN ----------------

        cursor.execute(
            """
            SELECT * FROM users
            WHERE Username=%s
            """,
            (username,)
        )

        user = cursor.fetchone()

        if not user:
            cursor.close()
            conn.close()
            return "User not found"

        valid = False

        try:
            valid = check_password_hash(
                user["Password"],
                password
            )
        except:
            if user["Password"] == password:
                valid = True

        if valid:

            session.clear()
            session["Username"] = user["Username"]

            cursor.close()
            conn.close()

            return redirect(url_for("dashboard"))

        cursor.close()
        conn.close()

        return "Password incorrect"

    return render_template("login.html")


# ============================================
# DASHBOARD / INDEX
# ============================================

@app.route("/dashboard")
@app.route("/index")
def index():

    username = session.get("Username")

    total_games = 0
    high_score = 0
    game_stats = {}

    if username:

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # total matches played
        cursor.execute(
            """
            SELECT COUNT(*) AS total
            FROM history
            WHERE username=%s
            """,
            (username,)
        )

        total_games = cursor.fetchone()["total"]

        # highest score overall
        cursor.execute(
            """
            SELECT MAX(score) AS max_score
            FROM history
            WHERE username=%s
            """,
            (username,)
        )

        result = cursor.fetchone()

        if result["max_score"]:
            high_score = result["max_score"]

        # stats per game
        cursor.execute(
            """
            SELECT
                game_name,
                MAX(score) AS best_score,
                COUNT(*) AS played

            FROM history

            WHERE username=%s

            GROUP BY game_name
            """,
            (username,)
        )

        rows = cursor.fetchall()

        for row in rows:

            game_stats[row["game_name"]] = {

                "best": row["best_score"],

                "played": row["played"]
            }

        cursor.close()
        conn.close()

    return render_template(

        "index.html",

        Username=username,

        total_games=total_games,

        high_score=high_score,

        game_stats=game_stats
    )


# ============================================
# PROFILE
# ============================================

@app.route("/profile", methods=["GET", "POST"])
def profile():

    if "Username" not in session:
        return redirect(url_for("login"))

    current_username = session["Username"]

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == "POST":

        new_username = request.form["Username"]
        email = request.form["Email"]
        phone = request.form["Phone_Number"]

        # update users table
        cursor.execute(
            """
            UPDATE users
            SET Username=%s,
                Email=%s,
                Phone_Number=%s
            WHERE Username=%s
            """,
            (
                new_username,
                email,
                phone,
                current_username
            )
        )

        # update leaderboard
        cursor.execute(
            """
            UPDATE leaderboard
            SET Username=%s
            WHERE Username=%s
            """,
            (
                new_username,
                current_username
            )
        )

        # update history
        cursor.execute(
            """
            UPDATE history
            SET username=%s
            WHERE username=%s
            """,
            (
                new_username,
                current_username
            )
        )

        conn.commit()

        session["Username"] = new_username

    cursor.execute(
        """
        SELECT * FROM users
        WHERE Username=%s
        """,
        (session["Username"],)
    )

    user = cursor.fetchone()

    cursor.close()
    conn.close()

    return render_template(
        "user_profile.html",
        user=user
    )
# ============================================
# GAME ROUTES
# ============================================

@app.route("/tic-tac-toe")
def tic_tac_toe():
    return render_template("tic_tac_toe.html")


@app.route("/brick-breaker")
def brick_breaker():
    return render_template("brick_n_ball.html")


@app.route("/snake")
def snake():
    return render_template("snake_apple.html")


@app.route("/space-shooter")
def space_shooter():
    return render_template("space_shooter.html")


@app.route("/flappy-bird")
def flappy_bird():
    return render_template("flappy_bird.html")


@app.route("/car")
def car_game():
    return render_template("car.html")


# ============================================
# SAVE MATCH HISTORY
# ============================================

@app.route("/save_history", methods=["POST"])
def save_history():

    if "Username" not in session:
        return jsonify({
            "success": False,
            "message": "Login required"
        }), 401

    game_name = request.form.get("game_name")
    result = request.form.get("result")
    score = request.form.get("score", 0)

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO history
        (username, game_name, result, score)

        VALUES (%s,%s,%s,%s)
        """,
        (
            session["Username"],
            game_name,
            result,
            score
        )
    )

    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({
        "success": True,
        "message": "History saved"
    })


# ============================================
# SAVE SCORE → LEADERBOARD
# BEST SCORE ONLY
# ============================================

@app.route("/save-score", methods=["POST"])
def save_score():

    if "Username" not in session:
        return jsonify({
            "success": False,
            "message": "Please login first"
        }), 401

    data = request.get_json()

    game_name = data.get("game_name")
    score = int(data.get("score", 0))

    if not game_name:
        return jsonify({
            "success": False,
            "message": "Game name missing"
        }), 400

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # check existing score
    cursor.execute(
        """
        SELECT * FROM leaderboard
        WHERE Username=%s
        AND game_name=%s
        """,
        (
            session["Username"],
            game_name
        )
    )

    existing = cursor.fetchone()

    # no old score → insert
    if not existing:

        cursor.execute(
            """
            INSERT INTO leaderboard
            (Username, game_name, score)

            VALUES (%s,%s,%s)
            """,
            (
                session["Username"],
                game_name,
                score
            )
        )

    else:

        old_score = existing["score"]

        # update only if new score bigger
        if score > old_score:

            cursor.execute(
                """
                UPDATE leaderboard
                SET score=%s,
                    played_at=CURRENT_TIMESTAMP

                WHERE Username=%s
                AND game_name=%s
                """,
                (
                    score,
                    session["Username"],
                    game_name
                )
            )

    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({
        "success": True,
        "message": "Score updated"
    })


# ============================================
# HISTORY PAGE
# ============================================

@app.route("/history")
def history():

    if "Username" not in session:
        return redirect(url_for("login"))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT *

        FROM history

        WHERE username=%s

        ORDER BY played_at DESC
        """,
        (session["Username"],)
    )

    history_data = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "history.html",
        history=history_data
    )


# ============================================
# LEADERBOARD PAGE
# TOP 10 PLAYERS
# ============================================

@app.route("/leaderboard")
def leaderboard():

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT
            Username,
            game_name,
            score,
            played_at

        FROM leaderboard

        ORDER BY score DESC

        LIMIT 10
        """
    )

    leaders = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "leaderboard.html",
        leaders=leaders
    )
# ============================================
# ADMIN DASHBOARD
# ============================================

@app.route("/admin_dashboard")
def admin_dashboard():

    if "admin_username" not in session:
        return redirect(url_for("login"))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # all users
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    total_users = len(users)

    # total games played
    cursor.execute("""
        SELECT COUNT(*) AS total_games
        FROM history
    """)
    total_games = cursor.fetchone()["total_games"]

    # active users
    cursor.execute("""
        SELECT COUNT(DISTINCT username)
        AS active_users
        FROM history
    """)
    active_users = cursor.fetchone()["active_users"]

    # game types
    cursor.execute("""
        SELECT COUNT(DISTINCT game_name)
        AS game_types
        FROM history
    """)
    game_types = cursor.fetchone()["game_types"]

    # game stats
    cursor.execute("""
        SELECT
            game_name,
            COUNT(*) AS plays,
            AVG(score) AS avg_score,
            MAX(score) AS best_score

        FROM history

        GROUP BY game_name

        ORDER BY plays DESC
    """)
    game_stats = cursor.fetchall()

    # top players
    cursor.execute("""
        SELECT
            username,
            COUNT(*) AS matches_played,
            SUM(score) AS total_score,
            AVG(score) AS avg_score

        FROM history

        GROUP BY username

        ORDER BY total_score DESC

        LIMIT 6
    """)
    top_players = cursor.fetchall()

    # games list
    cursor.execute("SELECT * FROM games")
    admin_games = cursor.fetchall()

    # recent history
    cursor.execute("""
        SELECT
            username,
            game_name,
            result,
            score,
            played_at

        FROM history

        ORDER BY played_at DESC

        LIMIT 8
    """)
    recent_history = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "admin_dashboard.html",

        users=users,

        total_users=total_users,

        total_games=total_games,

        active_users=active_users,

        game_types=game_types,

        game_stats=game_stats,

        top_players=top_players,

        recent_history=recent_history,

        admin_games=admin_games,

        admin_username=session["admin_username"]
    )


# ============================================
# UPDATE GAME
# ============================================

@app.route("/admin/update-game/<int:game_id>", methods=["POST"])
def update_game(game_id):

    if "admin_username" not in session:
        return redirect(url_for("login"))

    name = request.form.get("name")
    category = request.form.get("category")
    status = request.form.get("status")
    route = request.form.get("route")
    icon = request.form.get("icon")

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE games
        SET
            game_name=%s,
            description=%s,
            status=%s,
            route=%s,
            icon=%s
        WHERE id=%s
    """, (
        name,
        category,
        status,
        route,
        icon,
        game_id
    ))

    conn.commit()

    cursor.close()
    conn.close()

    return redirect(url_for("admin_dashboard"))


# ============================================
# ADD GAME
# ============================================

@app.route("/add_game", methods=["POST"])
def add_game():

    if "admin_username" not in session:
        return redirect(url_for("login"))

    game_name = request.form.get("game_name")
    description = request.form.get("description")
    icon = request.form.get("icon")
    route = request.form.get("route")
    status = request.form.get("status", "Active")

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO games
        (game_name, description, icon, route, status)

        VALUES (%s,%s,%s,%s,%s)
    """, (
        game_name,
        description,
        icon,
        route,
        status
    ))

    conn.commit()

    cursor.close()
    conn.close()

    return redirect(url_for("admin_dashboard"))


# ============================================
# EDIT GAME
# ============================================

@app.route("/edit_game", methods=["POST"])
def edit_game():

    if "admin_username" not in session:
        return redirect(url_for("login"))

    game_id = request.form.get("game_id")
    game_name = request.form.get("game_name")
    description = request.form.get("description")
    icon = request.form.get("icon")
    route = request.form.get("route")
    status = request.form.get("status")

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE games
        SET
            game_name=%s,
            description=%s,
            icon=%s,
            route=%s,
            status=%s

        WHERE id=%s
    """, (
        game_name,
        description,
        icon,
        route,
        status,
        game_id
    ))

    conn.commit()

    cursor.close()
    conn.close()

    return redirect(url_for("admin_dashboard"))


# ============================================
# DELETE GAME
# ============================================

@app.route("/delete_game/<int:game_id>")
def delete_game(game_id):

    if "admin_username" not in session:
        return redirect(url_for("login"))

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM games WHERE id=%s",
        (game_id,)
    )

    conn.commit()

    cursor.close()
    conn.close()

    return redirect(url_for("admin_dashboard"))


# ============================================
# DELETE USER
# ============================================

@app.route("/admin/delete-user/<int:user_id>")
def delete_user(user_id):

    if "admin_username" not in session:
        return redirect(url_for("login"))

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM users WHERE id=%s",
        (user_id,)
    )

    conn.commit()

    cursor.close()
    conn.close()

    return redirect(url_for("admin_dashboard"))


# ============================================
# API: GET USER STATS (FOR LIVE UPDATES)
# ============================================

@app.route("/api/user-stats")
def api_user_stats():
    """
    API endpoint for live dashboard stats updates.
    Returns user's total games and high score in JSON format.
    """
    
    username = session.get("Username")
    
    total_games = 0
    high_score = 0
    
    if username:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # total matches played
        cursor.execute(
            """
            SELECT COUNT(*) AS total
            FROM history
            WHERE username=%s
            """,
            (username,)
        )
        
        total_games = cursor.fetchone()["total"]
        
        # highest score overall
        cursor.execute(
            """
            SELECT MAX(score) AS max_score
            FROM history
            WHERE username=%s
            """,
            (username,)
        )
        
        result = cursor.fetchone()
        
        if result["max_score"]:
            high_score = result["max_score"]
        
        cursor.close()
        conn.close()
        
        return jsonify({
            "success": True,
            "total_games": total_games,
            "high_score": high_score
        })
    
    # Guest user
    return jsonify({
        "success": False,
        "message": "Not logged in",
        "total_games": 0,
        "high_score": 0
    })


# ============================================
# LOGOUT
# ============================================

@app.route("/logout")
def logout():

    session.clear()

    return redirect(
        url_for("login")
    )


# ============================================
# RUN APP
# ============================================

if __name__ == "__main__":
    # Production: Use gunicorn (handled by Procfile)
    # Local development: Run with debug enabled
    debug_mode = os.environ.get("FLASK_ENV") != "production"
    port = int(os.environ.get("PORT", 5000))
    app.run(
        host="0.0.0.0",
        port=port,
        debug=debug_mode
    )