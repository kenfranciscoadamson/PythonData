# for Plot1

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
    pivot_df = results_df.pivot(index='driverCode', columns='race', values='points').reindex(columns=expected_races)
    
    # Add a column for total points
    pivot_df['Total Points'] = pivot_df.sum(axis=1)
    
    # Sort the drivers by their total points
    pivot_df = pivot_df.sort_values(by='Total Points', ascending=False)
    
    # Plot the heatmap with only columns having data
    fig1 = px.imshow(
        pivot_df.dropna(axis=1, how='all'),
        text_auto=True,
        aspect='auto',
        color_continuous_scale=[[0, 'rgb(204, 229, 255)'], [0.25, 'rgb(153, 204, 255)'], [0.5, 'rgb(102, 178, 255)'], [0.75, 'rgb(51, 153, 255)'], [1, 'rgb(0, 128, 255)']],
        labels={'x': 'Race', 'y': 'Driver', 'color': 'Points'}
    )
    fig1.update_xaxes(title_text='')
    fig1.update_yaxes(title_text='')
    fig1.update_yaxes(tickmode='linear')
    fig1.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightGrey', showline=False, tickson='boundaries')
    fig1.update_xaxes(showgrid=False, showline=False)
    fig1.update_layout(plot_bgcolor='rgba(0,0,0,0)')
    fig1.update_layout(coloraxis_showscale=False)
    fig1.update_layout(xaxis=dict(side='top'))
    fig1.update_layout(margin=dict(l=0, r=0, b=0, t=0))
    fig1.show()

    # Plot the heatmap with all columns
    fig2 = px.imshow(
        pivot_df,
        text_auto=True,
        aspect='auto',
        color_continuous_scale=[[0, 'rgb(204, 229, 255)'], [0.25, 'rgb(153, 204, 255)'], [0.5, 'rgb(102, 178, 255)'], [0.75, 'rgb(51, 153, 255)'], [1, 'rgb(0, 128, 255)']],
        labels={'x': 'Race', 'y': 'Driver', 'color': 'Points'}
    )
    fig2.update_xaxes(title_text='')
    fig2.update_yaxes(title_text='')
    fig2.update_yaxes(tickmode='linear')
    fig2.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightGrey', showline=False, tickson='boundaries')
    fig2.update_xaxes(showgrid=False, showline=False)
    fig2.update_layout(plot_bgcolor='rgba(0,0,0,0)')
    fig2.update_layout(coloraxis_showscale=False)
    fig2.update_layout(xaxis=dict(side='top'))
    fig2.update_layout(margin=dict(l=0, r=0, b=0, t=0))
    fig2.show()

if __name__ == "__main__":
    main()
