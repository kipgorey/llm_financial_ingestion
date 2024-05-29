import llm_calls
import utils
import json
from tqdm import tqdm

def main():

    # Get user openai api key
    api_key = input("Please enter your openai api key (no extra spaces): ")

    # Extract the text from the pdf
    financial_text = utils.extract_text_by_page("test_pdfs/pdf3.pdf")

    files = []

    progress_bar = tqdm(total=len(financial_text), desc="Processing Pages")
    
    for page in financial_text:
        # increment loop bar
        progress_bar.update(1)

        if utils.is_cash_flows(page):
            json_data = llm_calls.extract_information(page, 'formats/cash_flows.txt', api_key)
            utils.parse_gpt(json_data, 'return_data/cash_flows.json')
            files.append('return_data/cash_flows.json')
        
        elif utils.is_balance_sheets(page):
            json_data = llm_calls.extract_information(page, 'formats/balance_sheets.txt', api_key)
            utils.parse_gpt(json_data, 'return_data/balance_sheets.json')
            files.append('return_data/balance_sheets.json')

        elif utils.is_income_statement(page, api_key):
            json_data = llm_calls.extract_information(page, 'formats/income_statements.txt', api_key)
            utils.parse_gpt(json_data, 'return_data/income_statements.json')
            files.append('return_data/income_statements.json')

    progress_bar.close()

    # conjoin 3 statement jsons
    utils.combine_specific_json_files(files, 'return_data/financial_data.json')


    # Provide the user with an analytical overview
    response = llm_calls.analytical_overview('return_data/financial_data.json', api_key)

    print(f"\nGPT: { response }")


if __name__ == "__main__":
    main()
