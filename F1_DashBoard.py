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
    
    # Pivot the DataFrame to get the desired shape
    pivot_df = results_df.pivot(index='driverCode', columns='race', values='points')
    
    # Add a column for total points
    pivot_df['Total Points'] = pivot_df.sum(axis=1)
    
    # Sort the drivers by their total points
    pivot_df = pivot_df.sort_values(by='Total Points', ascending=False)
    
    # Sort the columns based on the round number
    race_order = results_df[['race', 'round']].drop_duplicates().set_index('race').sort_values('round').index.tolist()
    race_order.append('Total Points')  # Ensure 'Total Points' is the last column
    pivot_df = pivot_df[race_order]
    
    # Plot the heatmap using Plotly
    fig = px.imshow(
        pivot_df,
        text_auto=True,
        aspect='auto',  # Automatically adjust the aspect ratio
        color_continuous_scale=[[0, 'rgb(255, 204, 204)'],  # Light red
                                [0.25, 'rgb(255, 102, 102)'],
                                [0.5, 'rgb(255, 51, 51)'],
                                [0.75, 'rgb(204, 0, 0)'],
                                [1, 'rgb(153, 0, 0)']],
        labels={'x': 'Race', 'y': 'Driver', 'color': 'Points'}  # Change hover texts
    )
    fig.update_xaxes(title_text='')  # Remove axis titles
    fig.update_yaxes(title_text='')
    fig.update_yaxes(tickmode='linear')  # Show all ticks, i.e. driver names
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightGrey', showline=False, tickson='boundaries')  # Show horizontal grid only
    fig.update_xaxes(showgrid=False, showline=False)  # And remove vertical grid
    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)')  # White background
    fig.update_layout(coloraxis_showscale=False)  # Remove legend
    fig.update_layout(xaxis=dict(side='top'))  # x-axis on top
    fig.update_layout(margin=dict(l=0, r=0, b=0, t=0))  # Remove border margins
    fig.show()

if __name__ == "__main__":
    main()
