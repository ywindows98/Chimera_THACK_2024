import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

data_frame_path = "default/students.csv"
df = pd.read_csv(data_frame_path)

unique_classes = df['race_ethnicity'].unique()
colors = plt.cm.jet(np.linspace(0, 1, len(unique_classes)))

fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')

for i, unique_class in enumerate(unique_classes):
    class_data = df[df['race_ethnicity'] == unique_class]
    ax.scatter(class_data['math_score'], class_data['reading_score'], class_data['writing_score'],
               color=colors[i], label=unique_class)

ax.set_xlabel('Math Score')
ax.set_ylabel('Reading Score')
ax.set_zlabel('Writing Score')
ax.legend()

plt.savefig('./figures/3d_plot.png', transparent=True)
plt.show()
