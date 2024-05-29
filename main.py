import llm_calls
import utils
import json
from tqdm import tqdm

def main():
    # Extract financial text from PDF

    api_key = input("Please enter your api key (no extra spaces): ")

    financial_text = utils.extract_text_by_page("test_pdfs/AMZN-Q1-2024-Earnings-Release.pdf")

    financial_data = {}

    progress_bar = tqdm(total=len(financial_text), desc="Processing Pages")


    
    for page in financial_text:
        if utils.is_cash_flows(page):
            json_data = llm_calls.extract_information(page, 'formats/cash_flows.txt', api_key)
            utils.parse_gpt(json_data, 'return_data/cash_flows.json')
        
        if utils.is_balance_sheets(page):
            json_data = llm_calls.extract_information(page, 'formats/balance_sheets.txt', api_key)
            utils.parse_gpt(json_data, 'return_data/balance_sheets.json')

        if utils.is_income_statement(page):
            json_data = llm_calls.extract_information(page, 'formats/income_statements.txt', api_key)
            utils.parse_gpt(json_data, 'return_data/income_statements.json')

        # increment loop bar
        progress_bar.update(1)

    progress_bar.close()


    

if __name__ == "__main__":
    main()
