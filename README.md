# lume_demo

PDF Reader Design:


1. Takes in and reads pdf by page
2. Takes each page and parses it to determine if it has relevant financial information.
    If it does, it converts it to a standard and appropriate json using chat gpt.
    If it doesn't, the page is disregarded.
3. Once all of the pages are scanned, the important financial data is consolidated to a single json financial_data.json in the return data folder
4. That data is passed back to the llm with a pre-provided structure (can be found in the formats directory) which synthesizes the information for the user


The page by page design of this was in order to eliminate api costs so that 10+ pages worth of tokens were being processed and also to lower the context for each request to get more accurate data.
