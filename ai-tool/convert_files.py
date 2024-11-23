import pypandoc
import PyPDF2
import json
import openpyxl
import pandas as pd
import csv
import os
import shutil

class Converter:
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
    def get_format(file_path: str) -> str: 
        return os.path.splitext(file_path)[1].lower()
    
    @staticmethod
    def convert_to_txt(file_path: str, output_directory: str = "data/") -> bool:
        is_convert = True

        if not os.path.exists(output_directory):
            os.makedirs(output_directory, exist_ok=True)

        ext = Converter.get_format(file_path)
        output_file = output_directory + os.path.splitext(file_path)[0] + ".txt"

        if ext == ".pdf":
            Converter.pdf_to_txt(file_path, output_file)
        elif ext == ".json":
            Converter.json_to_txt(file_path, output_file)
        elif ext == ".csv":
            Converter.csv_to_txt(file_path, output_file)
        elif ext in [".xlsx"]:
            Converter.xlsx_to_txt(file_path, output_file)
        elif ext in [".docx", ".odt", ".html", ".md", ".epub"]:
            Converter.general_to_txt(file_path, output_file, input_format=ext[1:])
        elif ext == '.txt':
            shutil.copy(file_path, output_file)
            print(f"File {file_path} copied to {output_file}")
        else:
            print(f"File format {ext} is not supported.")
            return is_convert

    @staticmethod
    def txt_to_dataframe(file_path: str, file_format: str) -> tuple:
        df = pd.DataFrame()

        if file_format == ".txt":
            df = pd.read_csv(file_path)
            df = df.drop([0, 1]).reset_index(drop=True)

        elif file_format == ".csv":
            df = pd.read_csv(file_path)

        elif file_format == '.json':
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
            try:
                df = pd.DataFrame([data])
            except:
                df = pd.json_normalize(data)

        elif file_format == ".xlsx":
            df = pd.read_excel(file_path, sheet_name='Sheet1')
            df = df.drop([0, 1]).reset_index(drop=True)

        return df, df.columns.to_list(), df.dtypes.to_list()

# EXAMPLE USAGE OF CONVERTER CLASS
# file_paths = [
#     "example_data/Iris.csv",
#     "example_data/sample1.json",
#     "example_data/xlsx_to_txt.xlsx",
#     "example_data/Iris.txt"
# ]

# for file_path in file_paths: 
#     is_convert = Converter.convert_to_txt(file_path)

#     format = Converter.get_format(file_path)
#     print("File Format: ", format)

#     df, attribute_names, data_types = Converter.txt_to_dataframe(file_path, format)
#     print("Attribute Names:", attribute_names)
#     print("Data Types:", data_types)
#     print("Is DataFrame:", type(df))
#     print("DataFrame:")
#     print(df)
    
