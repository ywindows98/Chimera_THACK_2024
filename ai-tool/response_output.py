import pandas as pd
import matplotlib.pyplot as plt

# Example DataFrame creation
# df = pd.DataFrame({
#     'SepalLengthCm': [...],
#     'SepalWidthCm': [...],
#     'PetalLengthCm': [...],
#     'PetalWidthCm': [...],
#     'Species': [...]
# })

# Generate a scatter plot
def plot_iris_scatter(df, x_column, y_column, hue_column):
    # Create a color map for different species
    colors = {'Iris-setosa': 'red', 'Iris-versicolor': 'green', 'Iris-virginica': 'blue'}
    
    # Plotting
    plt.figure(figsize=(10, 6))
    for species, group in df.groupby(hue_column):
        plt.scatter(group[x_column], group[y_column], 
                    label=species, color=colors[species], alpha=0.7)
    
    plt.title('Iris Dataset Scatter Plot')
    plt.xlabel(x_column)
    plt.ylabel(y_column)
    plt.legend(title=hue_column)
    plt.grid(True)
    plt.show()

# Call the function
plot_iris_scatter(df, 'SepalLengthCm', 'SepalWidthCm', 'Species')
