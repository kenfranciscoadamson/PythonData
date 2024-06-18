import os
import requests
from google.cloud import bigquery
import pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup

# Set Up Authentication
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\Kenn\Desktop\Kenn Files\Google Key\bold-gravity-426402-a6-141a6503528e.json"

# Define the dataset and table names
dataset_name = "f1_data"
race_results_table = "race_results"
drivers_standings_table = "drivers_standings"
constructors_standings_table = "constructors_standings"
recent_races_table = "recent_races"
recent_winners_table = "recent_winners"
upcoming_races_table = "upcoming_races"
upcoming_race_table = "upcoming_race"

# Initialize a BigQuery client
client = bigquery.Client()

# Create the dataset if it doesn't exist
dataset_ref = client.dataset(dataset_name)
try:
    client.get_dataset(dataset_ref)
except Exception:
    dataset = bigquery.Dataset(dataset_ref)
    dataset.location = "US"
    client.create_dataset(dataset)
    print(f"Dataset {dataset_name} created.")

def create_table_if_not_exists(table_name, schema):
    table_ref = dataset_ref.table(table_name)
    try:
        client.get_table(table_ref)
    except Exception:
        table = bigquery.Table(table_ref, schema=schema)
        client.create_table(table)
        print(f"Table {table_name} created.")
    return table_ref

def load_data_to_bigquery(dataframe, table_ref):
    try:
        job = client.load_table_from_dataframe(dataframe, table_ref)
        job.result()
        print(f"Data loaded into {table_ref.table_id} successfully.")
    except Exception as e:
        print(f"Error loading data into {table_ref.table_id}: {e}")

# Function to fetch recent F1 news headlines
def fetch_f1_news_headlines():
    news_url = "https://www.formula1.com/en/latest/all.html"
    response = requests.get(news_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        headlines = soup.find_all('p', class_='f1--cc--caption', limit=5)
        headlines_list = [headline.get_text(strip=True) for headline in headlines]
        return headlines_list
    else:
        return ["Failed to fetch F1 news headlines."]

# Function to fetch recent race results
def fetch_recent_race_results():
    url = "http://ergast.com/api/f1/current/last/results.json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        race = data['MRData']['RaceTable']['Races'][0]
        race_name = race['raceName']
        race_date = pd.to_datetime(race['date'])
        race_results = race['Results']
        results_list = [{'Position': result['position'], 
                         'Driver': f"{result['Driver']['givenName']} {result['Driver']['familyName']}", 
                         'Constructor': result['Constructor']['name']} 
                        for result in race_results]
        race_results_df = pd.DataFrame(results_list)
        days_since_race = (datetime.now() - race_date).days
        return race_name, race_date, race_results_df, days_since_race
    else:
        raise Exception(f"Failed to fetch race results data. Status code: {response.status_code}")

# Function to fetch next race details
def fetch_next_race_details():
    url = "http://ergast.com/api/f1/current/next.json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        race = data['MRData']['RaceTable']['Races'][0]
        race_name = race['raceName']
        race_date = pd.to_datetime(race['date'])
        days_until_race = (race_date - datetime.now()).days
        return race_name, race_date, days_until_race
    else:
        raise Exception(f"Failed to fetch next race data. Status code: {response.status_code}")

# Function to fetch driver's standings
def fetch_drivers_standings():
    url = "http://ergast.com/api/f1/current/driverStandings.json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        standings = data['MRData']['StandingsTable']['StandingsLists'][0]['DriverStandings']
        standings_list = [{'Position': standing['position'],
                           'Driver': f"{standing['Driver']['givenName']} {standing['Driver']['familyName']}",
                           'Points': standing['points']} for standing in standings]
        standings_df = pd.DataFrame(standings_list)
        return standings_df
    else:
        raise Exception(f"Failed to fetch driver's standings data. Status code: {response.status_code}")

# Function to fetch constructor's standings
def fetch_constructors_standings():
    url = "http://ergast.com/api/f1/current/constructorStandings.json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        standings = data['MRData']['StandingsTable']['StandingsLists'][0]['ConstructorStandings']
        standings_list = [{'Position': standing['position'],
                           'Constructor': standing['Constructor']['name'],
                           'Points': standing['points']} for standing in standings]
        standings_df = pd.DataFrame(standings_list)
        return standings_df
    else:
        raise Exception(f"Failed to fetch constructor's standings data. Status code: {response.status_code}")

# Function to fetch remaining races
def fetch_remaining_races():
    url = "http://ergast.com/api/f1/current.json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        races = data['MRData']['RaceTable']['Races']
        remaining_races_list = [{'Race': race['raceName'],
                                 'Date': pd.to_datetime(race['date'])} for race in races if pd.to_datetime(race['date']) > datetime.now()]
        remaining_races_df = pd.DataFrame(remaining_races_list)
        return remaining_races_df
    else:
        raise Exception(f"Failed to fetch remaining races data. Status code: {response.status_code}")

# Fetch and display F1 news headlines
print(f"Hello Boss,")
print("Here are some recent F1 updates for you:\n")

f1_news_headlines = fetch_f1_news_headlines()
print("Recent F1 News Headlines:")
for idx, headline in enumerate(f1_news_headlines, 1):
    print(f"{idx}. {headline}")
print()

# Fetch and display recent race results
race_name, race_date, race_results_df, days_since_race = fetch_recent_race_results()
print(f"Recent Race Results - {race_name} (held on {race_date.date()}):\n")
print(race_results_df)
print(f"\nIt has been {days_since_race} days since the last race.\n")

# Fetch and display next race details
next_race_name, next_race_date, days_until_race = fetch_next_race_details()
print(f"The next race is {next_race_name} on {next_race_date.date()}.")
print(f"There are {days_until_race} days left until the next race.\n")

# Fetch and display driver's standings
drivers_standings_df = fetch_drivers_standings()
print("Driver's Championship Standings:\n")
print(drivers_standings_df)

# Fetch and display constructor's standings
constructors_standings_df = fetch_constructors_standings()
print("\nConstructor's Championship Standings:\n")
print(constructors_standings_df)

# Fetch and display remaining races
remaining_races_df = fetch_remaining_races()
print("\nRemaining Races:\n")
print(remaining_races_df)

# Load data into BigQuery

# Define schema for race results table
race_results_schema = [
    bigquery.SchemaField("Position", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("Driver", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("Constructor", "STRING", mode="REQUIRED")
]

# Create race results table and load data
race_results_table_ref = create_table_if_not_exists(race_results_table, race_results_schema)
load_data_to_bigquery(race_results_df, race_results_table_ref)

# Define schema for driver's standings table
drivers_standings_schema = [
    bigquery.SchemaField("Position", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("Driver", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("Points", "STRING", mode="REQUIRED")
]

# Create driver's standings table and load data
drivers_standings_table_ref = create_table_if_not_exists(drivers_standings_table, drivers_standings_schema)
load_data_to_bigquery(drivers_standings_df, drivers_standings_table_ref)

# Define schema for constructor's standings table
constructors_standings_schema = [
    bigquery.SchemaField("Position", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("Constructor", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("Points", "STRING", mode="REQUIRED")
]

# Create constructor's standings table and load data
constructors_standings_table_ref = create_table_if_not_exists(constructors_standings_table, constructors_standings_schema)
load_data_to_bigquery(constructors_standings_df, constructors_standings_table_ref)

# Define schema for remaining races table
remaining_races_schema = [
    bigquery.SchemaField("Race", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("Date", "DATE", mode="REQUIRED")
]

# Create remaining races table and load data
remaining_races_table_ref = create_table_if_not_exists(upcoming_races_table, remaining_races_schema)
load_data_to_bigquery(remaining_races_df, remaining_races_table_ref)

# Fetch recent 5 races results
url = "http://ergast.com/api/f1/current/last/5/results.json"
response = requests.get(url)
if response.status_code == 200:
    data = response.json()
    print("Recent 5 races results data fetched successfully.")
else:
    print(f"Failed to fetch recent 5 races results data. Status code: {response.status_code}")
    data = None  # Assign None to data to indicate failure

# Process recent 5 races results data if available
if data:
    recent_races = data.get('MRData', {}).get('RaceTable', {}).get('Races', [])
    if recent_races:
        recent_races_list = []
        for race in recent_races:
            race_name = race.get('raceName', '')
            date = race.get('date', '')
            circuit_name = race.get('Circuit', {}).get('circuitName', '')
            for result in race.get('Results', []):
                position = result.get('position', '')
                driver = f"{result['Driver']['givenName']} {result['Driver']['familyName']}"
                constructor = result.get('Constructor', {}).get('name', '')
                recent_races_list.append({
                    'race_name': race_name,
                    'date': date,
                    'circuit_name': circuit_name,
                    'position': position,
                    'driver': driver,
                    'constructor': constructor
                })
        recent_races_df = pd.DataFrame(recent_races_list)
        recent_races_df['date'] = pd.to_datetime(recent_races_df['date'])
        print("\nRecent 5 races results:")
        print(recent_races_df)
    else:
        print("No recent races data available.")
else:
    print("No recent 5 races data fetched.")

# Process recent 5 races results data if available
if data:
    recent_races = data.get('MRData', {}).get('RaceTable', {}).get('Races', [])
    if recent_races:
        recent_races_list = []
        for race in recent_races:
            race_name = race.get('raceName', '')
            date = race.get('date', '')
            circuit_name = race.get('Circuit', {}).get('circuitName', '')
            for result in race.get('Results', []):
                position = result.get('position', '')
                driver = f"{result['Driver']['givenName']} {result['Driver']['familyName']}"
                constructor = result.get('Constructor', {}).get('name', '')
                recent_races_list.append({
                    'race_name': race_name,
                    'date': date,
                    'circuit_name': circuit_name,
                    'position': position,
                    'driver': driver,
                    'constructor': constructor
                })
        recent_races_df = pd.DataFrame(recent_races_list)
        recent_races_df['date'] = pd.to_datetime(recent_races_df['date'])
        print("\nRecent 5 races results:")
        print(recent_races_df)
    else:
        print("No recent races data available.")
else:
    print("No recent 5 races data fetched.")


# Define schema for recent races table
recent_races_schema = [
    bigquery.SchemaField("race_name", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("date", "DATE", mode="REQUIRED"),
    bigquery.SchemaField("circuit_name", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("position", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("driver", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("constructor", "STRING", mode="REQUIRED")
]

# Create recent races table and load data
recent_races_table_ref = create_table_if_not_exists(recent_races_table, recent_races_schema)
load_data_to_bigquery(recent_races_df, recent_races_table_ref)

# Fetch recent winners for the upcoming race since 2021
upcoming_race_url = "http://ergast.com/api/f1/current/next.json"
upcoming_race_response = requests.get(upcoming_race_url)
if upcoming_race_response.status_code == 200:
    upcoming_race_data = upcoming_race_response.json()
    upcoming_race_name = upcoming_race_data['MRData']['RaceTable']['Races'][0]['raceName']
    print(f"Upcoming race: {upcoming_race_name}")
else:
    raise Exception(f"Failed to fetch upcoming race data. Status code: {upcoming_race_response.status_code}")

recent_winners_url = f"http://ergast.com/api/f1/races?limit=1000"
recent_winners_response = requests.get(recent_winners_url)
if recent_winners_response.status_code == 200:
    recent_winners_data = recent_winners_response.json()
    print("Recent winners data fetched successfully.")
else:
    raise Exception(f"Failed to fetch recent winners data. Status code: {recent_winners_response.status_code}")

# Process recent winners data
recent_winners = recent_winners_data['MRData']['RaceTable']['Races']
recent_winners_list = []
for race in recent_winners:
    if race['raceName'] == upcoming_race_name and int(race['season']) >= 2021:
        winner = race['Results'][0]['Driver']['familyName']
        date = race['date']
        recent_winners_list.append({'race_name': race['raceName'], 'season': race['season'], 'winner': winner, 'date': date})
recent_winners_df = pd.DataFrame(recent_winners_list)
recent_winners_df['date'] = pd.to_datetime(recent_winners_df['date'])
print("\nRecent winners:")
print(recent_winners_df)

# Define schema for recent winners table
recent_winners_schema = [
    bigquery.SchemaField("race_name", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("season", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("winner", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("date", "DATE", mode="REQUIRED")
]

# Create recent winners table and load data
recent_winners_table_ref = create_table_if_not_exists(recent_winners_table, recent_winners_schema)
load_data_to_bigquery(recent_winners_df, recent_winners_table_ref)

# Fetch upcoming 5 races
url = "http://ergast.com/api/f1/current/next.json"
response = requests.get(url)
if response.status_code == 200:
    data = response.json()
    print("Upcoming 5 races data fetched successfully.")
else:
    raise Exception(f"Failed to fetch upcoming 5 races data. Status code: {response.status_code}")

# Process upcoming 5 races data
upcoming_races = data['MRData']['RaceTable']['Races']
upcoming_races_list = []
for race in upcoming_races:
    race_name = race['raceName']
    date = race['date']
    circuit_name = race['Circuit']['circuitName']
    location = race['Circuit']['location']
    upcoming_races_list.append({'race_name': race_name, 'date': date, 'circuit_name': circuit_name, 'location': location})
upcoming_races_df = pd.DataFrame(upcoming_races_list)
upcoming_races_df['date'] = pd.to_datetime(upcoming_races_df['date'])
print("\nUpcoming 5 races:")
print(upcoming_races_df)

# Define schema for upcoming races table
upcoming_races_schema = [
    bigquery.SchemaField("race_name", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("date", "DATE", mode="REQUIRED"),
    bigquery.SchemaField("circuit_name", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("location", "STRING", mode="REQUIRED")
]

# Create upcoming races table and load data
upcoming_races_table_ref = create_table_if_not_exists(upcoming_races_table, upcoming_races_schema)
load_data_to_bigquery(upcoming_races_df, upcoming_races_table_ref)

# Fetch more info about the upcoming race
upcoming_race_url = "http://ergast.com/api/f1/current/next.json"
upcoming_race_response = requests.get(upcoming_race_url)
if upcoming_race_response.status_code == 200:
    upcoming_race_data = upcoming_race_response.json()
    upcoming_race_name = upcoming_race_data['MRData']['RaceTable']['Races'][0]['raceName']
    print(f"Upcoming race: {upcoming_race_name}")
else:
    raise Exception(f"Failed to fetch upcoming race data. Status code: {upcoming_race_response.status_code}")

# Process more info about the upcoming race
upcoming_race = upcoming_race_data['MRData']['RaceTable']['Races'][0]
upcoming_race_list = []
upcoming_race_list.append({'race_name': upcoming_race_name, 'date': upcoming_race['date'], 'circuit_name': upcoming_race['Circuit']['circuitName'], 'location': upcoming_race['Circuit']['location'], 'podiums_since_2021': upcoming_race['Results'][0]['Driver']['familyName']})
upcoming_race_df = pd.DataFrame(upcoming_race_list)
upcoming_race_df['date'] = pd.to_datetime(upcoming_race_df['date'])
print("\nMore info about the upcoming race:")
print(upcoming_race_df)

# Define schema for upcoming race table
upcoming_race_schema = [
    bigquery.SchemaField("race_name", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("date", "DATE", mode="REQUIRED"),
    bigquery.SchemaField("circuit_name", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("location", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("podiums_since_2021", "STRING", mode="REQUIRED")
]

# Create upcoming race table and load data
upcoming_race_table_ref = create_table_if_not_exists(upcoming_race_table, upcoming_race_schema)
load_data_to_bigquery(upcoming_race_df, upcoming_race_table_ref)

print("All data loaded into BigQuery successfully.")
