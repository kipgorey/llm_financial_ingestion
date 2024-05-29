import pdfplumber
import re
import json
import tabula


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

    print('testing')

    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            pages_text.append(page.extract_text())

    return pages_text


# Reads the given format from the standard format text file, keeps code cleaner
def read_format(file_path: str):

    with open(file_path, 'r') as file:
        return file.read()
    


# parses the final gpt output for a json output, then writes it to give .json file
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
        # Assuming we want the first JSON object found
        json_string = json_objects[0]
        
        try:
            # Parse the JSON string
            json_data = json.loads(json_string)
            
            # Write the JSON data to a file
            with open(output_filename, 'w') as json_file:
                json.dump(json_data, json_file, indent=4)
            
            print(f"JSON data has been written to {output_filename}")
        except json.JSONDecodeError:
            print("Failed to decode JSON.")
    else:
        print("No JSON object found in the input string.")


def create_json(filename: str):
    data = {}
    with open(filename, "w") as json_file:
        json.dump(data, json_file)



def is_income_statement(page_text: str):
    keywords = ['consolidated', 'income', 'net']
    return all(keyword in page_text.lower() for keyword in keywords)


def is_balance_sheets(page_text: str):
    keywords = ['balance sheets', 'current assets', 'goodwill']
    return all(keyword in page_text.lower() for keyword in keywords)


def is_cash_flows(page_text: str):
    keywords = ['net income', 'amortization']
    return all(keyword in page_text.lower() for keyword in keywords)
