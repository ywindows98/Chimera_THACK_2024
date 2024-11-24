# Chimera Chat AI
Chimera Chat AI is an intelligent assistant designed to process data files provided by users (e.g., CSV, Excel, JSON). Users can input natural language queries such as "Show the average sales by month" or "Compare the profit for 2020 and 2021." The assistant analyzes the data and presents the results through tables, charts, or other visualizations, offering clear and actionable insights. 

![image](https://github.com/user-attachments/assets/0814860c-bf75-4edf-b0c9-e9ee5354d05d)


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
Dataset for processing can be uploaded by the user or set by the user prompt by writing the desired default data set name.

### Requests
When desired dataset for processing is determined, the user can write a request for the LLM. The user has to describe how he wants the data to be visualized. 
The user can also request multiple plots from the assistant.

If the visualization is successfully generated, it will be displayed on the main section of the application.

### Rating
The user can also request to regenerate the visualization and rate it with like or dislike.
Rated messages are stored in the database for potential problem analysis and improvement of the model.
