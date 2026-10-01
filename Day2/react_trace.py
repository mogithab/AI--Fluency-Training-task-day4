"""Day 2: Correct ReAct trace for the scholarship comparison."""

import sys
from pathlib import Path

# Use Day1 tools without moving any Day2 files into Day1
DAY1_FOLDER = Path(__file__).resolve().parent.parent / "Day1"
sys.path.insert(0, str(DAY1_FOLDER))

from tools import get_course_fee, calculator


QUESTION = (
    "Which is cheaper: CS101 and AI202 with a 10% scholarship, "
    "or all three courses with a 25% scholarship? By how much?"
)

print("QUESTION:", QUESTION, "\n")

print("--- the agent's actions and observations ---")

# Step 1: Get course fees
cs101 = get_course_fee("CS101")
print("step 1: get_course_fee({'course_code': 'CS101'}) ->", cs101)

ai202 = get_course_fee("AI202")
print("step 1: get_course_fee({'course_code': 'AI202'}) ->", ai202)

ds303 = get_course_fee("DS303")
print("step 1: get_course_fee({'course_code': 'DS303'}) ->", ds303)

# Step 2: Calculate first option
option1 = calculator("(12000 + 18000) * 0.9")
print("step 2: calculator({'expression': '(12000 + 18000) * 0.9'}) ->", option1)

# Step 3: Calculate second option
option2 = calculator("(12000 + 18000 + 15000) * 0.75")
print(
    "step 3: calculator({'expression': '(12000 + 18000 + 15000) * 0.75'}) ->",
    option2
)

# Step 4: Calculate difference
difference = calculator("33750 - 27000")
print(
    "step 4: calculator({'expression': '33750 - 27000'}) ->",
    difference
)

answer = (
    "Taking CS101 and AI202 with the 10% scholarship costs "
    "Rs. 27,000, which is Rs. 6,750 cheaper than all three courses "
    "at Rs. 33,750."
)

print("\nFINAL ANSWER:", answer)