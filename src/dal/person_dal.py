"""DAL: Person / Actor / Director (IS-A hierarchy). All SQL is parameterized."""

def insert_person(conn, name):
    return conn.execute("INSERT INTO Person(Name) VALUES (?)", (name,)).lastrowid

def get_person_id_by_name(conn, name):
    row = conn.execute("SELECT Id FROM Person WHERE Name = ?", (name,)).fetchone()
    return row["Id"] if row else None

def insert_actor(conn, person_id):
    return conn.execute("INSERT INTO Actor(PersonId) VALUES (?)", (person_id,)).lastrowid

def insert_director(conn, person_id):
    return conn.execute("INSERT INTO Director(PersonId) VALUES (?)", (person_id,)).lastrowid

def get_director_id(conn, person_id):
    row = conn.execute("SELECT Id FROM Director WHERE PersonId = ?", (person_id,)).fetchone()
    return row["Id"] if row else None

def get_actor_id(conn, person_id):
    row = conn.execute("SELECT Id FROM Actor WHERE PersonId = ?", (person_id,)).fetchone()
    return row["Id"] if row else None

def list_directors(conn, name_filter=None):
    sql = ("SELECT Director.Id, Person.Id AS PersonId, Person.Name, "
           "COUNT(MovieDirector.Id) AS NumberOfMovies "
           "FROM Director JOIN Person ON Person.Id = Director.PersonId "
           "LEFT JOIN MovieDirector ON MovieDirector.DirectorId = Director.Id ")
    params = []
    if name_filter:
        sql += "WHERE Person.Name LIKE ? "; params.append(f"%{name_filter}%")
    sql += "GROUP BY Director.Id, Person.Id, Person.Name ORDER BY Person.Name"
    return conn.execute(sql, params).fetchall()

def list_actors(conn, name_filter=None):
    sql = ("SELECT Actor.Id, Person.Id AS PersonId, Person.Name "
           "FROM Actor JOIN Person ON Person.Id = Actor.PersonId ")
    params = []
    if name_filter:
        sql += "WHERE Person.Name LIKE ? "; params.append(f"%{name_filter}%")
    sql += "ORDER BY Person.Name"
    return conn.execute(sql, params).fetchall()

def update_person_name(conn, person_id, new_name):
    return conn.execute("UPDATE Person SET Name = ? WHERE Id = ?", (new_name, person_id)).rowcount

def delete_person(conn, person_id):
    return conn.execute("DELETE FROM Person WHERE Id = ?", (person_id,)).rowcount