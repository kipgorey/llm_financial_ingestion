# lume_demo




Thought Process:



    - Most important Question > How will I extract the information and then convert it to the standard format
        a - Giving the entire document to GPT would ensure that all of the data is properly converted, but trusting the ML model to directly copy and paste data is less than ideal
        b - Parsing to find where certain financial data is might work better but because of the non-uniform formatting of each document, that leaves the possibility that data is missed in this process
    
    As of now, a seems the better option as it ensures all data is captured and with improved models, this system will only improve whereas option b will not improve with the release of better LLM's