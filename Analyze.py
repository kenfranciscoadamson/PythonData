import pandas as pd
import matplotlib.pyplot as plt

# Load dataset
data = pd.read_csv('data.csv')

# Descriptive statistics
print(data.describe())

#Visualize distribution of a column
plt.hist(data['column_name'], bins=30)
plt.title('Distribution of column_name')
plt.xlabel('Value')
plt.ylabel('Frequency')
plt.show()

# Scatter plot to visualize relationships
plt.scatter(data['column_x'], data['column_y'])
plt.title('column_x vs column_y')
plt.xlabel('column_x')
plt.ylabel('column_y')
plt.show()

# Correlation matrix
print(data.corr())
