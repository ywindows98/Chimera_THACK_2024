import pandas as pd
from openai import OpenAI
from dotenv import load_dotenv
import re
import subprocess
import os
import sys

# A class representing a client to interact with OpenAI API
class Client:
    def __init__(self, api_key: str, org_key: str):
        self.api_key = api_key # OpenAI API key
        self.org_key = org_key # OpenAI organization key

    def get_client(self):
        # Returns an instance of the OpenAI client
        return OpenAI(api_key=self.api_key, organization=self.org_key)

# A class to represent the user input (prompt)
class User:
    def __init__(self, prompt: str, file_path: str):
        self.prompt = prompt # Stores the user prompt
        self.file_path = file_path # Stores the user dataset

    def get_prompt(self):
        # Returns the user prompt
        return self.prompt

    def get_file_path(self):
        # Returns the user dataset
        return self.file_path

# A class to manage the creation and use of an assistant in OpenAI API
class Assistant:
    def __init__(self, name: str, description: str, instructions: str, model: str):
        self.name = name  # Name of the assistant
        self.description = description  # Description of the assistant's role
        self.instructions = instructions  # Custom instructions for the assistant
        self.model = model  # Model name to use
        self.assistant = None  # Placeholder for the created assistant

    def create_assistant(self, client: OpenAI):
        # Creates the assistant in the OpenAI API
        self.assistant = client.beta.assistants.create(
            name=self.name,
            description=self.description,
            instructions=self.instructions,
            model=self.model
        )

    def get_assistant(self):
        # Returns the assistant if created, otherwise raises an exception
        if self.assistant is not None:
            return self.assistant
        else:
            raise NotImplemented("Assistant not created.")

# A class to manage conversation threads with the OpenAI API
class Thread:
    def __init__(self):
        self.thread = None # Placeholder for the thread

    def create_thread(self, client: OpenAI, result: str, prompt: str):
        # Creates a new thread using the user's prompt and dataset result
        self.thread = client.beta.threads.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt
                },
                {
                    "role": "user",
                    "content": result
                }
            ]
        )

    def get_thread(self):
        # Returns the thread if created, otherwise raises an exception
        if self.thread is not None:
            return self.thread
        else:
            raise NotImplemented("Thread not created.")


# Function to execute a thread run and wait for the result
def run(client, thread, assistant: Assistant.get_assistant, timeout: int):
    return client.beta.threads.runs.create_and_poll(
        thread_id=thread.id,
        assistant_id=assistant.id,
        timeout=timeout
    )

# Function to load a dataset and extract its attributes and data types
def load_dataset(file_path: str):
    try:
        df = pd.read_csv(file_path) # Load the dataset as a pandas DataFrame
        print(f"Dataset {file_path} read success")
        attributes = [str(attr) for attr in df.columns.tolist()] # Column names
        data_types = [str(dtype) for dtype in df.dtypes.tolist()] # Data types of columns
        result = ''
        for attribute, data_type in zip(attributes, data_types):
            result += 'attribute: ' + attribute + ' is ' + data_type + ' data type\n'

    except FileNotFoundError:
        # Handle missing dataset file
        raise FileNotFoundError("Dataset not found.")

    except Exception as e:
        # Handle other exceptions
        raise e

    else:
        # Return the formatted result stringя
        return result

def create_py_file(messages, file_path):
    # Extract Python code blocks from the assistant messages
    pattern = r"```python\n(.*?)```"
    matches = re.findall(pattern, messages[0].content[0].text.value, re.DOTALL)
    output_file = "response_output.py"

    # Write the extracted code to a Python file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("import numpy as np\nimport pandas as pd\nimport matplotlib.pyplot as plt\n")
        f.write(matches[0])

    # Replace placeholder file path in the code with the actual dataset file path
    with open(output_file, 'r') as file:
        file_content = file.read()

    file_content = re.sub(r"data_frame_path\s*=\s*'[^']*'",
                          f'data_frame_path = "{file_path}"', file_content)

    with open(output_file, 'w') as file:
        file.write(file_content)

    # Clean up any pre-existing files in the `figures` folder
    folder_path = './figures'
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)
        elif os.path.isdir(file_path):
            os.rmdir(file_path)

    # Execute the Python file
    subprocess.run(["python", output_file])

# Function to handle the query, process the dataset, and interact with the OpenAI API
def send_query(file_path, prompt, model_name="gpt-4o"):
    # Validate inputs
    # if type(file_path) is not str:
    #     raise FileNotFoundError("Wrong file path.")
    if type(prompt) is not str:
        raise TypeError("Wrong prompt type.")

    if file_path is None:
        dataset_pattern = {
            "student": "./example_datasets/students.csv",
            "co2": "./example_datasets/co2.csv",
            "iris": "./example_datasets/iris.csv"
        }

        try:
            for dataset_name, dataset_path in dataset_pattern.items():
                if re.search(dataset_name, prompt):
                    file_path = dataset_path
                    break
        except Exception as e:
            raise e

    # Create a User object with the given prompt and file path
    user = User(prompt=prompt, file_path=file_path)

    # Load environment variables for API keys
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    org_key = os.getenv("ORGANIZATION")

    # Load the dataset and get its summary
    dataset = load_dataset(user.get_file_path())

    # Create an OpenAI client
    client = Client(api_key=api_key, org_key=org_key).get_client()

    # Read assistant description and instructions from files
    with open("./description", "r", encoding='utf-8') as f:
        description = f.read()
    with open("./instructions", "r", encoding='utf-8') as f:
        instructions = f.read()

    # Create and initialize an assistant
    assistant = Assistant(name=model_name, description=description, instructions=instructions
                          , model=model_name)
    assistant.create_assistant(client=client)

    # Create a thread with the dataset summary and user prompt
    thread = Thread()
    thread.create_thread(client=client, result=dataset, prompt=user.get_prompt())

    # Run the assistant and wait for the response
    run(client=client, thread=thread.get_thread(), assistant=assistant.get_assistant(), timeout=180)
    print("Reques sent")

    # Get the response messages from the thread
    response = client.beta.threads.messages.list(thread_id=thread.get_thread().id)
    print("Response get")
    messages = [message for message in response]

    # Create a Python file from the response and execute it
    create_py_file(messages=messages, file_path=file_path)

    return 1

# if __name__ == "__main__":
#     prompt = "I want to see a bar graph comparing math and writing grades as a function of parental education. And That the xlabel be sprayed at a 45 degree angle"
#     send_query(file_path="./students.csv", prompt=prompt)

