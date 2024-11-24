"""
Usage OpenAI Api key from Telekom
"""
import os
import json
import re
from openai import OpenAI
from openai.types.beta.threads.message_create_params import Attachment, AttachmentToolFileSearch

from convert_files import Converter
from service_messages import description, instructions, service_promt

client = OpenAI(
  api_key = os.environ["OPENAI_TOKEN"],
  organization=os.environ["ORGANIZATION"],
)

# file_path = 'data/Iris.pdf'
# file = client.files.create(
#     file=open(file_path, 'rb'),
#     purpose='assistants'
# )

# Create thread
thread = client.beta.threads.create()

# Create an Assistant (or fetch it if it was already created). It has to have
# "file_search" tool enabled to attach files when prompting it.
def get_assistant():
    for assistant in client.beta.assistants.list():
        if assistant.name == 'My Assistant Name':
            return assistant

    # No Assistant found, create a new one
    return client.beta.assistants.create(
        model='gpt-4o',
        description=description,
        instructions=instructions,
        tools=[{"type": "file_search"}],
        # response_format={"type": "json_object"}, # Isn't possible with "file_search"
        name='My Assistant Name',
    )

# Add your prompt here
attr_names = ['Id','SepalLengthCm','SepalWidthCm','PetalLengthCm','PetalWidthCm','Species']
d_types = ["int64", "float64", "flaot64", 'float64', 'float64', 'object']

attr_type = []
attributes = ""
for i in range(len(attr_names)):
    attr_type.append(f"{attr_names[i]} of type {d_types[i]}")
    attributes+=f" {attr_type[i]}, "


file_path = 'Iris.csv'
file_format = Converter.get_format(file_path) 


prompt = str()
prompt += service_promt.format(attributes)
prompt = "Create Python code to generate a scatter plot from the uploaded file. Assume it has been processed using `FileToTxtConverter.convert_to_txt(file_path)` and loaded into a DataFrame as `df`." 
client.beta.threads.messages.create(
    thread_id = thread.id,
    role='user',
    content=prompt,
    # attachments=[Attachment(file_id=file.id, tools=[AttachmentToolFileSearch(type='file_search')])]
)

# Run the created thread with the assistant. It will wait until the message is processed.
run = client.beta.threads.runs.create_and_poll(
    thread_id=thread.id,
    assistant_id=get_assistant().id,
    timeout=300, # 5 minutes
    # response_format={"type": "json_object"}, # Isn't possible
)

# Eg. issue with openai server
if run.status != "completed":
    raise Exception('Run failed:', run.status)

# Fetch outputs of the thread
messages_cursor = client.beta.threads.messages.list(thread_id=thread.id)
messages = [message for message in messages_cursor]

message = messages[0] # This is the output from the Assistant (second message is your message)
assert message.content[0].type == "text"

# Output text of the Assistant
res_txt = message.content[0].text.value
print(res_txt)

pattern = r"```python\n(.*?)```"
matches = re.findall(pattern, res_txt, re.DOTALL)
if matches:
    # Write the extracted Python code to a file
    output_file = "response_output.py"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(matches[0])

    print(f"Python code written to {output_file}")
else:
    print("No valid Python code block found in the response.")

# subprocess.run(["python", output_file])

