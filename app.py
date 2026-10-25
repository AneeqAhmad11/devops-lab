import os
import time

import psycopg2
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)


def get_conn():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "db"),
        dbname=os.getenv("DB_NAME", "tasksdb"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "secret"),
    )


def init_db():
    # The database container may need a few seconds to start, so retry.
    for _ in range(30):
        try:
            conn = get_conn()
            cur = conn.cursor()
            cur.execute(
                "CREATE TABLE IF NOT EXISTS tasks ("
                "id SERIAL PRIMARY KEY, title TEXT NOT NULL)"
            )
            conn.commit()
            conn.close()
            return
        except psycopg2.OperationalError:
            time.sleep(2)
    raise RuntimeError("Database not reachable")


@app.route("/")
def index():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, title FROM tasks ORDER BY id DESC")
    tasks = cur.fetchall()
    conn.close()
    return render_template("index.html", tasks=tasks, host=os.uname().nodename)


@app.route("/add", methods=["POST"])
def add():
    title = request.form.get("title", "").strip()
    if title:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("INSERT INTO tasks (title) VALUES (%s)", (title,))
        conn.commit()
        conn.close()
    return redirect(url_for("index"))


@app.route("/health")
def health():
    return "ok", 200


init_db()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
