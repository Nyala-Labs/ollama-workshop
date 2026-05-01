#!/usr/bin/env python3
"""
04_local_tool_calling.py

Let a local model decide when it should call a Python function.
"""

from __future__ import annotations

import os

from dotenv import load_dotenv
from ollama import Client, ResponseError

load_dotenv()

# Tool calling works best with a tool-capable model.
# If your default model does not call tools reliably, try qwen2.5:0.5b or llama3.1.
MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5:0.5b")
HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")

USER_QUESTION = (
    "Compare the weather in Singapore and San Francisco, then tell me which city "
    "sounds warmer for a light jacket."
)


def get_weather(city: str) -> str:
    """
    Get a pretend weather report for a city.

    Args:
        city: The city the user asked about.

    Returns:
        A short weather summary that our demo model can reason over.
    """

    forecasts = {
        "singapore": "Singapore is 31C with high humidity and scattered clouds.",
        "san francisco": "San Francisco is 16C with cool wind and light fog.",
        "new york": "New York is 22C with mild sun and a light breeze.",
        "tokyo": "Tokyo is 19C with clear skies and dry air.",
    }

    return forecasts.get(
        city.strip().lower(),
        f"I do not have a weather report for {city}. Try Singapore, San Francisco, New York, or Tokyo.",
    )


def main() -> None:
    client = Client(host=HOST)

    # available_tools is the bridge between a tool name from the model and
    # the real Python function we want to execute.
    available_tools = {
        "get_weather": get_weather,
    }

    messages = [
        {
            "role": "system",
            "content": (
                "You are a helpful weather assistant. Use the weather tool whenever "
                "you need city conditions before answering."
            ),
        },
        {"role": "user", "content": USER_QUESTION},
    ]

    print(f"Using model: {MODEL}")
    print(f"Ollama host: {HOST}")
    print("\nUser question:")
    print(USER_QUESTION)

    try:
        while True:
            response = client.chat(
                model=MODEL,
                messages=messages,
                tools=[get_weather],
                options={"temperature": 0},
            )

            messages.append(response.message)

            if not response.message.tool_calls:
                print("\nFinal answer:\n")
                print(response.message.content)
                break

            for tool_call in response.message.tool_calls:
                tool_name = tool_call.function.name
                arguments = tool_call.function.arguments or {}

                print(f"\nTool call: {tool_name}({arguments})")

                tool_function = available_tools.get(tool_name)
                if tool_function is None:
                    tool_result = f"Unknown tool: {tool_name}"
                else:
                    tool_result = tool_function(**arguments)

                print(f"Tool result: {tool_result}")

                messages.append(
                    {
                        "role": "tool",
                        "tool_name": tool_name,
                        "content": str(tool_result),
                    }
                )
    except ResponseError as error:
        print(f"Ollama returned an error: {error.error}")
        print(
            f"Did you remember to start the Ollama app and run `ollama run {MODEL}`?"
        )
        print(
            "If the model does not support tool calling well, switch MODEL to a tool-capable one."
        )
    except Exception as error:
        print(f"Tool-calling demo failed: {error}")
        print(
            f"Did you remember to start the Ollama app and run `ollama run {MODEL}`?"
        )


if __name__ == "__main__":
    main()
