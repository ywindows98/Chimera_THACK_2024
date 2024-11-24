### Dependencies
numpy
pandas
streamlit
streamlit_chat
scipy
matplotlib
openai
dotenv
sqlite3

### Command to run the application locally from the prototype directory
streamlit run llm_sml.py --theme.base="light" --server.address 127.0.0.1

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