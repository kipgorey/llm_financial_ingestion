import pdfplumber
import re
import json
import tabula
import llm_calls


# Not used, but useful function to extract complete text of document
def extract_text(path: str) -> str:
    text = ""

    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            text += page.extract_text()

    return text


# Function to extract the text to string from each page of a PDF and return as a list of the pages
def extract_text_by_page(path: str) -> list:
    pages_text = []

    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            pages_text.append(page.extract_text())

    return pages_text


# Reads the given format from the standard format text file, keeps code cleaner
def read_format(file_path: str):

    with open(file_path, 'r') as file:
        return file.read()
    


# Parses the final gpt output for a json output, then writes it to give .json file
def parse_gpt(input_string, output_filename):
    def find_json_objects(string):
        stack = []
        json_objects = []
        start = 0

        for i, char in enumerate(string):
            if char == '{':
                if not stack:
                    start = i
                stack.append(char)
            elif char == '}':
                if stack:
                    stack.pop()
                    if not stack:
                        json_objects.append(string[start:i+1])
        return json_objects

    json_objects = find_json_objects(input_string)
    
    if json_objects:
        json_string = json_objects[0]
        
        try:
            json_data = json.loads(json_string)
            
            with open(output_filename, 'w') as json_file:
                json.dump(json_data, json_file, indent=4)
            
        except json.JSONDecodeError:
            print("Failed to decode JSON.")
    else:
        print("No JSON object found in the input string.")


# Function allows me to combine one or more json files into a single, largerone
def combine_specific_json_files(files, output_file):
    combined_data = {}

    for file in files:
        with open(file, 'r') as f:
            data = json.load(f)
            # Use the file name without extension as the key
            key = file.split('/')[-1].replace('.json', '')
            combined_data[key] = data

    with open(output_file, 'w') as outfile:
        json.dump(combined_data, outfile, indent=4)


# Converts json at a specific path to a string
def json_to_string(file_path):
    with open(file_path, 'r') as file:
        json_string = file.read()
    return json_string


# Returns true of false if the text provided is an income statement
def is_income_statement(page_text: str, api_key: str):
    keywords = ['income', 'net income', 'tax']
    has_keywords = all(keyword in page_text.lower() for keyword in keywords)
    has_both = 'Income' in page_text

    if has_keywords and has_both:
        return llm_calls.check_income_statement(page_text, api_key)


# Returns true or false if the text provided is a balance sheet
def is_balance_sheets(page_text: str):
    keywords = ['balance sheets', 'current assets', 'goodwill']
    return all(keyword in page_text.lower() for keyword in keywords)


# Returns true of alse if the text provided is a statement of cash flows
def is_cash_flows(page_text: str):
    keywords = ['net income', 'amortization', 'investing activities', 'operating activities']
    return all(keyword in page_text.lower() for keyword in keywords)
