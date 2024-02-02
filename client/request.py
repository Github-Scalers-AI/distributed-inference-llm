import json

import requests


def send_sample_request():
    input_prompt = "Explain about the milkyway galaxy to a 5 year old."
    prompt = f"system_prompt: You are a teacher. prompt:{input_prompt}"
    sample_input = {"prompt": prompt, "stream": True}

    output = requests.post(
        "http://localhost:30800/generate", json=sample_input, stream=True
    )
    print(output.status_code)
    for line in output.iter_lines():
        text = json.loads(line.decode("utf-8"))["text"]
        print(text, end="")


send_sample_request()
