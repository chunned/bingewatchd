import sqlite3

# Create DB and cursor object
con = sqlite3.connect("tvdb.db")
cur = con.cursor()


def createTables():
    # Create SHOW table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS show(
    id INTEGER,
    name TEXT,
    startDate TEXT,
    endDate TEXT,
    rating INTEGER,
    PRIMARY KEY (id, name)
    )
    """)
    # TODO: add genres, add any constraints necessary (i.e. NOT NULL)

    # Create SEASON table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS season(
    id INTEGER,
    number INTEGER,
    startDate TEXT,
    endDate TEXT,
    rating INTEGER,
    PRIMARY KEY (id, number)
    )
    """)

    # # Create STUDIO table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS studio(
    id INTEGER,
    name TEXT,
    country TEXT,
    PRIMARY KEY (id, name)
    )
    """)

    # Create EPISODE table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS episode(
    id INTEGER,
    name TEXT,
    number INTEGER,
    airDate TEXT,
    dateWatched TEXT,
    rating INTEGER,
    PRIMARY KEY (id, name)
    )
    """)

    # Create ACTOR table
    cur.execute("""CREATE TABLE IF NOT EXISTS actor(
    id INTEGER, 
    name TEXT, 
    country TEXT, 
    PRIMARY KEY (id, name)
    )
    """)

    # RELATIONSHIP TABLES
    # Studio-Show relationship (Studio produces Show)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS studio_show(
    studioID INTEGER, 
    showID INTEGER, 
    FOREIGN KEY(studioID, studioName) REFERENCES studio(id, name), 
    FOREIGN KEY(showID, showName) REFERENCES show(id, name)
    PRIMARY KEY (studioID, showID)
    )
    """)

    # Actor-Show relationship A (Actor stars in Show)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS stars_in(
    showID INTEGER,
    actorID INTEGER,
    FOREIGN KEY(showID) REFERENCES show(id),
    FOREIGN KEY(actorID) REFERENCES actor(id),
    PRIMARY KEY (showID, actorID)
    )
    """)

    # Actor-Show relationship B (Actor appears in Show)
    cur.execute("""CREATE TABLE IF NOT EXISTS appears_in(
    episodeID integer,
    actorID integer,
    FOREIGN KEY(episodeID) REFERENCES episode(id),
    FOREIGN KEY(actorID) REFERENCES actor(id),
    PRIMARY KEY (episodeID, actorID)
    )
    """)

    # Show-Season relationship (Show contains Season)
    cur.execute("""CREATE TABLE IF NOT EXISTS show_season(
    showID INTEGER,
    seasonID INTEGER,
    FOREIGN KEY(showID) REFERENCES show(id),
    FOREIGN KEY(seasonID) REFERENCES season(id),
    PRIMARY KEY (showID, seasonID)
    )
    """)

    # Season-Episode relationship (Season contains Episode)
    cur.execute("""CREATE TABLE IF NOT EXISTS season_episode(
    seasonID INTEGER,
    episodeID INTEGER,
    FOREIGN KEY(seasonID) REFERENCES season(id),
    FOREIGN KEY(episodeID) REFERENCES episode(id),
    PRIMARY KEY (seasonID, episodeID)
    )
    """)

    # Genres table
    cur.execute("""CREATE TABLE IF NOT EXISTS genres(
    showID INTEGER, 
    genreName TEXT,
    FOREIGN KEY (showID) REFERENCES show(id),
    PRIMARY KEY (showID, genreName) 
    )
    """)


createTables()