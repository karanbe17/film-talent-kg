-- Sample data (DML). Run after 01_schema.sql.
PRAGMA foreign_keys = ON;

INSERT INTO Person(Name) VALUES
 ('Christopher Nolan'), ('Francis Ford Coppola'), ('George Lucas'),
 ('Quentin Tarantino'), ('Martin Scorsese'), ('Ridley Scott'),
 ('Leonardo DiCaprio'), ('Al Pacino'), ('Mark Hamill'),
 ('Brad Pitt'), ('Russell Crowe'), ('Robert De Niro');

INSERT INTO Director(PersonId) SELECT Id FROM Person
 WHERE Name IN ('Christopher Nolan','Francis Ford Coppola','George Lucas',
                'Quentin Tarantino','Martin Scorsese','Ridley Scott');

INSERT INTO Actor(PersonId) SELECT Id FROM Person
 WHERE Name IN ('Leonardo DiCaprio','Al Pacino','Mark Hamill',
                'Brad Pitt','Russell Crowe','Robert De Niro');

INSERT INTO Movie(Title, Genre, StudioName) VALUES
 ('Inception',        'Sci-Fi',  'Warner Bros'),
 ('The Godfather',    'Crime',   'Paramount'),
 ('Star Wars',        'Sci-Fi',  '20th Century Fox'),
 ('Inglourious Basterds','War',  'Universal'),
 ('Raging Bull',      'Drama',   'United Artists'),
 ('Gladiator',        'Action',  'Universal'),
 ('The Wolf of Wall Street','Biography','Paramount');

-- Movie <-> Director (looked up by name, never by hard-coded Id)
INSERT INTO MovieDirector(MovieId, DirectorId)
SELECT m.Id, d.Id FROM (
  SELECT 'Inception' t, 'Christopher Nolan' n UNION ALL
  SELECT 'The Godfather','Francis Ford Coppola' UNION ALL
  SELECT 'Star Wars','George Lucas' UNION ALL
  SELECT 'Inglourious Basterds','Quentin Tarantino' UNION ALL
  SELECT 'Raging Bull','Martin Scorsese' UNION ALL
  SELECT 'Gladiator','Ridley Scott' UNION ALL
  SELECT 'The Wolf of Wall Street','Martin Scorsese') x
JOIN Movie m ON m.Title = x.t
JOIN Person p ON p.Name = x.n
JOIN Director d ON d.PersonId = p.Id;

-- Movie <-> Actor with role
INSERT INTO PerformanceRole(MovieId, ActorId, RoleName, RoleType)
SELECT m.Id, a.Id, x.r, x.k FROM (
  SELECT 'Inception' t, 'Leonardo DiCaprio' n, 'Cobb' r, 'Lead' k UNION ALL
  SELECT 'The Godfather','Al Pacino','Michael Corleone','Lead' UNION ALL
  SELECT 'Star Wars','Mark Hamill','Luke Skywalker','Lead' UNION ALL
  SELECT 'Inglourious Basterds','Brad Pitt','Aldo Raine','Lead' UNION ALL
  SELECT 'Raging Bull','Robert De Niro','Jake LaMotta','Lead' UNION ALL
  SELECT 'Gladiator','Russell Crowe','Maximus','Lead' UNION ALL
  SELECT 'The Wolf of Wall Street','Leonardo DiCaprio','Jordan Belfort','Lead' UNION ALL
  SELECT 'The Godfather','Robert De Niro','Vito Corleone (young)','Supporting') x
JOIN Movie m ON m.Title = x.t
JOIN Person p ON p.Name = x.n
JOIN Actor a ON a.PersonId = p.Id;