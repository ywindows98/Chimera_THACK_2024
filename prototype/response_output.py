import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

data_frame_path = "user_dataset/current_data.csv"

# Load data
df = pd.read_csv(data_frame_path)

# Unique species
species = df['Species'].unique()

# Colors for species
colors = plt.cm.get_cmap('viridis', len(species))(np.arange(len(species)))

# Create 3D plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Plot each species
for idx, spec in enumerate(species):
    species_data = df[df['Species'] == spec]
    ax.scatter(species_data['SepalLengthCm'], species_data['SepalWidthCm'], species_data['PetalLengthCm'], 
               color=colors[idx], label=spec)

# Labels and legend
ax.set_xlabel('Sepal Length (cm)')
ax.set_ylabel('Sepal Width (cm)')
ax.set_zlabel('Petal Length (cm)')
ax.legend(loc='best')

# Save the plot
plt.savefig('./figures/3d_scatter_plot.png', transparent=True)
