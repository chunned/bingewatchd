import sqlite3

# Create DB and cursor object
con = sqlite3.connect("tvdb.db")
cur = con.cursor()

def createTables():
  # Create SHOW table
  cur.execute("CREATE TABLE IF NOT EXISTS show(id INTEGER, name TEXT, startDate TEXT, endDate TEXT, rating INTEGER, PRIMARY KEY (id, name))")
  # TODO: add genres, add any constraints necessary (i.e. NOT NULL)
  
  # Create SEASON table
  cur.execute("CREATE TABLE IF NOT EXISTS season(id INTEGER, number INTEGER, startDate TEXT, endDate TEXT, rating INTEGER, PRIMARY KEY (id, number))")
  
  # Create STUDIO table
  cur.execute("CREATE TABLE IF NOT EXISTS studio(id INTEGER, name TEXT, country TEXT, PRIMARY KEY (id, name))")
  
  # Create EPISODE table
  cur.execute("CREATE TABLE IF NOT EXISTS episode(id INTEGER, name TEXT, number INTEGER, airDate TEXT, dateWatched TEXT, rating INTEGER, PRIMARY KEY (id, name))")
  
  # Create ACTOR table
  cur.execute("CREATE TABLE IF NOT EXISTS actor(id INTEGER, name TEXT, country TEXT, PRIMARY KEY (id, name))")
