-- ProduCast relational schema (DDL)  -- SQLite
-- Conventions (CSC501 manual 4.3): PascalCase names, surrogate key "Id",
-- UK_ = candidate key, FK_Source_Col_2_Target_Col = foreign key.
-- Safe to run on a fresh database.

PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS PerformanceRole;
DROP TABLE IF EXISTS MovieDirector;
DROP TABLE IF EXISTS Movie;
DROP TABLE IF EXISTS Actor;
DROP TABLE IF EXISTS Director;
DROP TABLE IF EXISTS Person;

-- Superclass of the IS-A hierarchy
CREATE TABLE Person (
    Id   INTEGER PRIMARY KEY AUTOINCREMENT,
    Name VARCHAR(255) NOT NULL,
    CONSTRAINT UK_Person_Name UNIQUE (Name)
);

-- Subclass Actor (one-to-one with Person -> candidate key on the FK)
CREATE TABLE Actor (
    Id       INTEGER PRIMARY KEY AUTOINCREMENT,
    PersonId INTEGER NOT NULL,
    CONSTRAINT UK_Actor_PersonId UNIQUE (PersonId),
    CONSTRAINT FK_Actor_PersonId_2_Person_Id
        FOREIGN KEY (PersonId) REFERENCES Person(Id) ON DELETE CASCADE
);

-- Subclass Director
CREATE TABLE Director (
    Id       INTEGER PRIMARY KEY AUTOINCREMENT,
    PersonId INTEGER NOT NULL,
    CONSTRAINT UK_Director_PersonId UNIQUE (PersonId),
    CONSTRAINT FK_Director_PersonId_2_Person_Id
        FOREIGN KEY (PersonId) REFERENCES Person(Id) ON DELETE CASCADE
);

CREATE TABLE Movie (
    Id         INTEGER PRIMARY KEY AUTOINCREMENT,
    Title      VARCHAR(255) NOT NULL,
    Genre      VARCHAR(255) NOT NULL,
    StudioName VARCHAR(255),
    CONSTRAINT UK_Movie_Title UNIQUE (Title)
);

-- Many-to-many: Movie <-> Director
CREATE TABLE MovieDirector (
    Id         INTEGER PRIMARY KEY AUTOINCREMENT,
    MovieId    INTEGER NOT NULL,
    DirectorId INTEGER NOT NULL,
    CONSTRAINT UK_MovieDirector_MovieId_DirectorId UNIQUE (MovieId, DirectorId),
    CONSTRAINT FK_MovieDirector_MovieId_2_Movie_Id
        FOREIGN KEY (MovieId) REFERENCES Movie(Id) ON DELETE CASCADE,
    CONSTRAINT FK_MovieDirector_DirectorId_2_Director_Id
        FOREIGN KEY (DirectorId) REFERENCES Director(Id) ON DELETE CASCADE
);

-- Many-to-many: Movie <-> Actor (bridge entity Performance_Role in the ERD)
CREATE TABLE PerformanceRole (
    Id       INTEGER PRIMARY KEY AUTOINCREMENT,
    MovieId  INTEGER NOT NULL,
    ActorId  INTEGER NOT NULL,
    RoleName VARCHAR(255) NOT NULL,
    RoleType VARCHAR(20) NOT NULL DEFAULT 'Supporting',
    CONSTRAINT UK_PerformanceRole_MovieId_ActorId UNIQUE (MovieId, ActorId),
    CONSTRAINT CK_PerformanceRole_RoleType
        CHECK (RoleType IN ('Lead', 'Supporting', 'Cameo')),
    CONSTRAINT FK_PerformanceRole_MovieId_2_Movie_Id
        FOREIGN KEY (MovieId) REFERENCES Movie(Id) ON DELETE CASCADE,
    CONSTRAINT FK_PerformanceRole_ActorId_2_Actor_Id
        FOREIGN KEY (ActorId) REFERENCES Actor(Id) ON DELETE CASCADE
);