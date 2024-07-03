# for Plot2

import pandas as pd
import plotly.express as px
import requests

# Base URL for Ergast API
BASE_URL = 'https://ergast.com/api/f1'

def fetch_race_schedule(year):
    endpoint = f"{BASE_URL}/{year}.json"
    try:
        response = requests.get(endpoint)
        if response.status_code == 200:
            data = response.json()
            races = data['MRData']['RaceTable']['Races']
            return races
        else:
            print(f"Failed to retrieve race schedule. Status code: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {str(e)}")
        return None

def fetch_race_results(year, round):
    endpoint = f"{BASE_URL}/{year}/{round}/results.json"
    try:
        response = requests.get(endpoint)
        if response.status_code == 200:
            data = response.json()
            races = data['MRData']['RaceTable']['Races']
            if races:
                results = races[0]['Results']
                return results
            else:
                print(f"No race results found for round {round}")
                return None
        else:
            print(f"Failed to retrieve race results for round {round}. Status code: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {str(e)}")
        return None

def main():
    year = 2024
    races = fetch_race_schedule(year)
    if not races:
        print("No races found.")
        return
    
    all_results = []
    
    for race in races:
        round_no = race['round']
        race_name = race['raceName']
        print(f"Fetching results for {race_name} (Round {round_no})")
        results = fetch_race_results(year, round_no)
        
        if results:
            for result in results:
                driver_code = result['Driver']['code']
                points = float(result['points'])
                all_results.append({'round': round_no, 'race': race_name, 'driverCode': driver_code, 'points': points})
    
    if not all_results:
        print("No race results found for the season.")
        return
    
    results_df = pd.DataFrame(all_results)
    
    # Ensure all expected races are included as columns
    expected_races = [race['raceName'] for race in races]
    
    # Plot 1: All columns having data
    pivot_df_data = results_df.pivot(index='driverCode', columns='race', values='points')
    
    # Plot 2: All columns regardless of data
    pivot_df_all = results_df.pivot(index='driverCode', columns='race', values='points').reindex(columns=expected_races, fill_value=0)
    
    # Add a column for total points
    pivot_df_data['Total Points'] = pivot_df_data.sum(axis=1)
    pivot_df_all['Total Points'] = pivot_df_all.sum(axis=1)
    
    # Sort the drivers by their total points
    pivot_df_data = pivot_df_data.sort_values(by='Total Points', ascending=False)
    pivot_df_all = pivot_df_all.sort_values(by='Total Points', ascending=False)
    
    # Plot the heatmaps using Plotly
    
    # Plot 1: All columns having data
    fig1 = px.imshow(
        pivot_df_data,
        text_auto=True,
        aspect='auto',
        color_continuous_scale=[[0, 'rgb(204, 229, 255)'],
                                [0.25, 'rgb(153, 204, 255)'],
                                [0.5, 'rgb(102, 178, 255)'],
                                [0.75, 'rgb(51, 153, 255)'],
                                [1, 'rgb(0, 128, 255)']],
        labels={'x': 'Race', 'y': 'Driver', 'color': 'Points'}
    )
    fig1.update_layout(title='Plot 1: All columns having data')
    fig1.show()
    
    # Plot 2: All columns regardless of data
    fig2 = px.imshow(
        pivot_df_all,
        text_auto=True,
        aspect='auto',
        color_continuous_scale=[[0, 'rgb(204, 229, 255)'],
                                [0.25, 'rgb(153, 204, 255)'],
                                [0.5, 'rgb(102, 178, 255)'],
                                [0.75, 'rgb(51, 153, 255)'],
                                [1, 'rgb(0, 128, 255)']],
        labels={'x': 'Race', 'y': 'Driver', 'color': 'Points'}
    )
    fig2.update_layout(title='Plot 2: All columns regardless of data')
    fig2.show()

if __name__ == "__main__":
    main()
