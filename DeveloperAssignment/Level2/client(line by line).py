import socket
import json
import os
import sys
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def read_prompt_from_file(input_file, line_number):
    with open(input_file, 'r') as f:
        lines = f.readlines()
        if line_number < len(lines):
            return lines[line_number].strip()
        else:
            return None

def update_last_processed_line(log_file, line_number):
    with open(log_file, 'w') as f:
        f.write(str(line_number))

def get_next_line_number(log_file, total_lines):
    try:
        with open(log_file, 'r') as f:
            last_line = int(f.read().strip())
    except (FileNotFoundError, ValueError):
        last_line = -1

    next_line = (last_line + 1) % total_lines  # Loop back to the first line if we reach the end
    update_last_processed_line(log_file, next_line)
    return next_line

def send_prompt_to_server(prompt):
    try:
        # Create a socket object
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.settimeout(10)  # Set a timeout for the socket operations

        # Connect to the server
        server_host = '127.0.0.1'
        server_port = 9999
        client_socket.connect((server_host, server_port))

        # Send the prompt to the server
        client_socket.sendall(prompt.encode('utf-8'))

        # Receive the response from the server
        response = client_socket.recv(4096).decode('utf-8')
        print(f"Received response: {response}")

        # Save the response to a JSON file
        output_file = "client_responses.json"
        with open(output_file, 'a') as f:
            json.dump({
                "Prompt": prompt,
                "Message": response,
                "Source": "Gemini"
            }, f, indent=4)
            f.write('\n')  # Newline for readability

    except socket.error as e:
        print(f"Error sending prompt or receiving response: {e}")
    finally:
        # Close the connection
        client_socket.close()

if __name__ == "__main__":
    input_file = "input.txt"
    log_file = "last_processed_line.txt"

    # Get the total number of lines in input.txt
    with open(input_file, 'r') as f:
        total_lines = len(f.readlines())

    # Get the next line number to process
    line_number = get_next_line_number(log_file, total_lines)

    # Read the corresponding prompt from the file
    prompt = read_prompt_from_file(input_file, line_number)
    if prompt:
        send_prompt_to_server(prompt)
    else:
        print(f"No prompt found at line {line_number}")
