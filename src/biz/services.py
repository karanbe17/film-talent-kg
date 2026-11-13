"""Business layer: validation + orchestration of multi-step operations."""
import sqlite3
from src.dal import database, movie_dal, person_dal

ROLE_TYPES = ("Lead", "Supporting", "Cameo")

class BizError(Exception):
    """A user-correctable problem (shown as a flash message in the UI)."""

def _clean(value, label, required=True, max_len=255):
    value = (value or "").strip()
    if required and not value:
        raise BizError(f"{label} is required.")
    if len(value) > max_len:
        raise BizError(f"{label} is too long (max {max_len}).")
    return value or None

def _guard(fn):
    def wrapper(*a, **kw):
        try:
            return fn(*a, **kw)
        except sqlite3.IntegrityError as e:
            raise BizError(f"Rejected by database constraint: {e}") from e
    wrapper.__name__ = fn.__name__
    return wrapper

def dashboard(genre=None, title=None, person=None):
    with database.transaction() as c:
        return {
            "movies": movie_dal.search_movies(c, genre=_clean(genre, "Genre", False), title=_clean(title, "Title", False)),
            "directors": person_dal.list_directors(c, _clean(person, "Name", False)),
            "actors": person_dal.list_actors(c, _clean(person, "Name", False)),
            "cast": movie_dal.list_cast(c),
        }

def get_movie(movie_id):
    with database.transaction() as c:
        movie = movie_dal.get_movie(c, movie_id)
        if movie is None:
            raise BizError("Movie not found.")
        return movie

@_guard
def add_actor(name):
    name = _clean(name, "Actor name")
    with database.transaction() as c:
        pid = person_dal.get_person_id_by_name(c, name) or person_dal.insert_person(c, name)
        if person_dal.get_actor_id(c, pid):
            raise BizError(f"'{name}' is already an actor.")
        person_dal.insert_actor(c, pid)

@_guard
def add_director_with_movie(director_name, title, genre, studio):
    director_name = _clean(director_name, "Director name")
    title = _clean(title, "Movie title", required=False)
    with database.transaction() as c:
        pid = person_dal.get_person_id_by_name(c, director_name) or person_dal.insert_person(c, director_name)
        did = person_dal.get_director_id(c, pid) or person_dal.insert_director(c, pid)
        if title:
            genre_v = _clean(genre, "Genre")
            mid = movie_dal.get_movie_id_by_title(c, title) or movie_dal.insert_movie(c, title, genre_v, _clean(studio, "Studio", False))
            movie_dal.link_director(c, mid, did)

@_guard
def add_movie(title, genre, studio, director_name):
    title = _clean(title, "Title"); genre = _clean(genre, "Genre")
    studio = _clean(studio, "Studio", False)
    director_name = _clean(director_name, "Director name", False)
    with database.transaction() as c:
        mid = movie_dal.insert_movie(c, title, genre, studio)
        if director_name:
            pid = person_dal.get_person_id_by_name(c, director_name) or person_dal.insert_person(c, director_name)
            did = person_dal.get_director_id(c, pid) or person_dal.insert_director(c, pid)
            movie_dal.link_director(c, mid, did)

@_guard
def add_cast(movie_title, actor_name, role_name, role_type):
    movie_title = _clean(movie_title, "Movie"); actor_name = _clean(actor_name, "Actor")
    role_name = _clean(role_name, "Role name")
    if role_type not in ROLE_TYPES:
        raise BizError(f"Role type must be one of {ROLE_TYPES}.")
    with database.transaction() as c:
        mid = movie_dal.get_movie_id_by_title(c, movie_title)
        if mid is None:
            raise BizError(f"Movie '{movie_title}' does not exist.")
        pid = person_dal.get_person_id_by_name(c, actor_name)
        aid = person_dal.get_actor_id(c, pid) if pid else None
        if aid is None:
            raise BizError(f"'{actor_name}' is not a registered actor.")
        movie_dal.insert_performance(c, mid, aid, role_name, role_type)

@_guard
def update_movie(movie_id, title, genre, studio):
    title = _clean(title, "Title"); genre = _clean(genre, "Genre")
    with database.transaction() as c:
        if movie_dal.update_movie(c, movie_id, title, genre, _clean(studio, "Studio", False)) == 0:
            raise BizError("Movie not found.")

def delete_movie(movie_id):
    with database.transaction() as c:
        if movie_dal.delete_movie(c, movie_id) == 0:
            raise BizError("Movie not found.")

@_guard
def rename_person(person_id, new_name):
    new_name = _clean(new_name, "Name")
    with database.transaction() as c:
        if person_dal.update_person_name(c, person_id, new_name) == 0:
            raise BizError("Person not found.")

def delete_person(person_id):
    with database.transaction() as c:
        if person_dal.delete_person(c, person_id) == 0:
            raise BizError("Person not found.")

def delete_performance(performance_id):
    with database.transaction() as c:
        movie_dal.delete_performance(c, performance_id)