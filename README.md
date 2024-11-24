# Chimera Chat AI
Chimera Chat AI is an intelligent assistant designed to process data files provided by users (e.g., CSV, Excel, JSON). Users can input natural language queries such as "Show the average sales by month" or "Compare the profit for 2020 and 2021." The assistant analyzes the data and presents the results through tables, charts, or other visualizations, offering clear and actionable insights. 

![image](https://github.com/user-attachments/assets/ceac45f4-4da9-4a01-8a2a-6bc5a643d163)

## Dependencies
The main dependencies required for the web application can be found in the requirements.txt file. Make sure to install them before running the application.
```
numpy
pandas
streamlit
streamlit_chat
scipy
matplotlib
openai
dotenv
sqlite3
```

## Local Setup Instructions
1. To run the project locally, start by cloning the repository:  
   ```bash
   git clone https://github.com/ywindows98/Chimera_THACK_2024.git
   ```

2. After cloning, install all dependencies listed in the `requirements.txt` file using the following command:  
   ```bash
   pip install -r requirements.txt
   ```

3. Launch the application by running the following command in your terminal:  
   ```bash
   streamlit run llm_sml.py --theme.base="light" --server.address 127.0.0.1
   ```  
   This will open the web project in your default browser.

## Usage
### Data  
Users can upload a dataset in CSV format for processing. The AI assistant will analyze and process the uploaded dataset based on the user’s request.  

### Requests  
If no dataset is uploaded, the AI assistant can automatically select a suitable dataset from its default library based on the keywords provided in the user’s query.  

In the request, users should clearly specify how they want the data to be visualized, such as graphs, charts, or tables. Users can also request multiple visualizations in a single query.  

If the visualization is generated successfully, the results will be displayed in the main section of the application.  

### Feedback  
Users can request the regeneration of a visualization and provide feedback using "like" or "dislike" options.  

All feedback is stored in a database for further analysis and to improve the model's performance.  
