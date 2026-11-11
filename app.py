"""Intentionally vulnerable scanner test fixture. Do not deploy or run."""
import sqlite3
import subprocess
from flask import Flask, request

app = Flask(__name__)

@app.route("/users")
def users():
    # SAST test: untrusted input is concatenated into SQL.
    name = request.args.get("name", "")
    with sqlite3.connect(":memory:") as database:
        database.execute("CREATE TABLE users (name TEXT)")
        rows = database.execute("SELECT name FROM users WHERE name = '" + name + "'").fetchall()
    return {"users": rows}

@app.route("/command")
def command():
    # SAST test: untrusted input reaches a shell command.
    command_text = request.args.get("cmd", "")
    return subprocess.check_output(command_text, shell=True, text=True)
