import os
from dotenv import load_dotenv
from openai import OpenAI
import argparse
from prompts import system_prompt
from call_function import available_functions, call_function
import json

def main():
    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if api_key is None:
        raise RuntimeError("No API key found")
    
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    parser = argparse.ArgumentParser(description="Chatbor")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()


    messages=[
        {
            "role": "system", "content": system_prompt
        },
        {
            "role": "user",
            "content": args.user_prompt,
        }
    ]

    generate_content(client, messages, args)

def generate_content(client: OpenAI, messages: list, args: dict) -> None: 
    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
        temperature=0,
        tools = available_functions,
    )

    if args.verbose:
        print(f"User prompt:{args.user_prompt}")
        if response.usage is not None:
            print(f"Prompt tokens: {response.usage.prompt_tokens}")
            print(f"Response tokens: {response.usage.completion_tokens}")
        else:
            raise RuntimeError("Error with API response")

    message = response.choices[0].message

    if message.tool_calls:
        for tool_call in message.tool_calls:
            function_args = json.loads(tool_call.function.arguments or "{}")
            function_name = tool_call.function.name
            result_message = call_function(tool_call)
            if not result_message['content']:
                raise Exception("Tool call should have a non-empty content")
            if args.verbose:
                print(f"-> {result_message['content']}")
    else:
        response_text = message.content
        print(response_text)


if __name__ == "__main__":
    main()
