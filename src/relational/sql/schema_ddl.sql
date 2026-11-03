-- 1. CORE ENTITIES
-- ==========================================

CREATE TABLE Studio (
    StudioName VARCHAR(100) PRIMARY KEY,
    HQ VARCHAR(100)
);

CREATE TABLE Person (
    PersonID INTEGER PRIMARY KEY AUTOINCREMENT,
    Name VARCHAR(150) NOT NULL,
    BirthDate DATE
);

CREATE TABLE Award (
    AwardName VARCHAR(100),
    Category VARCHAR(100),
    Year INTEGER,
    PRIMARY KEY (AwardName, Category, Year)
);

CREATE TABLE Movie (
    MovieID INTEGER PRIMARY KEY AUTOINCREMENT,
    Title VARCHAR(255) NOT NULL,
    ReleaseDate DATE,
    Duration INTEGER,
    Genre VARCHAR(50),
    BoxOfficeRevenue DECIMAL(15,2),
    Budget DECIMAL(15,2),
    StudioName VARCHAR(100) NOT NULL,
    FOREIGN KEY (StudioName) REFERENCES Studio(StudioName) ON DELETE CASCADE
);

-- ==========================================
-- 2. ISA HIERARCHY SUBCLASSES
-- ==========================================

CREATE TABLE Actor (
    PersonID INTEGER PRIMARY KEY,
    FOREIGN KEY (PersonID) REFERENCES Person(PersonID) ON DELETE CASCADE
);

CREATE TABLE Director (
    PersonID INTEGER PRIMARY KEY,
    FOREIGN KEY (PersonID) REFERENCES Person(PersonID) ON DELETE CASCADE
);

CREATE TABLE CameraMan (
    PersonID INTEGER PRIMARY KEY,
    FOREIGN KEY (PersonID) REFERENCES Person(PersonID) ON DELETE CASCADE
);

-- ==========================================
-- 3. RELATIONSHIPS (BRIDGE TABLES)
-- ==========================================

-- Person Receives Award
CREATE TABLE Receives (
    PersonID INTEGER,
    AwardName VARCHAR(100),
    Category VARCHAR(100),
    Year INTEGER,
    PRIMARY KEY (PersonID, AwardName, Category, Year),
    FOREIGN KEY (PersonID) REFERENCES Person(PersonID) ON DELETE CASCADE,
    FOREIGN KEY (AwardName, Category, Year) REFERENCES Award(AwardName, Category, Year) ON DELETE CASCADE
);

-- Director Directs Movie (Co-Director Support)
CREATE TABLE MovieDirector (
    MovieID INTEGER,
    PersonID INTEGER,
    PRIMARY KEY (MovieID, PersonID),
    FOREIGN KEY (MovieID) REFERENCES Movie(MovieID) ON DELETE CASCADE,
    FOREIGN KEY (PersonID) REFERENCES Director(PersonID) ON DELETE CASCADE
);

-- Actor Fills PerformanceRole in a Movie
CREATE TABLE PerformanceRole (
    MovieID INTEGER,
    PersonID INTEGER,
    CharacterName VARCHAR(150),
    BillingOrder INTEGER,
    PRIMARY KEY (MovieID, PersonID, CharacterName),
    FOREIGN KEY (MovieID) REFERENCES Movie(MovieID) ON DELETE CASCADE,
    FOREIGN KEY (PersonID) REFERENCES Actor(PersonID) ON DELETE CASCADE
);