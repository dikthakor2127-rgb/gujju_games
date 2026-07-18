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
    return redirect(url_for("dashboard"))


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
            (
                Username,
                Email,
                Phone_Number,
                Password,
                Confirm_password
            )

            VALUES
            (%s,%s,%s,%s,%s)
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
# =====================================================

@app.route("/login", methods=["GET", "POST"])
def login():

    # Already logged in
    if "Username" in session:
        return redirect(url_for("dashboard"))

    if "admin_username" in session:
        return redirect(url_for("admin_dashboard"))

    if request.method == "POST":

        username = request.form.get("Username", "").strip()
        password = request.form.get("Password", "")

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
                # ============================================
        # ADMIN LOGIN
        # ============================================

        cursor.execute(
            """
            SELECT *
            FROM admins
            WHERE Username=%s
            """,
            (username,)
        )

        admin = cursor.fetchone()

        if admin:

            valid = False

            try:
                valid = check_password_hash(
                    admin["Password"],
                    password
                )
            except Exception:
                valid = admin["Password"] == password

            if valid:

                session.clear()
                session["admin_username"] = admin["Username"]

                cursor.close()
                conn.close()

                return redirect(url_for("admin_dashboard"))

            cursor.close()
            conn.close()

            return "Admin password incorrect"

        # ============================================
        # USER LOGIN
        # ============================================

        cursor.execute(
            """
            SELECT *
            FROM users
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

        except Exception:

            valid = user["Password"] == password

        if not valid:

            cursor.close()
            conn.close()

            return "Password incorrect"

        session.clear()
        session["Username"] = user["Username"]

        cursor.close()
        conn.close()

        return redirect(url_for("dashboard"))

    return render_template("login.html")


# =====================================================
# USER DASHBOARD
# =====================================================

@app.route("/dashboard")
@app.route("/index")
def dashboard():

    if "Username" not in session:
        return redirect(url_for("login"))

    username = session["Username"]

    total_games = 0
    high_score = 0
    game_stats = {}

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Total Games Played
    cursor.execute(
        """
        SELECT COUNT(*) AS total
        FROM history
        WHERE username=%s
        """,
        (username,)
    )

    total_games = cursor.fetchone()["total"]

    # Highest Score
    cursor.execute(
        """
        SELECT MAX(score) AS max_score
        FROM history
        WHERE username=%s
        """,
        (username,)
    )

    result = cursor.fetchone()

    if result and result["max_score"] is not None:
        high_score = result["max_score"]

    # Per Game Statistics
    cursor.execute(
        """
        SELECT
            game_name,
            MAX(score) AS best_score,
            COUNT(*) AS played

        FROM history

        WHERE username=%s

        GROUP BY game_name

        ORDER BY game_name
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


# =====================================================
# PROFILE
# =====================================================

@app.route("/profile", methods=["GET", "POST"])
def profile():

    if "Username" not in session:
        return redirect(url_for("login"))

    current_username = session["Username"]

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == "POST":

        new_username = request.form.get("Username", "").strip()
        email = request.form.get("Email", "").strip()
        phone = request.form.get("Phone_Number", "").strip()

        if not new_username:
            new_username = current_username

        cursor.execute("""
            UPDATE users
            SET Username=%s,
                Email=%s,
                Phone_Number=%s
            WHERE Username=%s
        """, (
            new_username,
            email,
            phone,
            current_username
        ))

        cursor.execute("""
            UPDATE leaderboard
            SET Username=%s
            WHERE Username=%s
        """, (
            new_username,
            current_username
        ))

        cursor.execute("""
            UPDATE history
            SET username=%s
            WHERE username=%s
        """, (
            new_username,
            current_username
        ))

        conn.commit()

        session["Username"] = new_username
        current_username = new_username

    cursor.execute("""
        SELECT *
        FROM users
        WHERE Username=%s
    """, (current_username,))

    user = cursor.fetchone()

    cursor.close()
    conn.close()

    return render_template(
        "user_profile.html",
        user=user
    )
# ===========================================================
# GAME ROUTES
# ===========================================================

@app.route("/tic-tac-toe")
def tic_tac_toe():

    return render_template(
        "tic_tac_toe.html"
    )


@app.route("/brick-breaker")
def brick_breaker():

    return render_template(
        "brick_n_ball.html"
    )


@app.route("/snake")
def snake():

    return render_template(
        "snake_apple.html"
    )


@app.route("/space-shooter")
def space_shooter():

    return render_template(
        "space_shooter.html"
    )


@app.route("/flappy-bird")
def flappy_bird():

    return render_template(
        "flappy_bird.html"
    )


@app.route("/car")
def car_game():

    return render_template(
        "car.html"
    )
# ============================================
# SAVE MATCH HISTORY
# ============================================

@app.route("/save_history", methods=["POST"])
def save_history():

    if "Username" not in session:
        return jsonify({
            "success": False,
            "message": "Please login first."
        }), 401

    game_name = request.form.get("game_name", "").strip()
    result = request.form.get("result", "").strip()

    try:
        score = int(request.form.get("score", 0))
    except (TypeError, ValueError):
        score = 0

    if not game_name:
        return jsonify({
            "success": False,
            "message": "Game name is required."
        }), 400

    conn = None
    cursor = None

    try:

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO history
            (
                username,
                game_name,
                result,
                score
            )

            VALUES
            (%s,%s,%s,%s)
            """,
            (
                session["Username"],
                game_name,
                result,
                score
            )
        )

        conn.commit()

        return jsonify({
            "success": True,
            "message": "History saved successfully."
        })

    except Exception as e:

        if conn:
            conn.rollback()

        print("History Error:", e)

        return jsonify({
            "success": False,
            "message": "Unable to save history."
        }), 500

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()
            # ============================================
# SAVE SCORE → LEADERBOARD
# BEST SCORE ONLY
# ============================================

@app.route("/save-score", methods=["POST"])
def save_score():

    if "Username" not in session:
        return jsonify({
            "success": False,
            "message": "Please login first."
        }), 401

    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "success": False,
            "message": "Invalid request."
        }), 400

    game_name = data.get("game_name", "").strip()

    try:
        score = int(data.get("score", 0))
    except (TypeError, ValueError):
        score = 0

    if not game_name:
        return jsonify({
            "success": False,
            "message": "Game name missing."
        }), 400

    conn = None
    cursor = None

    try:

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Check existing leaderboard record

        cursor.execute(
            """
            SELECT score

            FROM leaderboard

            WHERE Username=%s
            AND game_name=%s
            """,
            (
                session["Username"],
                game_name
            )
        )

        existing = cursor.fetchone()

        # No existing score → Insert

        if existing is None:

            cursor.execute(
                """
                INSERT INTO leaderboard
                (
                    Username,
                    game_name,
                    score
                )

                VALUES
                (%s,%s,%s)
                """,
                (
                    session["Username"],
                    game_name,
                    score
                )
            )

        else:

            # Update only if score is higher

            if score > existing["score"]:

                cursor.execute(
                    """
                    UPDATE leaderboard

                    SET
                        score=%s,
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

        return jsonify({
            "success": True,
            "message": "Leaderboard updated."
        })

    except Exception as e:

        if conn:
            conn.rollback()

        print("Leaderboard Error:", e)

        return jsonify({
            "success": False,
            "message": "Unable to save score."
        }), 500

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()
            # ============================================
# HISTORY PAGE
# ============================================

@app.route("/history")
def history():

    if "Username" not in session:
        return redirect(url_for("login"))

    conn = None
    cursor = None

    try:

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                id,
                game_name,
                result,
                score,
                played_at

            FROM history

            WHERE username=%s

            ORDER BY played_at DESC
        """, (
            session["Username"],
        ))

        history_data = cursor.fetchall()

        return render_template(
            "history.html",
            history=history_data
        )

    except Exception as e:

        print("History Error:", e)

        return render_template(
            "history.html",
            history=[]
        )

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()


# ============================================
# LEADERBOARD PAGE
# ============================================

@app.route("/leaderboard")
def leaderboard():

    conn = None
    cursor = None

    try:

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                Username,
                game_name,
                score,
                played_at

            FROM leaderboard

            ORDER BY
                score DESC,
                played_at ASC

            LIMIT 10
        """)

        leaders = cursor.fetchall()

        return render_template(
            "leaderboard.html",
            leaders=leaders
        )

    except Exception as e:

        print("Leaderboard Error:", e)

        return render_template(
            "leaderboard.html",
            leaders=[]
        )

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()


# ============================================
# ADMIN DASHBOARD
# ============================================

@app.route("/admin_dashboard")
def admin_dashboard():

    if "admin_username" not in session:
        return redirect(url_for("login"))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Total Users
    cursor.execute("SELECT COUNT(*) AS total_users FROM users")
    total_users = cursor.fetchone()["total_users"]

    # Total Matches
    cursor.execute("SELECT COUNT(*) AS total_games FROM history")
    total_games = cursor.fetchone()["total_games"]

    # Active Users
    cursor.execute("""
        SELECT COUNT(DISTINCT username)
        AS active_users
        FROM history
    """)
    active_users = cursor.fetchone()["active_users"]
        # ============================================
    # GAME TYPES
    # ============================================

    cursor.execute("""
        SELECT COUNT(*) AS game_types
        FROM games
    """)

    game_types = cursor.fetchone()["game_types"]

    # ============================================
    # GAME STATISTICS
    # ============================================

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

    # ============================================
    # TOP PLAYERS
    # ============================================

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

    # ============================================
    # GAMES LIST
    # ============================================

    cursor.execute("""
        SELECT *
        FROM games
        ORDER BY id
    """)

    admin_games = cursor.fetchall()

    # ============================================
    # RECENT MATCH HISTORY
    # ============================================

    cursor.execute("""
        SELECT
            username,
            game_name,
            result,
            score,
            played_at

        FROM history

        ORDER BY played_at DESC

        LIMIT 10
    """)

    recent_history = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(

        "admin_dashboard.html",

        admin_username=session["admin_username"],

        users=[],

        total_users=total_users,

        total_games=total_games,

        active_users=active_users,

        game_types=game_types,

        game_stats=game_stats,

        top_players=top_players,

        admin_games=admin_games,

        recent_history=recent_history

    )
# ============================================
# UPDATE GAME
# ============================================

@app.route("/admin/update-game/<int:game_id>", methods=["POST"])
def update_game(game_id):

    if "admin_username" not in session:
        return redirect(url_for("login"))

    name = request.form.get("name", "").strip()
    description = request.form.get("description", "").strip()
    status = request.form.get("status", "Active").strip()
    route = request.form.get("route", "").strip()
    icon = request.form.get("icon", "🎮").strip()

    if not name:
        return "Game name is required."

    conn = None
    cursor = None

    try:

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
            description,
            status,
            route,
            icon,
            game_id
        ))

        conn.commit()

    except Exception as e:

        if conn:
            conn.rollback()

        print("Update Game Error:", e)

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()

    return redirect(url_for("admin_dashboard"))


# ============================================
# ADD GAME
# ============================================

@app.route("/add_game", methods=["POST"])
def add_game():

    if "admin_username" not in session:
        return redirect(url_for("login"))

    game_name = request.form.get("game_name", "").strip()
    description = request.form.get("description", "").strip()
    icon = request.form.get("icon", "🎮").strip()
    route = request.form.get("route", "").strip()
    status = request.form.get("status", "Active").strip()

    if not game_name:
        return "Game name cannot be empty."

    conn = None
    cursor = None

    try:

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO games
            (
                game_name,
                description,
                icon,
                route,
                status
            )

            VALUES
            (%s,%s,%s,%s,%s)
        """, (
            game_name,
            description,
            icon,
            route,
            status
        ))

        conn.commit()

    except Exception as e:

        if conn:
            conn.rollback()

        print("Add Game Error:", e)

    finally:

        if cursor:
            cursor.close()

        if conn:
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
    game_name = request.form.get("game_name", "").strip()
    description = request.form.get("description", "").strip()
    icon = request.form.get("icon", "🎮").strip()
    route = request.form.get("route", "").strip()
    status = request.form.get("status", "Active").strip()

    conn = None
    cursor = None

    try:

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

    except Exception as e:

        if conn:
            conn.rollback()

        print("Edit Game Error:", e)

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()

    return redirect(url_for("admin_dashboard"))


# ============================================
# DELETE GAME
# ============================================

@app.route("/delete_game/<int:game_id>")
def delete_game(game_id):

    if "admin_username" not in session:
        return redirect(url_for("login"))

    conn = None
    cursor = None

    try:

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM games WHERE id=%s",
            (game_id,)
        )

        conn.commit()

    except Exception as e:

        if conn:
            conn.rollback()

        print("Delete Game Error:", e)

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()

    return redirect(url_for("admin_dashboard"))


# ============================================
# DELETE USER
# ============================================

@app.route("/admin/delete-user/<int:user_id>")
def delete_user(user_id):

    if "admin_username" not in session:
        return redirect(url_for("login"))

    conn = None
    cursor = None

    try:

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM users WHERE id=%s",
            (user_id,)
        )

        conn.commit()

    except Exception as e:

        if conn:
            conn.rollback()

        print("Delete User Error:", e)

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()

    return redirect(url_for("admin_dashboard"))


# ============================================
# API USER STATS
# ============================================

@app.route("/api/user-stats")
def api_user_stats():

    if "Username" not in session:

        return jsonify({
            "success": False,
            "total_games": 0,
            "high_score": 0
        })

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT COUNT(*) AS total_games
        FROM history
        WHERE username=%s
    """, (
        session["Username"],
    ))

    total_games = cursor.fetchone()["total_games"]

    cursor.execute("""
        SELECT MAX(score) AS high_score
        FROM history
        WHERE username=%s
    """, (
        session["Username"],
    ))

    result = cursor.fetchone()

    cursor.close()
    conn.close()

    return jsonify({

        "success": True,

        "total_games": total_games,

        "high_score": result["high_score"] or 0

    })


# ============================================
# LOGOUT
# ============================================

@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("login"))


# ============================================
# RUN APP
# ============================================

if __name__ == "__main__":

    debug_mode = os.environ.get("FLASK_ENV") != "production"

    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port,
        debug=debug_mode
    )