import pypandoc
import PyPDF2
import json
import openpyxl
import pandas as pd
import csv
import os
import shutil

class FileToTxtConverter:
    @staticmethod
    def pdf_to_txt(file_path, output_file):
        try:
            with open(file_path, 'rb') as pdf_file:
                reader = PyPDF2.PdfReader(pdf_file)
                with open(output_file, 'w', encoding='utf-8') as txt_file:
                    for page in reader.pages:
                        txt_file.write(page.extract_text() + '\n')
            print(f"PDF converted to TXT: {output_file}")
        except Exception as e:
            print(f"Error converting PDF: {e}")

    @staticmethod
    def json_to_txt(file_path, output_file):
        try:
            with open(file_path, 'r', encoding='utf-8') as json_file:
                data = json.load(json_file)
                with open(output_file, 'w', encoding='utf-8') as txt_file:
                    txt_file.write(json.dumps(data, indent=4, ensure_ascii=False))
            print(f"JSON converted to TXT: {output_file}")
        except Exception as e:
            print(f"Error converting JSON: {e}")

    @staticmethod
    def csv_to_txt(file_path, output_file):
        try:
            with open(file_path, 'r', encoding='utf-8') as csv_file:
                reader = csv.reader(csv_file)
                with open(output_file, 'w', encoding='utf-8') as txt_file:
                    for row in reader:
                        txt_file.write(','.join(row) + '\n')
            print(f"CSV converted to TXT: {output_file}")
        except Exception as e:
            print(f"Error converting CSV: {e}")

    @staticmethod
    def xlsx_to_txt(file_path, output_file):
        try:
            df = pd.read_excel(file_path, sheet_name='Sheet1', index_col=0)
            with open(output_file, 'w') as outfile:
                df.to_string(outfile)
        except Exception as e:
            print(f"Error converting XLXS: {e}")

    @staticmethod
    def general_to_txt(file_path, output_file, input_format=None):
        try:
            pypandoc.convert_file(file_path, 'plain', outputfile=output_file)
            print(f"{input_format.upper()} converted to TXT: {output_file}")
        except Exception as e:
            print(f"Error converting {input_format.upper()}: {e}")

    @staticmethod
    def convert_to_txt(file_path: str, output_directory: str = "data/"):
        is_convert = True

        if not os.path.exists(output_directory):
            os.makedirs(output_directory, exist_ok=True)

        ext = os.path.splitext(file_path)[1].lower()
        output_file = output_directory + os.path.splitext(file_path)[0] + ".txt"

        if ext == ".pdf":
            FileToTxtConverter.pdf_to_txt(file_path, output_file)
        elif ext == ".json":
            FileToTxtConverter.json_to_txt(file_path, output_file)
        elif ext == ".csv":
            FileToTxtConverter.csv_to_txt(file_path, output_file)
        elif ext in [".xlsx"]:
            FileToTxtConverter.xlsx_to_txt(file_path, output_file)
        elif ext in [".docx", ".odt", ".html", ".md", ".epub"]:
            FileToTxtConverter.general_to_txt(file_path, output_file, input_format=ext[1:])
        elif ext == '.txt':
            shutil.copy(file_path, output_file)
            print(f"File {file_path} copied to {output_file}")
        else:
            print(f"File format {ext} is not supported.")
            return "False"

# Example usage
# file_paths = [
#     r"Iris.csv",
#     r"pdf_to_json.pdf",
#     r'sample1.json',
#     r'xlsx_to_txt.xlsx',
#     r'simple.txt'

# ]

# for file_path in file_paths:
#     is_convert = FileToTxtConverter.convert_to_txt(file_path)