import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

data_frame_path = "default/Bird_strikes.csv"

df = pd.read_csv(data_frame_path)

# Plot 1: Incidents by Aircraft Type
plt.figure(figsize=(10, 6))
df['AircraftType'].value_counts().plot(kind='bar')
plt.title('Number of Incidents by Aircraft Type')
plt.xlabel('Aircraft Type')
plt.ylabel('Number of Incidents')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('./figures/incidents_by_aircraft_type.png', transparent=True)
plt.close()

# Plot 2: Wildlife Strikes by Wildlife Species
plt.figure(figsize=(10, 6))
df['WildlifeSpecies'].value_counts().head(10).plot(kind='bar')
plt.title('Top 10 Wildlife Strikes by Species')
plt.xlabel('Wildlife Species')
plt.ylabel('Number of Strikes')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('./figures/wildlife_strikes_by_species.png', transparent=True)
plt.close()

# Plot 3: Damage Distribution
plt.figure(figsize=(10, 6))
df['Damage'].value_counts().plot(kind='bar')
plt.title('Distribution of Damage Levels')
plt.xlabel('Damage Level')
plt.ylabel('Frequency')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('./figures/damage_distribution.png', transparent=True)
plt.close()
