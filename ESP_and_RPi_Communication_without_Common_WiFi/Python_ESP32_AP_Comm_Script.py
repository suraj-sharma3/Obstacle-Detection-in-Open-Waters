import socket

# ESP32 Access Point IP and Port
ESP32_IP = "192.168.4.1"  # Replace with the actual IP address of your ESP32 Access Point
PORT = 80  # Port for HTTP server

def send_request():
    # Create a TCP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connect to the ESP32 server
        print(f"Connecting to {ESP32_IP}:{PORT}...")
        client_socket.connect((ESP32_IP, PORT))
        print("Connected!")

        # Send an HTTP GET request
        http_request = "GET / HTTP/1.1\r\nHost: ESP32\r\n\r\n"
        client_socket.sendall(http_request.encode())
        print("HTTP GET request sent.")

        # Receive and display the response
        response = client_socket.recv(4096)  # Receive up to 4096 bytes
        print("Response from ESP32:")
        print(response.decode())

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Close the socket
        client_socket.close()
        print("Connection closed.")

# Call the function to send the request
if __name__ == "__main__":
    send_request()
