from google.cloud import bigquery
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Set up BigQuery client
client = bigquery.Client()

# Example query to fetch driver standings data
query = """
    SELECT
        driverCode,
        race,
        points
    FROM
        your_dataset.your_table
    WHERE
        season = 2024
    ORDER BY
        driverCode,
        race
"""

try:
    # Execute the query
    query_job = client.query(query)

    # Convert query results to a Pandas DataFrame
    results_df = query_job.to_dataframe()

    # Pivot the data to create a wide table
    results_pivot = results_df.pivot(index='driverCode', columns='race', values='points')

    # Optionally, sort drivers by their total points
    results_pivot['total_points'] = results_pivot.sum(axis=1)
    results_pivot = results_pivot.sort_values(by='total_points', ascending=False).drop(columns='total_points')

    # Plotting using Seaborn
    plt.figure(figsize=(12, 10))
    sns.heatmap(results_pivot, cmap='Blues', annot=True, fmt='.1f', linewidths=.5)
    plt.title('Driver Standings Heatmap - Season 2024')
    plt.xlabel('Race')
    plt.ylabel('Driver')
    plt.xticks(rotation=45)
    plt.yticks(rotation=0)
    plt.tight_layout()
    plt.show()

except Exception as e:
    print(f"Error fetching or processing data: {str(e)}")