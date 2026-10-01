"""Day 3: ReAct agent with guards."""

import json
import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "Day_1")
    )
)

from config import client, MODEL, banner
from my_tools import TOOLS, TOOL_FUNCTIONS


SYSTEM_PROMPT = (
    "You are a college assistant. "
    "When the user mentions a local HTML file, use the exact local filename. "
    "For example, if the user says notice.html, call read_webpage with "
    "url='notice.html'. Do not add Day_3/ or convert it to an example.com URL. "
    "Use calculator for arithmetic. "
    "Never guess numbers that should come from a file."
)


MAX_TOOL_CHARS = 1500
CHAR_BUDGET = 30000


def agent(question, max_steps=6, verbose=True):

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": question}
    ]

    seen_calls = {}
    total_chars = 0

    for step in range(1, max_steps + 1):

        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=TOOLS,
            temperature=0
        )

        message = response.choices[0].message

        if not message.tool_calls:
            return message.content.strip()

        messages.append({
            "role": "assistant",
            "content": message.content or "",
            "tool_calls": [
                {
                    "id": call.id,
                    "type": "function",
                    "function": {
                        "name": call.function.name,
                        "arguments": call.function.arguments
                    }
                }
                for call in message.tool_calls
            ]
        })

        for call in message.tool_calls:

            name = call.function.name
            arguments = {}

            try:
                arguments = json.loads(
                    call.function.arguments or "{}"
                )

                # Detect repeated identical tool calls
                call_key = (
                    name,
                    json.dumps(arguments, sort_keys=True)
                )

                seen_calls[call_key] = seen_calls.get(call_key, 0) + 1

                if seen_calls[call_key] >= 3:
                    result = (
                        "Stopped repeated tool call: "
                        f"{name}({arguments})"
                    )

                else:

                    function = TOOL_FUNCTIONS.get(name)

                    if function is None:
                        result = (
                            f"Unknown tool: {name}. "
                            f"Available: {list(TOOL_FUNCTIONS)}"
                        )
                    else:
                        result = function(**arguments)

            except json.JSONDecodeError as error:
                result = f"Argument error: {error}"

            except TypeError as error:
                result = f"Argument error: {error}"

            # Limit tool output
            result = str(result)[:MAX_TOOL_CHARS]

            total_chars += len(result)

            if total_chars > CHAR_BUDGET:
                return "Stopped: character budget exceeded."

            if verbose:
                print(
                    f"   step {step}: "
                    f"{name}({arguments}) -> "
                    f"{result[:120]}"
                )

            messages.append({
                "role": "tool",
                "tool_call_id": call.id,
                "content": result
            })

    return "Stopped: maximum steps reached without a final answer."


if __name__ == "__main__":

    banner("MY AGENT (guards on)")

    questions = [
        (
            "Read notice.html and tell me the total fee for CS101 "
            "and AI202 after the merit scholarship."
        ),
        (
            "Read fees.html and tell me the fee for CS101."
        ),
        (
            "Read big.html and tell me how many students are listed."
        )
    ]

    for question in questions:
        print("\nQ:", question)
        print("A:", agent(question))