import json
import time
import requests

BASE = "http://localhost:11434"
MODEL = "qwen2.5:1.5b"
PROMPT = "In three sentences, explain what an AI agent is."


def list_models():
    data = requests.get(f"{BASE}/api/tags").json()
    print("\n=== /api/tags ===")
    for model in data.get("models", []):
        size_gb = model["size"] / 1e9
        print(f"{model['name']}: {size_gb:.2f} GB")


def loaded_models():
    data = requests.get(f"{BASE}/api/ps").json()
    print("\n=== /api/ps ===")
    for model in data.get("models", []):
        print(
            f"{model.get('name')} | "
            f"size={model.get('size', 0) / 1e9:.2f} GB | "
            f"processor={model.get('details', {}).get('family', 'n/a')}"
        )


def generate_once():
    payload = {
        "model": MODEL,
        "prompt": PROMPT,
        "stream": False
    }

    start = time.perf_counter()

    response = requests.post(
        f"{BASE}/api/generate",
        json=payload
    )

    elapsed = time.perf_counter() - start
    data = response.json()

    print("\n=== /api/generate ===")
    print(data.get("response", ""))

    eval_count = data.get("eval_count", 0)

    print(f"Elapsed: {elapsed:.2f} s")
    print(f"Tokens: {eval_count}")

    if elapsed > 0:
        print(f"Tokens/sec: {eval_count / elapsed:.2f}")


def chat_streaming():
    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "user",
                "content": PROMPT
            }
        ],
        "stream": True
    }

    start = time.perf_counter()
    first_token_time = None

    response = requests.post(
        f"{BASE}/api/chat",
        json=payload,
        stream=True
    )

    print("\n=== /api/chat streaming ===")

    for line in response.iter_lines():
        if not line:
            continue

        data = json.loads(line)

        if first_token_time is None:
            first_token_time = time.perf_counter()

        message = data.get("message", {})
        print(message.get("content", ""), end="", flush=True)

    end = time.perf_counter()

    print()

    if first_token_time:
        print(f"TTFT: {first_token_time - start:.2f} s")

    print(f"Total time: {end - start:.2f} s")


def openai_compatible():
    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "user",
                "content": PROMPT
            }
        ],
        "temperature": 0
    }

    response = requests.post(
        f"{BASE}/v1/chat/completions",
        headers={
            "Authorization": "Bearer ollama"
        },
        json=payload
    )

    data = response.json()

    print("\n=== /v1/chat/completions ===")
    print(
        data["choices"][0]["message"]["content"]
    )


if __name__ == "__main__":
    list_models()
    generate_once()
    chat_streaming()
    openai_compatible()
    loaded_models()