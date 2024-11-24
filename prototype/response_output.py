import pandas as pd
import matplotlib.pyplot as plt

data_frame_path = "current_data.csv"

df = pd.read_csv(data_frame_path)

co2_by_make = df.groupby('Make')['CO2 Emissions(g/km)'].mean().sort_values()
plt.figure(figsize=(12, 8))
co2_by_make.plot(kind='bar', color='skyblue')
plt.title('Average CO2 Emissions by Auto Manufacturer')
plt.xlabel('Auto Manufacturer')
plt.ylabel('CO2 Emissions (g/km)')
plt.xticks(rotation=45, ha="right")
plt.tight_layout()

file_name = 'co2_emissions_by_auto_manufacturer.png'
plt.savefig('./figures/' + file_name, transparent=True)
plt.close()
