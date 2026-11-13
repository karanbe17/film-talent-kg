-- Demonstration queries (SELECT / UPDATE / DELETE). Run after 02_seed.sql.
PRAGMA foreign_keys = ON;

-- Q1 JOIN: movies with their directors
SELECT Movie.Title, Person.Name AS Director
FROM Movie
JOIN MovieDirector ON MovieDirector.MovieId = Movie.Id
JOIN Director      ON Director.Id = MovieDirector.DirectorId
JOIN Person        ON Person.Id = Director.PersonId
ORDER BY Movie.Title;

-- Q2 AGGREGATION: number of movies per director
SELECT Person.Name, COUNT(MovieDirector.Id) AS NumberOfMovies
FROM Director
JOIN Person        ON Person.Id = Director.PersonId
JOIN MovieDirector ON MovieDirector.DirectorId = Director.Id
GROUP BY Director.Id, Person.Name
ORDER BY NumberOfMovies DESC, Person.Name;

-- Q3 SUBQUERY (IN): movies sharing a genre with any movie by Scorsese
SELECT Title FROM Movie
WHERE Genre IN (
    SELECT Movie.Genre
    FROM Movie
    JOIN MovieDirector ON MovieDirector.MovieId = Movie.Id
    JOIN Director      ON Director.Id = MovieDirector.DirectorId
    JOIN Person        ON Person.Id = Director.PersonId
    WHERE Person.Name = 'Martin Scorsese');

-- Q4 SELF-JOIN with aliases: movies with the same genre as 'Inception'
SELECT MovieOther.Title, MovieOther.Genre
FROM Movie AS MovieInception, Movie AS MovieOther
WHERE MovieInception.Title = 'Inception'
  AND MovieOther.Genre = MovieInception.Genre
  AND MovieOther.Id <> MovieInception.Id;

-- Q5 MULTI-JOIN: cast list with role types
SELECT Movie.Title, Person.Name AS Actor, PerformanceRole.RoleName, PerformanceRole.RoleType
FROM PerformanceRole
JOIN Movie  ON Movie.Id = PerformanceRole.MovieId
JOIN Actor  ON Actor.Id = PerformanceRole.ActorId
JOIN Person ON Person.Id = Actor.PersonId
ORDER BY Movie.Title, PerformanceRole.RoleType;

-- Q6 Actors who worked with more than one director (HAVING)
SELECT Person.Name, COUNT(DISTINCT MovieDirector.DirectorId) AS Directors
FROM Actor
JOIN Person          ON Person.Id = Actor.PersonId
JOIN PerformanceRole ON PerformanceRole.ActorId = Actor.Id
JOIN MovieDirector   ON MovieDirector.MovieId = PerformanceRole.MovieId
GROUP BY Actor.Id, Person.Name
HAVING COUNT(DISTINCT MovieDirector.DirectorId) > 1;

-- UPDATE (always with a WHERE clause)
UPDATE Movie SET Genre = 'Science Fiction' WHERE Title = 'Star Wars';

-- DELETE: removing a movie cascades to MovieDirector and PerformanceRole
DELETE FROM Movie WHERE Title = 'Star Wars';
SELECT COUNT(*) AS OrphanLinks FROM MovieDirector
WHERE MovieId NOT IN (SELECT Id FROM Movie);   -- expected: 0