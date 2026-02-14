import os
import argparse
from call_function import available_functions, call_function
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt

load_dotenv()

api_key = os.environ.get("GEMINI_API_KEY")
if api_key == None:
    raise RuntimeError("API key not found")

client = genai.Client(api_key=api_key)

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()

messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

def main():
    for _ in range(20):
        response = client.models.generate_content(model = "gemini-2.5-flash", 
                                                    contents = messages,
                                                    config=types.GenerateContentConfig(tools = [available_functions],system_instruction=system_prompt))
        
        candidates = response.candidates
        if candidates:
            for candidate in candidates:
                messages.append(candidate)
        
        if not response.usage_metadata:
            raise RuntimeError("Failed API request")
        
        if args.verbose:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
        
        function_calls = response.function_calls

        function_response_list = []

        if function_calls:
            for function_call in function_calls:

                function_call_result = call_function(function_call)
                if len(function_call_result.parts) == 0:
                    raise Exception("Function call returned an empty result")
                
                function_response = function_call_result.parts[0].function_response
                if function_response == None:
                    raise Exception("Function call response returned 'None'")
                
                function_response_list.append(function_call_result.parts[0])

                if args.verbose:
                    print(f"-> {function_call_result.parts[0].function_response.response}")
            messages.append(types.Content(role="user", parts=function_response_list))

        if not function_calls:
            print(response.text)
            return
        
        if _ == 19:
            print("Iterated 20 times without reaching a definitive resolution")
            print(response.text)


if __name__ == "__main__":
    main()
