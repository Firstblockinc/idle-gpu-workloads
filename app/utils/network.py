import socket

def get_local_ip():
    try:
        # Create a socket object
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Connect to a remote server to determine the local IP
        s.connect(('8.8.8.8', 80))
        # Get the local IP address
        local_ip = s.getsockname()[0]
    except Exception as e:
        local_ip = None
        print(f"Error: {e}")
    finally:
        s.close()
    
    return local_ip