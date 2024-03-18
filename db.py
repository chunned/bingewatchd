import sqlite3


def createTables(cur):
    # Parameters: SQLite cursor object
    # MAIN RELATIONS
    # Create SHOW table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS show(
    id INTEGER PRIMARY KEY,
    name TEXT,
    startDate TEXT,
    endDate TEXT,
    rating INTEGER
    )
    """)
    
    # Create SEASON table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS season(
    id INTEGER PRIMARY KEY,
    number INTEGER,
    airDate TEXT,
    rating INTEGER
    )
    """)

    # # Create network table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS network(
    id INTEGER PRIMARY KEY,
    name TEXT,
    country TEXT
    )
    """)

    # Create EPISODE table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS episode(
    id INTEGER PRIMARY KEY,
    name TEXT,
    number INTEGER,
    airDate TEXT,
    dateWatched TEXT,
    rating INTEGER
    )
    """)

    # Create ACTOR table
    cur.execute("""CREATE TABLE IF NOT EXISTS actor(
    id INTEGER PRIMARY KEY, 
    name TEXT
    )
    """)

    # RELATIONSHIP TABLES
    # network-Show relationship (network airs Show)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS network_show(
    networkID INTEGER, 
    showID INTEGER, 
    FOREIGN KEY(networkID) REFERENCES network(id), 
    FOREIGN KEY(showID) REFERENCES show(id)
    PRIMARY KEY (networkID, showID)
    )
    """)

    # Actor-Episode relationship (Actor appears in Episode)
    cur.execute("""CREATE TABLE IF NOT EXISTS appears_in(
    character TEXT,
    episodeID INTEGER,
    actorID INTEGER,
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


def insertShow(cur, con, show):
    try:
        cur.execute("INSERT INTO show (id, name, startDate, endDate) VALUES (?, ?, ?, ?)",
                    (show['id'], show['name'], show['startDate'], show['endDate']))
        con.commit()
    except sqlite3.IntegrityError:
        print("Show already exists in database.")
        return None


def insertSeason(cur, con, season):
    try:
        cur.execute("INSERT INTO season (id, number, airDate) VALUES (?, ?, ?)",
                    (season['id'], season['number'], season['airDate']))
        con.commit()
    except sqlite3.IntegrityError:
        print("Season already exists in database.")
        return None


def insertEpisode(cur, con, episode):
    try:
        cur.execute("INSERT INTO episode (id, name, number, airDate, dateWatched, rating) VALUES (?, ?, ?, ?, ?, ?)",
                    (episode['id'], episode['name'], episode['number'], episode['airDate'],
                     episode['dateWatched'], episode['rating']))
        con.commit()
    except sqlite3.IntegrityError:
        print("Episode already exists in database.")
        return None


def insertSeasonEpisode(cur, con, seasonID, episodeID):
    try:
        cur.execute("INSERT INTO season_episode (seasonID, episodeID) VALUES (?, ?)",
                    (seasonID, episodeID))
        con.commit()
    except sqlite3.IntegrityError:
        print("Season-Episode relationship already exists in database.")
        return None


def insertShowSeason(cur, con, showID, seasonID):
    try:
        cur.execute("INSERT INTO show_season (showID, seasonID) VALUES (?, ?)",
                    (showID, seasonID))
        con.commit()
    except sqlite3.IntegrityError:
        print("Show-Season relationship already exists in database.")


def insertActor(cur, con, actor):
    try:
        cur.execute("INSERT INTO actor (id, name) VALUES (?, ?)",
                    (actor['id'], actor['name']))
        con.commit()
    except sqlite3.IntegrityError:
        print("Actor already exists in database.")


def insertAppearance(cur, con, appearance):
    try:
        cur.execute("INSERT INTO appears_in (episodeID, actorID, character) VALUES (?, ?, ?)",
                    (appearance['episodeID'], appearance['actorID'], appearance['character']))
        con.commit()
    except sqlite3.IntegrityError:
        print("Appearance already exists in database.")


def insertNetwork(cur, con, network):
    try:
        cur.execute("INSERT INTO network (id, name, country) VALUES (?, ?, ?)",
                    (network['id'], network['name'], network['country']))
        con.commit()
    except sqlite3.IntegrityError:
        print("Network already exists in database.")


def insertNetworkShow(cur, con, networkID, showID):
    try:
        cur.execute("INSERT INTO network_show (networkID, showID) VALUES (?, ?)",
                    (networkID, showID))
        con.commit()
    except sqlite3.IntegrityError:
        print("Network-show relationship already exists in database.")


def insertShowGenre(cur, con, showID, genre):
    try:
        cur.execute("INSERT INTO genres (showID, genreName) VALUES (?, ?)",
                    (showID, genre))
        con.commit()
    except sqlite3.IntegrityError:
        print("Show-genre relationship already exists in database.")

def deleteInstance(cur, con, table, instanceID):
    try:
        cur.execute(f"DELETE FROM {table} WHERE id = {instanceID}")
        con.commit()
    except Exception as e:
        print(f"ERROR: {e}")

def patchInstance(cur, con, table, instanceID, columns, newValues):
    # Columns and newValues must be in the following format: (name, number, airDate), (Pilot, 1, 1993-09-10)
    try:
        cur.execute(f"UPDATE {table} SET {columns} = {newValues} WHERE id = {instanceID}")
        con.commit()
    except Exception as e:
        print(f"ERROR: {e}")

def putInstance(cur, con, table, columns, values):
    # Coluns and values 
    try:
        cur.execute(f"REPLACE INTO {table} {columns} VALUES{values}")
        con.commit()
    except Exception as e:
        print(f"ERROR: {e}")