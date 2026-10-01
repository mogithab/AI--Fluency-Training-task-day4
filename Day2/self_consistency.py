"""Day 2, Part C: run the same CoT prompt several times and take the majority answer."""

import sys
from pathlib import Path
from collections import Counter

DAY1_FOLDER = Path(__file__).resolve().parent.parent / "Day1"
sys.path.insert(0, str(DAY1_FOLDER))

from config import client, MODEL, banner
from cot_compare import COT_PROMPT, QUESTIONS

RUNS = 5
TEMPERATURE = 0.8


def final_answer(text):
    for line in reversed(text.splitlines()):
        if "final answer" in line.lower():
            return line.split(":", 1)[-1].strip()

    return text.splitlines()[-1].strip() if text.strip() else "(empty)"


def normalize_answer(answer):
    answer = answer.lower().strip()
    answer = answer.replace(".", "")
    answer = answer.replace(",", "")
    answer = answer.replace("₹", "")
    answer = answer.replace("rs", "")
    return answer.strip()


def run_many(question, runs=RUNS, temperature=TEMPERATURE):
    answers = []

    for attempt in range(1, runs + 1):
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": COT_PROMPT},
                {"role": "user", "content": question},
            ],
            temperature=temperature,
        )

        answer = final_answer(response.choices[0].message.content)

        print(f" run {attempt}: {answer}")

        answers.append(answer)

    return answers


if __name__ == "__main__":
    banner("SELF-CONSISTENCY")

    question = QUESTIONS[0]

    print("QUESTION:", question, "\n")

    answers = run_many(question)

    normalized_answers = [
        normalize_answer(answer)
        for answer in answers
    ]

    winner, count = Counter(normalized_answers).most_common(1)[0]

    original_winner = answers[normalized_answers.index(winner)]

    print(
        f"\nMajority answer ({count} of {len(answers)} runs): "
        f"{original_winner}"
    )