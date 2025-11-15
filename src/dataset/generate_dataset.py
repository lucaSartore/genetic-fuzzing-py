from inspect import findsource
from logging import debug

from pydantic import with_config
from functions_list import FUNCTIONS, FunctionType
from google import genai
from time import sleep
import os
import re
from dotenv import load_dotenv

# loading api key
load_dotenv("./.env")
key = str(os.getenv("GEMINI_API_KEY"))
client = genai.Client(api_key=key)

def main():
    for i, function in enumerate(FUNCTIONS):

        if i <= 5:
            continue

        print(f"{i+1}/{len(FUNCTIONS)} - generating {function['name']}")
        generate_function(function)


def generate_function(func: FunctionType):
    prompt = f"""
    I need you to generate a python function called {func["description"]}
    here is a short description of what the function does: {func["description"]}

    use this template to generate the output:
    
    ```python
    # necessary imports (use only the python standard libraries)

    # you can define other auxiliary functions

    def {func["name"]}(<func args USE STRICT TYPE ANNOTATION>):
        # code

    # add this ad the end of the file
    EXPORT_FUNCTION = {func["name"]}
    ```
    """
    output = use_llm(prompt)
    output = parse_python_code(output)
    verify_python_code(output, func)

    with open(f"./output/{func["name"]}.py", 'w') as f:
        f.write(output)

def parse_python_code(llm_output: str) -> str:
    pattern = r"```python\n(.*?)\n```"
    
    code_blocks = re.findall(pattern, llm_output, re.DOTALL)
    
    blocks = [block.strip() for block in code_blocks]
    assert len(blocks) == 1, "LLM generated multiple output blocks"

    return blocks[0]

def verify_python_code(code: str, func: FunctionType):
    try:
        exec(code)
    except Exception as e:
        raise Exception(f"LLM generated code failed to execute: {e}")


    pattern1 = f"EXPORT_FUNCTION = {func['name']}"
    pattern2 = f"EXPORT_FUNCTION={func['name']}"

    assert code.find(pattern1) or code.find(pattern2), "llm did not export the correct function"

def use_llm(input: str, max_attempt = 4) -> str:
    try:
        answer = client.models.generate_content(
            model='gemini-2.5-flash', contents=input
        )
        if answer.text != None:
            return answer.text
        raise Exception(f"llm did not give an answer: {answer}")
    except:
        if max_attempt <= 0:
            raise
        sleep(60)
        return use_llm(input, max_attempt-1)


if __name__ == "__main__":
    main()
