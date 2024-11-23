import os
import pandas as pd
import matplotlib.pyplot as plt
from openai import OpenAI

token = os.environ.get("GITHUB_TOKEN")
endpoint = "https://models.inference.ai.azure.com"
model_name = "gpt-4o"

client = OpenAI(
    base_url=endpoint,
    api_key=token,
)

# Функция для отправки текста в GPT-4o
def analyze_with_gpt(data_text, user_query):
    prompt = f"""
    You are a data analyst. Here is the dataset in CSV format:
    {data_text}

    The user has requested the following analysis:
    {user_query}

    Analyze the dataset and provide insights. If possible, suggest visualizations (e.g., scatter plot, bar chart, etc.).
    """
    response = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant specialized in data analysis.",
            },
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model=model_name,
    )
    return response.choices[0].message.content

# Обработка CSV-файла и пользовательского запроса
def process_file_and_query(file_path, user_query):
    # Загрузка файла CSV
    try:
        df = pd.read_csv(file_path)
        print("Файл успешно загружен!")
    except Exception as e:
        print(f"Ошибка загрузки файла: {e}")
        return
    
    # Преобразуем данные в текст для GPT
    data_text = df.head().to_string(index=False)
    
    # Отправка запроса в GPT
    gpt_response = analyze_with_gpt(data_text, user_query)
    
    print("\nОтвет GPT:")
    print(gpt_response)
    
    # Пример визуализации данных на основе текста GPT
    if "scatter plot" in gpt_response.lower():
        try:
            # Создаём пример графика (адаптируйте под конкретный запрос)
            plt.scatter(df[df.columns[0]], df[df.columns[1]])
            plt.xlabel(df.columns[0])
            plt.ylabel(df.columns[1])
            plt.title("Пример Scatter Plot")
            plt.show()
        except Exception as e:
            print(f"Ошибка при создании графика: {e}")

# Пример использования
if __name__ == "__main__":
    # Путь к CSV-файлу (замените на свой файл)
    file_path = r"C:\Users\admin\Chimera_THACK_2024\ai-tool\Iris.csv"  
    # file_path = os.path.join("Chimera_THACK_2024", "iris_dataset", "Iris.csv")
    user_query = "Please, Analyze the Dataset - iris and make the scatter plot."
    
    process_file_and_query(file_path, user_query)
