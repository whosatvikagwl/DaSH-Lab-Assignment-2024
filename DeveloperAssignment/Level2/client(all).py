import socket
import json

def connect_to_server(host='127.0.0.1', port=9999):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))
    return client

def send_prompt(client, prompt: str):
    try:
        client.sendall(prompt.encode('utf-8'))  # Ensure the entire message is sent
        response = client.recv(4096).decode('utf-8')  # Increased buffer size to avoid truncation
        return json.loads(response)
    except Exception as e:
        print(f"Error sending prompt or receiving response: {e}")
        return None

def save_response_to_file(response, output_file='client_responses.json'):
    if response:
        with open(output_file, 'a') as f:
            json.dump(response, f, indent=4)
            f.write("\n")

if __name__ == "__main__":
    input_file = "input.txt"
    client = connect_to_server()

    try:
        with open(input_file, 'r') as f:
            for line in f:
                prompt = line.strip()
                if prompt:
                    response = send_prompt(client, prompt)
                    save_response_to_file(response)
    except Exception as e:
        print(f"Error reading input file or processing prompts: {e}")
    finally:
        client.close()
