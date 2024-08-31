import google.generativeai as genai
import os
import json
import time


def get_response(prompt: str) -> (str, int, int):
    #genai.configure(api_key=os.getenv("GEMINI_API_KEY"))``
    genai.configure(api_key="AIzaSyDy2GONTyXZTpjIh7MeZAcnUiRtVdtdOwk")

    model = genai.GenerativeModel('gemini-1.5-flash')
    
    time_sent = int(time.time())
    response = model.generate_content(prompt)
    time_received = int(time.time())
    
    return (response.text, time_sent, time_received)

def generate_from_file(input_file: str, output_file: str):
    responses = []
    
    with open(input_file, 'r') as f:
        for line in f:
            prompt = line.strip()
            response, time_sent, time_received = get_response(prompt)
            responses.append({
                "Prompt": prompt,
                "Message": response,
                "TimeSent": time_sent,
                "TimeRecvd": time_received,
                "Source": "Gemini"
            })
    
    with open(output_file, 'w') as f:
        json.dump(responses, f, indent=4)

# Example usage:
if __name__ == "__main__":
    input_file = "input.txt"
    output_file = "responses.json"
    generate_from_file(input_file, output_file)
    
    with open('responses.json', 'r') as f:
        data = json.load(f)
        print(json.dumps(data, indent=4))
