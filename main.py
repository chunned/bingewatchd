import db
import tmdb
import sqlite3
import secrets
import bcrypt
from flask import session

'''
def main():
    print('OPTIONS MENU')
    print('1. Add a new episode')
    print('2. Add a rating to an existing show')
    print('3. Add a rating to an existing season')
    print('4. View My List')

    try:
        choice = int(input("Choice: "))
    except ValueError:
        print("ERROR: Choice was not an integer. Please try again.")
        return None

    if choice not in [1, 2, 3, 4]:
        print("ERROR: Invalid choice. Please option 1, 2, or 3.")
        return None

    if choice == 1:
        newEpisode()
    elif choice == 4:
        getEpisodes()
    else:
        print('Coming soon.')
'''

def newEpisode(showID,seasonNum,episodeNum,rating,dateWatched):
    con = sqlite3.connect(session.get("token"))
    cur = con.cursor()

    # Query episode
    episodeResult = tmdb.searchEpisode(showID, seasonNum, episodeNum)
    # If episode is already in DB, None will be returned - so check that 'result' has a value before proceeding
    if episodeResult:
        # Append rating to the result list
        episodeResult['rating'] = rating
        episodeResult['dateWatched'] = dateWatched
        # Add episode to DB
        db.insertEpisode(cur, con, episodeResult)

        # Add season to DB
        seasonResult = tmdb.searchSeason(showID, seasonNum)
        db.insertSeason(cur, con, seasonResult)

        # Add show to DB
        showResult = tmdb.searchShowDetails(showID)
        db.insertShow(cur, con, showResult[0])   # showResult is a tuple, we only want 1st item

        # Add show genre(s) to DB
        genres = showResult[3]
        for genre in genres:
            genreName = genre["name"]
            db.insertShowGenre(cur, con, showID, genreName)

        # Add network(s) to DB
        networks = showResult[2]
        for network in networks:
            db.insertNetwork(cur, con, network)
            db.insertNetworkShow(cur, con, network['id'], showID)

        # Add Season-Episode relationship entry
        db.insertSeasonEpisode(cur, con, seasonResult['id'], episodeResult['id'])

        # Add Show-Season relationship entry
        db.insertShowSeason(cur, con, showID, seasonResult['id'])

        # Search for cast and appearance details
        cast, appearances = tmdb.getCast(showID, seasonNum, episodeNum, episodeResult['id'])
        # Insert cast into actors table
        for actor in cast:
            db.insertActor(cur, con, actor)
        # Insert appearances into appears_in table
        for appearance in appearances:
            db.insertAppearance(cur, con, appearance)
    

#function to get the episodes in the table
def getEpisodes():
    con = sqlite3.connect(session.get("token"))
    cur = con.cursor()
    cur.execute('''SELECT * FROM show as sh JOIN show_season as ss on sh.id=ss.showID JOIN season as sea on sea.id=ss.seasonID JOIN season_episode as se on sea.id=se.seasonID JOIN episode as epi on se.episodeID=epi.id;''')
    rows = cur.fetchall() 
    table = [""]
    for row in rows:
        table.append(row)
        print(table)
    return table


def new_user(cur, con,name,password):
    # Store hashed+salted user password
    pass_hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    db_file = secrets.token_hex(32) + '.db'   # Generate random string for database file

    query = "INSERT INTO user (name, password, db_file) VALUES (?, ?, ?)"

    cur.execute(query, (name, pass_hashed, db_file))
    con.commit()


def verify_password(password, hashed_password):
    # Check hashed password. Using bcrypt.checkpw() method.
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)


def ulogin(cur, con,name,password):
    # Get user to input their username and password, see if database has a match
    # If so, return the database file, user is 'logged in'
    try : 
        cur.execute(f"SELECT * FROM user WHERE name = ?", (name,))
        row = cur.fetchall()
        pass_hash = row[0][1]
        # If x = True, password matches the stored hash
        x = verify_password(password, pass_hash)
        if x:
            return row[0][2]
        else:
            print('Incorrect password')
            return None
    except:
        return None

def deleteEntry(table,showID):
    con = sqlite3.connect(session.get("token"))
    cur = con.cursor()
    try:
        cur.execute(f"DELETE FROM {table} WHERE id = {showID}")
        con.commit()
    except Exception as e:
        print(f"ERROR: {e}")

USER_DB = "users.db"
# Initialize user database
connection = sqlite3.connect(USER_DB)
cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS user(
name TEXT PRIMARY KEY,
password TEXT,
db_file TEXT
)
""")

if __name__ == "__main__":
    print('Welcome to Watchd v0.1 (CLI only)')
    print('Initializing database...')
    # Initialize database
    con = sqlite3.connect(session.get("token"))
    cur = con.cursor()
    db.createTables(cur)
    print('Database created successfully.')
