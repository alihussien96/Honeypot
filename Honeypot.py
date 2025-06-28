import socket
import threading
from datetime import datetime

# --- Configuration ---
HOST = '0.0.0.0'  # Listen on all available network interfaces
PORT = 23         # Listen on port 23 (Telnet), a common target for attackers
LOG_FILE = 'honeypot.log'

def log_event(message):
    """Logs an event with a timestamp to the log file and prints it."""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_message = f"[{timestamp}] {message}"
    print(log_message)
    with open(LOG_FILE, 'a') as f:
        f.write(log_message + '\n')

def handle_connection(client_socket, client_address):
    """Handles an individual client connection."""
    ip, port = client_address
    log_event(f"New connection from: {ip}:{port}")

    try:
        # Send a fake welcome banner to the attacker
        client_socket.send(b"Welcome to the Telnet service\nLogin: ")

        # Loop to receive data from the attacker
        while True:
            # Receive data in small chunks
            data = client_socket.recv(1024)
            if not data:
                # Connection closed by the client
                break
            
            # Log the received data
            # Using repr() to see non-printable characters
            log_event(f"Data received from {ip}:{port} -> {repr(data)}")
            
            # Keep the connection alive by sending a fake prompt
            client_socket.send(b"> ")

    except ConnectionResetError:
        log_event(f"Connection reset by {ip}:{port}")
    except Exception as e:
        log_event(f"An error occurred with {ip}:{port}: {e}")
    finally:
        # Clean up the connection
        log_event(f"Connection closed for {ip}:{port}")
        client_socket.close()

def start_honeypot():
    """Starts the main honeypot server."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Allow reusing the address to avoid "Address already in use" errors
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        server.bind((HOST, PORT))
        server.listen(5) # Listen for up to 5 concurrent connections
        log_event(f"Honeypot started. Listening on {HOST}:{PORT}...")

        # Main loop to accept new connections
        while True:
            client_socket, client_address = server.accept()
            # Create a new thread to handle the client so the main loop isn't blocked
            client_handler = threading.Thread(target=handle_connection, args=(client_socket, client_address))
            client_handler.start()

    except PermissionError:
        log_event(f"[ERROR] Permission denied to bind to port {PORT}. Try running with sudo or choosing a port > 1024.")
    except Exception as e:
        log_event(f"[ERROR] An error occurred while starting the server: {e}")
    finally:
        server.close()
        log_event("Honeypot server shut down.")

# --- Main Execution Block ---
if __name__ == '__main__':
    start_honeypot()
  
