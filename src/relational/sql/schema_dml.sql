-- ==========================================
-- 1. DATA INSERTION (Seed 10 Movies)
-- ==========================================

INSERT INTO Studio (StudioName, HQ) VALUES 
('Warner Bros', 'Burbank'), 
('Paramount', 'Hollywood'), 
('Universal', 'Universal City'), 
('20th Century Fox', 'Los Angeles');

-- Insert Base Persons
INSERT INTO Person (PersonID, Name, BirthDate) VALUES 
(1, 'Christopher Nolan', '1970-07-30'),
(2, 'Martin Scorsese', '1942-11-17'),
(3, 'Quentin Tarantino', '1963-03-27'),
(4, 'Steven Spielberg', '1946-12-18'),
(5, 'Alfred Hitchcock', '1899-08-13'),
(6, 'James Cameron', '1954-08-16'),
(7, 'Ridley Scott', '1937-11-30'),
(8, 'Francis Ford Coppola', '1939-04-07'),
(9, 'Stanley Kubrick', '1928-07-26'),
(10, 'George Lucas', '1944-05-14'),
(11, 'Leonardo DiCaprio', '1974-11-11'),
(12, 'Robert De Niro', '1943-08-17'),
(13, 'Brad Pitt', '1963-12-18'),
(14, 'Tom Hanks', '1956-07-09'),
(15, 'Anthony Perkins', '1932-04-04'),
(16, 'Kate Winslet', '1975-10-05'),
(17, 'Russell Crowe', '1964-04-07'),
(18, 'Al Pacino', '1940-04-25'),
(19, 'Tom Cruise', '1962-07-03'),
(20, 'Mark Hamill', '1951-09-25');

-- Populate ISA Hierarchies
INSERT INTO Director (PersonID) VALUES (1), (2), (3), (4), (5), (6), (7), (8), (9), (10);
INSERT INTO Actor (PersonID) VALUES (11), (12), (13), (14), (15), (16), (17), (18), (19), (20);

-- Insert Movies
INSERT INTO Movie (MovieID, Title, Genre, StudioName) VALUES 
(1, 'Inception', 'Sci-Fi', 'Warner Bros'),
(2, 'The Wolf of Wall Street', 'Biography', 'Paramount'),
(3, 'Inglourious Basterds', 'War', 'Universal'),
(4, 'Saving Private Ryan', 'War', 'Paramount'),
(5, 'Psycho', 'Horror', 'Universal'),
(6, 'Titanic', 'Romance', '20th Century Fox'),
(7, 'Gladiator', 'Action', 'Universal'),
(8, 'The Godfather', 'Crime', 'Paramount'),
(9, 'Eyes Wide Shut', 'Drama', 'Warner Bros'),
(10, 'Star Wars', 'Sci-Fi', '20th Century Fox');

-- Bridge: Director Directs Movie
INSERT INTO MovieDirector (MovieID, PersonID) VALUES 
(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), 
(6, 6), (7, 7), (8, 8), (9, 9), (10, 10);

-- Bridge: Actor Fills PerformanceRole
INSERT INTO PerformanceRole (MovieID, PersonID, CharacterName, BillingOrder) VALUES 
(1, 11, 'Cobb', 1), 
(2, 11, 'Jordan Belfort', 1), (2, 12, 'Murray', 2),
(3, 13, 'Lt. Aldo Raine', 1), 
(4, 14, 'Captain Miller', 1), 
(5, 15, 'Norman Bates', 1),
(6, 16, 'Rose DeWitt Bukater', 1), 
(7, 17, 'Maximus', 1), 
(8, 18, 'Michael Corleone', 1),
(9, 19, 'Dr. Bill Harford', 1), 
(10, 20, 'Luke Skywalker', 1);

-- ==========================================
-- 2. DATA RETRIEVAL (SELECT Queries)
-- ==========================================

-- A. Subquery: Find movies that share the same genre as 'Inception'
SELECT Title FROM Movie 
WHERE Genre = (SELECT Genre FROM Movie WHERE Title = 'Inception') 
AND Title <> 'Inception';

-- B. Subquery with IN: Find genres of movies directed by 'Martin Scorsese'
SELECT Title FROM Movie 
WHERE Genre IN (
    SELECT m.Genre FROM Movie m
    JOIN MovieDirector md ON m.MovieID = md.MovieID
    JOIN Person p ON md.PersonID = p.PersonID
    WHERE p.Name = 'Martin Scorsese'
);

-- C. JOIN & Aggregation: Count the number of movies made by each director
SELECT p.Name, COUNT(md.MovieID) AS NumberOfMovies 
FROM Person p
JOIN MovieDirector md ON p.PersonID = md.PersonID
GROUP BY p.PersonID, p.Name;

-- ==========================================
-- 3. DATA MODIFICATION (UPDATE & DELETE)
-- ==========================================

UPDATE Person SET Name = 'Alfred J. Hitchcock' WHERE Name = 'Alfred Hitchcock';

-- Since your DDL has ON DELETE CASCADE, deleting the movie automatically cleans the bridge tables!
-- DELETE FROM Movie WHERE Title = 'Star Wars';