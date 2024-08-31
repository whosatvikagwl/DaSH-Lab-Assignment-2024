import socket
import threading
import google.generativeai as genai
import os
import json


genai.configure(api_key="AIzaSyDy2GONTyXZTpjIh7MeZAcnUiRtVdtdOwk")

def handle_client(client_socket):
    try:
        while True:
            prompt = client_socket.recv(1024).decode('utf-8')
            if not prompt:
                break

            response = generate_response(prompt)

            message = json.dumps({"Prompt": prompt, "Message": response})
            client_socket.send(message.encode('utf-8'))
    except Exception as e:
        print(f"Error handling client: {e}")
    finally:
        client_socket.close()

def generate_response(prompt: str) -> str:
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(prompt)
    return response.text

def start_server(host='127.0.0.1', port=9999):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)
    print(f"Server listening on {host}:{port}")

    while True:
        client_socket, addr = server.accept()
        print(f"Accepted connection from {addr}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    start_server()
