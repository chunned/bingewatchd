import db
import tmdb
import sqlite3


def main():
    print('OPTIONS MENU')
    print('1. Add a new episode')
    print('2. Add a rating to an existing show')
    print('3. Add a rating to an existing season')

    try:
        choice = int(input("Choice: "))
    except ValueError:
        print("ERROR: Choice was not an integer. Please try again.")
        return None

    if choice not in [1, 2, 3]:
        print("ERROR: Invalid choice. Please option 1, 2, or 3.")
        return None

    if choice == 1:
        newEpisode()

    else:
        print('Coming soon.')


def newEpisode():
    name = input("SHOW NAME: ")
    # Get show ID
    showID = tmdb.searchShow(name)
    try:
        seasonNum = int(input("SEASON #: "))
        episodeNum = int(input("EPISODE #: "))
        rating = int(input("RATING (%): "))
    except ValueError:
        print('ERROR: Rating, Season, or Episode number was not an integer. Please try again.')
        return None
    # Query episode
    episodeResult = tmdb.searchEpisode(showID, seasonNum, episodeNum)
    # If episode is already in DB, None will be returned - so check that 'result' has a value before proceeding
    if episodeResult:
        # Append rating to the result list
        episodeResult['rating'] = rating
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


if __name__ == "__main__":
    print('Welcome to Watchd v0.1 (CLI only)')
    print('Initializing database...')
    # Initialize database
    con = sqlite3.connect("t5.db")
    cur = con.cursor()
    db.createTables(cur)
    print('Database created successfully.')

    while True:
        main()
