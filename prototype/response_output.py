import pandas as pd
import matplotlib.pyplot as plt

# Define path to your CSV file
data_frame_path = "user_dataset/current_data.csv"

# Load the data into a DataFrame
df = pd.read_csv(data_frame_path)

# Group the data by 'Make' and sum the CO2 emissions
emissions_by_make = df.groupby('Make')['CO2 Emissions(g/km)'].sum().sort_values()

# Plot the bar graph
plt.figure(figsize=(12, 8))
emissions_by_make.plot(kind='bar')
plt.title('CO2 Emissions by Auto Manufacturer')
plt.xlabel('Manufacturer')
plt.ylabel('Total CO2 Emissions (g/km)')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()

# Save plot to a file
plt.savefig('./figures/co2_emissions_by_manufacturer.png', transparent=True)
plt.close()
