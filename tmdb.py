import requests
import json
#import dotenv
import os
from datetime import datetime

# TODO: try/except error handling

# Read API token and key from .env file
#apiSecrets = dotenv.dotenv_values('.env')
# Authentication header using API token from .env file
header = {'Authorization': f'Bearer {os.getenv("API_TOKEN")}',
          'accept': 'application/json'}
# Base URL used for all API queries
URLBASE = 'https://api.themoviedb.org/3'


def getApiConfiguration():
    # Observe the current TMDB configuration
    r = requests.request('GET', URLBASE + '/configuration', headers=header)
    content = str(r.content)
    content = content[2:-1]
    content = json.loads(content)
    return content


def searchShow(name):
    # Search for a show by its name, return its unique ID
    url = URLBASE + f'/search/tv?query={name}&include_adult=false&language=en-US'

    r = requests.get(url, headers=header)
    content = json.loads(r.content)
    # print(json.dumps(content, indent=2))
    # print(content['total_results'])
    limit = 3
    numResults = content["total_results"]
    if numResults < limit:
        limit = numResults
    # Display results
    print(numResults)
    showResults = []
    print(f'RESULTS FOUND: {numResults}')
    if numResults > limit:
        print(f"SHOWING FIRST {limit} RESULTS")
    '''for i in range(limit):
        print(f'RESULT #{i+1}')
        try:
            show = content['results'][i]
        except IndexError as e:
            # For debugging, uncomment below
            # print(content)
            # print(e)
            print(f"ERROR: Index {i} is out of range")
            return None

        print(f"TITLE: {show['original_name']}")
        try:
            print(f"COUNTRY: {show['origin_country'][0]}")
        except IndexError:
            print(f"COUNTRY: Unknown")
        try:
            print(f"YEAR: {show['first_air_date'][:4]}")
        except IndexError:
            print(f"YEAR: Unknown")
        print('---')'''
    return content
    '''
    choice = input('Enter your selection number: ')
    choice = int(choice)

    show = content['results'][choice - 1]
    return show['id']
    '''

def searchShowDetails(showID):
    # Search the metadata for a unique show ID
    url = URLBASE + f'/tv/{showID}'
    resp = requests.get(url, headers=header)
    content = json.loads(resp.content)

    #print(json.dumps(content, indent=2))
    last_air_date = content["last_air_date"]
    if content["in_production"]:
        # If show is still on the air, override the 'last aired' date
        last_air_date = None

    show = {
        'id': showID,
        'name': content["name"],
        'startDate': content["first_air_date"],
        'endDate': last_air_date
    }
    networks = []
    for netw in content["networks"]:
        network = {
            'id': netw["id"],
            'name': netw["name"],
            'country': netw["origin_country"]
        }
        networks.append(network)
    seasons = content["seasons"]
    genres = content["genres"]
    return show, seasons, networks, genres


def searchEpisode(showID, seasonNum, episodeNum):
    # Search an episode by its show name, season number, and episode number
    # Return dictionary of relevant episode metadata
    # Example input: "X-Files", 2, 4 (season 2, episode 4)
    url = URLBASE + f'/tv/{showID}/season/{seasonNum}'
    resp = requests.get(url, headers=header)
    content = json.loads(resp.content)
    print(content)
    episodes = content["episodes"]
    episodeNum = int(episodeNum)
    selectedEpisode = None
    for i in episodes:
        if i['episode_number'] == episodeNum:
            selectedEpisode = i

    if not selectedEpisode:
        print("ERROR: Episode not found!")
        return None

    dateWatched = datetime.now().strftime('%Y-%m-%d')
    episode = {
        'id': selectedEpisode["id"],
        'name': selectedEpisode["name"],
        'number': selectedEpisode["episode_number"],
        'airDate': selectedEpisode["air_date"],
        'dateWatched': dateWatched
    }

    return episode


def searchSeason(showID, seasonNum):
    # Search for a season by the show's unique ID and the season number
    # Return a dictionary of relevant season metadata
    seasons = searchShowDetails(showID)
    # searchShowDetails() returns details and seasons as a list - discard the details, not required for season table
    seasons = seasons[1]

    selectedSeason = None
    for i in seasons:
        if i['season_number'] == seasonNum:
            selectedSeason = i
    if not selectedSeason:
        print("ERROR: Season not found!")
        return None
    season = {
        'id': selectedSeason['id'],
        'number': selectedSeason['season_number'],
        'airDate': selectedSeason['air_date']
    }
    return season


def getCast(showID, seasonNum, episodeNum, episodeID):
    # showID, seasonNum, and episodeNum are used for the API query
    # episodeID is passed into the function to avoid a repeat query for the show ID
    # since this function always occurs after already searching for a new episode
    url = URLBASE + f'/tv/{showID}/season/{seasonNum}/episode/{episodeNum}/credits'

    resp = requests.get(url, headers=header)
    content = json.loads(resp.content)

    #print(json.dumps(content, indent=2))
    actors = []  # Will be entered into ACTOR table
    appears_in = []   # will be entered into APPEARS_IN table
    for array in content['cast'], content['guest_stars']:
        for castMember in array:
            actor = {
                'id': castMember["id"],
                'name': castMember["name"]
            }
            actors.append(actor)
            appearance = {
                'actorID': castMember["id"],
                'episodeID': episodeID,
                'character': castMember["character"]
            }
            appears_in.append(appearance)

    return actors, appears_in



