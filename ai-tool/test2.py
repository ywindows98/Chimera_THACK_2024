"""
Usage OpenAI Api key from Telekom
"""
import os
import json
from openai import OpenAI
from openai.types.beta.threads.message_create_params import Attachment, AttachmentToolFileSearch


client = OpenAI(
  api_key = os.environ["OPENAI_TOKEN"],
  organization=os.environ["ORGANIZATION"],
)

token = os.environ.get("GITHUB_TOKEN")
endpoint = "https://models.inference.ai.azure.com"
model_name = "gpt-4o"

client = OpenAI(
    base_url=endpoint,
    api_key=token,
)

# stream = client.chat.completions.create(
#     model="gpt-4o",
#     messages=[{"role": "user", "content": "Say this is a test"}],
#     stream=True,
# )
# for chunk in stream:
#     if chunk.choices[0].delta.content is not None:
#         print(chunk.choices[0].delta.content, end="")


# Upload your pdf(s) to the OpenAI API
file = client.files.create(
    file=open('pdf_to_json.pdf', 'rb'),
    purpose='assistants'
)

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
        description='You are a PDF retrieval assistant.',
        instructions="You are a helpful assistant designed to output only JSON. Find information from the text and files provided.",
        tools=[{"type": "file_search"}],
        # response_format={"type": "json_object"}, # Isn't possible with "file_search"
        name='My Assistant Name',
    )

# Add your prompt here
prompt = "What's the total price of the purchase order in PDF? Output in JSON format, like:\n{'price': 123.45}"
client.beta.threads.messages.create(
    thread_id = thread.id,
    role='user',
    content=prompt,
    attachments=[Attachment(file_id=file.id, tools=[AttachmentToolFileSearch(type='file_search')])]
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

# Because the Assistant can't produce JSON (as we're using "file_search"),
# it will likely output text + some JSON code. We can parse and extract just
# the JSON part, and ignore everything else (eg. gpt4o will start with something
# similar to "Of course, here's the parsed text: {useful_JSON_here}")
if res_txt.startswith('```json'):
    res_txt = res_txt[6:]
if res_txt.endswith('```'):
    res_txt = res_txt[:-3]
res_txt = res_txt[:res_txt.rfind('}')+1]
res_txt = res_txt[res_txt.find('{'):]
res_txt.strip()

# Parse the JSON output
data = json.loads(res_txt)

print(res_txt)  # Print the response text to debug the content

try:
    data = json.loads(res_txt)
    print(data)
except json.JSONDecodeError as e:
    print(f"JSON decode error: {e}")

# Delete the file(s) afterward to preserve space (max 100gb/company)
delete_ok = client.files.delete(file.id)