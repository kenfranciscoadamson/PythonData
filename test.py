import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Sample data
data = {
    'timestamp': [
        '2023-05-01 08:15:00', '2023-05-01 08:30:00', '2023-05-01 09:00:00',
        '2023-05-01 10:00:00', '2023-05-01 10:30:00', '2023-05-01 11:00:00',
        '2023-05-01 12:00:00', '2023-05-01 13:00:00', '2023-05-01 14:00:00',
        '2023-05-02 08:00:00', '2023-05-02 08:30:00', '2023-05-02 09:00:00',
        '2023-05-02 09:30:00', '2023-05-02 10:00:00', '2023-05-02 11:00:00',
        '2023-05-02 12:00:00', '2023-05-02 13:00:00', '2023-05-02 14:00:00',
        '2023-05-03 08:00:00', '2023-05-03 08:30:00', '2023-05-03 09:00:00',
        '2023-05-03 09:30:00', '2023-05-03 10:00:00', '2023-05-03 11:00:00',
        '2023-05-03 12:00:00', '2023-05-03 13:00:00'
    ],
    'player_id': [
        1, 2, 3, 1, 4, 2, 3, 1, 2, 3, 1, 2, 4, 3, 1, 2, 4, 3, 4, 1, 2, 3, 4, 1, 2
    ],
    'action': [
        'login', 'login', 'gather_wood', 'trade', 'craft', 'quest', 'gather_ore',
        'pvp', 'logout', 'login', 'gather_wood', 'trade', 'craft', 'pvp',
        'quest', 'gather_ore', 'trade', 'pvp', 'logout', 'login', 'gather_wood',
        'trade', 'quest', 'pvp', 'logout'
    ],
    'location': [
        'Bridgewatch', 'Fort Sterling', 'Lymhurst', 'Thetford', 'Carleon',
        'Fort Sterling', 'Bridgewatch', 'Lymhurst', 'Fort Sterling', 'Thetford',
        'Lymhurst', 'Fort Sterling', 'Carleon', 'Lymhurst', 'Thetford', 'Fort Sterling',
        'Carleon', 'Bridgewatch', 'Carleon', 'Thetford', 'Lymhurst', 'Bridgewatch',
        'Carleon', 'Bridgewatch', 'Fort Sterling'
    ]
}

# Convert data into a DataFrame
df = pd.DataFrame(data)

# Convert timestamp to datetime format
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Example of exploratory data analysis (EDA)

# Plotting player login times
plt.figure(figsize=(10, 6))
df['timestamp'].hist(bins=30, edgecolor='black')
plt.title('Player Login Times')
plt.xlabel('Timestamp')
plt.ylabel('Count')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Example of creating a heatmap of player actions by location
location_counts = df['location'].value_counts().reset_index()
location_counts.columns = ['location', 'count']

plt.figure(figsize=(12, 8))
sns.barplot(x='location', y='count', data=location_counts.head(10))
plt.title('Top 10 Locations by Player Activity')
plt.xlabel('Location')
plt.ylabel('Player Count')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Example of economic insights - analyzing player actions
action_counts = df['action'].value_counts().reset_index()
action_counts.columns = ['action', 'count']

plt.figure(figsize=(12, 8))
sns.barplot(x='action', y='count', data=action_counts)
plt.title('Player Actions')
plt.xlabel('Action')
plt.ylabel('Count')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Additional analysis and visualizations can be added based on your specific dataset and objectives

# Save or display your findings in the portfolio format