import openai
import utils


# extract_information calls chat_gpt's models and passes the document to ask it extract all import financial data
def extract_information(financial_text: str, format_path: str, api_key="", model="gpt-3.5-turbo", max_tokens=1000):

    openai.api_key = api_key

    format = utils.read_format(format_path)

    response = openai.chat.completions.create(
        model=model,
          messages=[
              {"role": "system",
               "content": "You are an assistant. "},
              {"role": "user", "content": f"Please map the data from here { financial_text } to fit this json format { format }. Please make sure all numbers are adjusted to be fully numerical value (for example: 20000 thousand would be 20000000) and the data is from the most recent quarter"}
          ],
          max_tokens=max_tokens,
          n=1,
          stop=None,
          temperature=0.5

    )

    return response.choices[0].message.content





# This will have a model look over the data and give an overview of what the data says
def analytical_overview(json_data_path: str, api_key="", model="gpt-3.5-turbo", max_tokens=1000):
    
    openai.api_key = api_key

    data = utils.json_to_string(json_data_path)

    format = utils.read_format('formats/analytical_response.txt')


    response = openai.chat.completions.create(
        model=model,
          messages=[
              {"role": "system",
               "content": "You are an assistant. Please give a summary regarding the three financial statements here and their data "},
              {"role": "user", "content": f"Please write a summary about these financial statements { data }"}
          ],
          max_tokens=max_tokens,
          n=1,
          stop=None,
          temperature=0.5

    )

    return response.choices[0].message.content


# Function sends the text data to gpt to see if it thinks it is an income statement or not
def check_income_statement(financial_text: str, api_key="", model="gpt-3.5-turbo", max_tokens=5):
        
    openai.api_key = api_key

    response = openai.chat.completions.create(
    model=model,
        messages=[
            {"role": "system",
            "content": "You are an assistant. "},
            {"role": "user", "content": f" If this is a statement of income, such that income is in the title, output yes, else output no, nothing else: { financial_text }"}
        ],
        max_tokens=max_tokens,
        n=1,
        stop=None,
        temperature=0.5

    )

    result = response.choices[0].message.content.strip().lower()
    
    return result == "yes"