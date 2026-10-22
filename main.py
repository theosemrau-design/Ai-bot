import os
import sys
import argparse
import json
from dotenv import load_dotenv
from openai import OpenAI
from prompts import system_prompt
from call_functions import *
from config import MAX_TOOL_CALLS

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()

messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": args.user_prompt},
]

load_dotenv()
api_key = os.environ.get("OPENROUTER_API_KEY")
if api_key == None or not api_key:
    raise RuntimeError("The api key wasn't found or is incorrect. Please add the key to your .env file with this sheme: OPENROUTER_API_KEY='your-key' and replace your-key with your actual key.")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)
for _ in range(MAX_TOOL_CALLS):
    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
        tools=available_functions,
        temperature=0,
    )

    if response.usage == None or not response.usage:
        raise RuntimeError()

    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {response.usage.prompt_tokens}")
        print(f"Response tokens: {response.usage.completion_tokens}")

    message = response.choices[0].message
    messages.append(message)
    if message.tool_calls:
        for tool_call in message.tool_calls:
            function_args = json.loads(tool_call.function.arguments or "{}")
            result_message = call_function(tool_call=tool_call, verbose=args.verbose)
            if not result_message.get('content'):
                raise Exception("Error: content is empty. Function call failed")
            messages.append(result_message)
            if args.verbose:
                print(f"-> {result_message['content']}")
    else:
        print(f"Final response: {message.content}")
        sys.exit(0)
print(f"Maximum tool calls reached({MAX_TOOL_CALLS}). Ending program")
sys.exit(1)