"""UI layer (Flask). Works from ANY directory."""
import sys
from pathlib import Path

# Dynamically add the project root to sys.path
_ROOT = Path(__file__).resolve().parents[2]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from flask import Flask, flash, redirect, render_template, request, url_for
from src.biz import services
from src.biz.services import BizError, ROLE_TYPES
from src.dal import database

app = Flask(__name__)
app.secret_key = "produ-cast-demo-key"
database.ensure_db()

def _act(fn, ok_msg, *args):
    try:
        fn(*args)
        flash(ok_msg, "ok")
    except BizError as e:
        flash(str(e), "error")
    return redirect(url_for("index"))

@app.route("/")
def index():
    data = services.dashboard(request.args.get("genre"), request.args.get("title"), request.args.get("person"))
    return render_template("index.html", role_types=ROLE_TYPES, genre=request.args.get("genre", ""), title=request.args.get("title", ""), person=request.args.get("person", ""), **data)

@app.post("/director/add")
def add_director():
    f = request.form
    return _act(services.add_director_with_movie, "Director (and movie) saved.", f["name"], f.get("title"), f.get("genre"), f.get("studio"))

@app.post("/actor/add")
def add_actor():
    return _act(services.add_actor, "Actor saved.", request.form["name"])

@app.post("/movie/add")
def add_movie():
    f = request.form
    return _act(services.add_movie, "Movie saved.", f["title"], f["genre"], f.get("studio"), f.get("director"))

@app.post("/cast/add")
def add_cast():
    f = request.form
    return _act(services.add_cast, "Cast member saved.", f["movie"], f["actor"], f["role"], f["role_type"])

@app.get("/movie/<int:movie_id>/edit")
def edit_movie_form(movie_id):
    try:
        return render_template("edit_movie.html", movie=services.get_movie(movie_id))
    except BizError as e:
        flash(str(e), "error")
        return redirect(url_for("index"))

@app.post("/movie/<int:movie_id>/edit")
def edit_movie(movie_id):
    f = request.form
    return _act(services.update_movie, "Movie updated.", movie_id, f["title"], f["genre"], f.get("studio"))

@app.post("/movie/<int:movie_id>/delete")
def delete_movie(movie_id):
    return _act(services.delete_movie, "Movie deleted (director links and cast removed by CASCADE).", movie_id)

@app.post("/person/<int:person_id>/rename")
def rename_person(person_id):
    return _act(services.rename_person, "Name updated.", person_id, request.form["name"])

@app.post("/person/<int:person_id>/delete")
def delete_person(person_id):
    return _act(services.delete_person, "Person deleted (role/director links removed by CASCADE).", person_id)

@app.post("/cast/<int:performance_id>/delete")
def delete_cast(performance_id):
    return _act(services.delete_performance, "Cast entry removed.", performance_id)

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)