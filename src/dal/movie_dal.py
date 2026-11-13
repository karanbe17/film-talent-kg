"""DAL: Movie, MovieDirector, PerformanceRole."""

def insert_movie(conn, title, genre, studio):
    return conn.execute("INSERT INTO Movie(Title, Genre, StudioName) VALUES (?, ?, ?)", (title, genre, studio)).lastrowid

def link_director(conn, movie_id, director_id):
    return conn.execute("INSERT INTO MovieDirector(MovieId, DirectorId) VALUES (?, ?)", (movie_id, director_id)).lastrowid

def insert_performance(conn, movie_id, actor_id, role_name, role_type):
    return conn.execute("INSERT INTO PerformanceRole(MovieId, ActorId, RoleName, RoleType) VALUES (?, ?, ?, ?)", (movie_id, actor_id, role_name, role_type)).lastrowid

def get_movie_id_by_title(conn, title):
    row = conn.execute("SELECT Id FROM Movie WHERE Title = ?", (title,)).fetchone()
    return row["Id"] if row else None

def get_movie(conn, movie_id):
    return conn.execute("SELECT * FROM Movie WHERE Id = ?", (movie_id,)).fetchone()

def search_movies(conn, genre=None, title=None):
    sql = ("SELECT Movie.Id, Movie.Title, Movie.Genre, Movie.StudioName, "
           "GROUP_CONCAT(Person.Name, ', ') AS Directors "
           "FROM Movie "
           "LEFT JOIN MovieDirector ON MovieDirector.MovieId = Movie.Id "
           "LEFT JOIN Director ON Director.Id = MovieDirector.DirectorId "
           "LEFT JOIN Person ON Person.Id = Director.PersonId ")
    where, params = [], []
    if genre:
        where.append("Movie.Genre LIKE ?"); params.append(f"%{genre}%")
    if title:
        where.append("Movie.Title LIKE ?"); params.append(f"%{title}%")
    if where:
        sql += "WHERE " + " AND ".join(where) + " "
    sql += "GROUP BY Movie.Id ORDER BY Movie.Title"
    return conn.execute(sql, params).fetchall()

def list_cast(conn, movie_id=None):
    sql = ("SELECT PerformanceRole.Id, Movie.Title, Person.Name AS Actor, "
           "PerformanceRole.RoleName, PerformanceRole.RoleType "
           "FROM PerformanceRole "
           "JOIN Movie ON Movie.Id = PerformanceRole.MovieId "
           "JOIN Actor ON Actor.Id = PerformanceRole.ActorId "
           "JOIN Person ON Person.Id = Actor.PersonId ")
    params = []
    if movie_id:
        sql += "WHERE Movie.Id = ? "; params.append(movie_id)
    sql += "ORDER BY Movie.Title, PerformanceRole.RoleType"
    return conn.execute(sql, params).fetchall()

def update_movie(conn, movie_id, title, genre, studio):
    return conn.execute("UPDATE Movie SET Title = ?, Genre = ?, StudioName = ? WHERE Id = ?", (title, genre, studio, movie_id)).rowcount

def delete_movie(conn, movie_id):
    return conn.execute("DELETE FROM Movie WHERE Id = ?", (movie_id,)).rowcount

def delete_performance(conn, performance_id):
    return conn.execute("DELETE FROM PerformanceRole WHERE Id = ?", (performance_id,)).rowcount