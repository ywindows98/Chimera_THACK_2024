import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

data_frame_path = "current_data.csv"

df = pd.read_csv(data_frame_path)

co2_by_make = df.groupby('Make')['CO2 Emissions(g/km)'].mean().sort_values()
plt.figure(figsize=(12, 8))
co2_by_make.plot(kind='bar', color='skyblue')
plt.ylabel('Average CO2 Emissions (g/km)')
plt.title('Average CO2 Emissions by Auto Manufacturer')
plt.xticks(rotation=90)
plt.tight_layout()

plt.savefig('./figures/co2_emissions_by_make.png', transparent=True)
