import time
import requests

BASE = "http://localhost:11434"

MODELS = [
    "qwen2.5:1.5b",
    "mistral:latest"
]

PROMPTS = [
    "Reply with exactly: OK",
    "In two sentences, what is an AI agent?",
    "A course costs Rs. 18,000 with a 15% scholarship. What is payable? Show the steps.",
]

for model in MODELS:
    print(f"\n=== {model} ===")

    for prompt in PROMPTS:
        start = time.perf_counter()

        r = requests.post(
            f"{BASE}/api/generate",
            json={
                "model": model,
                "prompt": prompt,
                "stream": False
            },
            timeout=120
        )

        elapsed = time.perf_counter() - start
        data = r.json()

        eval_count = data.get("eval_count", 0)
        tok_s = eval_count / elapsed if elapsed else 0
        load_duration = data.get("load_duration", 0) / 1e9

        print(f"\nPrompt: {prompt}")
        print(f"Response: {data.get('response', '').strip()}")
        print(f"Elapsed: {elapsed:.2f} s")
        print(f"Tokens: {eval_count}")
        print(f"Tokens/sec: {tok_s:.2f}")
        print(f"Load duration: {load_duration:.2f} s")