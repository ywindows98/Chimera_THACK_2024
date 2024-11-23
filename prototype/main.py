from openai import OpenAI
from openai.types.beta.threads.message_create_params import Attachment, AttachmentToolFileSearch
import pandas as pd
import re
import subprocess

from dotenv import load_dotenv
import os

load_dotenv()
token = os.getenv("OPENAI_API_KEY")
organization_token = os.getenv("ORGANIZATION")
model_name = "gpt-4o"

file_path = 'students.csv'

try:
    df = pd.read_csv(file_path)
    attributes = [str(attr) for attr in df.columns.tolist()]
    data_types = [str(dtype) for dtype in df.dtypes.tolist()]
    result = ''
    for attribute, data_type in zip(attributes, data_types):
        result += 'attribute: ' + attribute + ' is ' + data_type + ' data type\n'

except Exception as e:
    print(e)
    raise e

print(result)

client = OpenAI(
    # base_url=endpoint,
    api_key=token,
    organization=organization_token
)

assistant = client.beta.assistants.create(
  name="Data analyt",
  description="You have basic information about the dataframe, namely the attribute names and attribute data types. "
              "You need to write code that will process the data and output the important information the user asks for,"
              " if the user has not specified what they want, then select the information you think is important. "
              "Take into account that you don't know how many elements are in the dataframe, "
              "write a universal code that will work with any amount of data in the dataframe. ",
  instructions="1) Dont use seadorn. "
               "2) Use matplotlib and pandas, numpy for data analys. "
               "3) Write code on python in one block. "
               "4) Write only code, without description. "
               "5) Always Make and save allways figures in png file plt.savefig('./figures/'+file_name, transparent=True) with unique file_name. "
               "6) Take into account that you don't know how many elements are in the dataframe, write a universal code that will work with any amount of data in the dataframe. "
               "7) Do not create any mockup of the potential dataset. "
               "8) ode should be easy to use on a dataset, user should be able to just put the csv file."
               "9) Always create a variable data_frame_path = 'path...' at the beginning of the code into which you need to insert the path to the dataframe.",
  model="gpt-4o"
)

thread = client.beta.threads.create(
  messages=[
    {
      "role": "user",
      "content": "I want to get a graph comparing average math scores sorted by the education level of the student's parents"
    },
    {
      "role": "user",
      "content": result
    }
  ]
)

def get_assistant():
    for assistant in client.beta.assistants.list():
        if assistant.name == 'Data analyt':
            return assistant

run = client.beta.threads.runs.create_and_poll(
    thread_id=thread.id,
    assistant_id=get_assistant().id,
    timeout=300
)

messages_cursor = client.beta.threads.messages.list(thread_id=thread.id)
messages = [message for message in messages_cursor]
print(messages)

pattern = r"```python\n(.*?)```"
matches = re.findall(pattern, messages[0].content[0].text.value, re.DOTALL)
output_file = "response_output.py"
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(matches[0])

with open(output_file, 'r') as file:
    file_content = file.read()

# Ищем строку, содержащую data_frame_path и заменяем её на новый путь
file_content = re.sub(r"data_frame_path\s*=\s*'[^']*'", f'data_frame_path = "{file_path}"', file_content)

# Записываем изменения обратно в файл
with open(output_file, 'w') as file:
    file.write(file_content)

folder_path = './figures'
for filename in os.listdir(folder_path):
    file_path = os.path.join(folder_path, filename)
    if os.path.isfile(file_path):
        os.remove(file_path)  # Удаляем файл
    elif os.path.isdir(file_path):
        os.rmdir(file_path)  # Удаляем пустую папку

subprocess.run(["python", output_file])