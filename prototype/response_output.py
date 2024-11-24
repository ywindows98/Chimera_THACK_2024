import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

data_frame_path = "default/default_data.csv"
df = pd.read_csv(data_frame_path)

# Calculate mean math and writing scores by parental education level
mean_scores = df.groupby('parental_level_of_education')[['math_score', 'writing_score']].mean()

# Plot bar graph
ax = mean_scores.plot(kind='bar', figsize=(10, 6))
plt.title('Average Math and Writing Scores by Parental Level of Education')
plt.xlabel('Parental Level of Education')
plt.ylabel('Average Score')
plt.xticks(rotation=45)

# Save figure
plt.savefig('./figures/average_scores_by_parental_education.png', transparent=True)
plt.show()
