import socket
import os
from cryptography.fernet import Fernet
from dotenv import load_dotenv

# Load secrets from .env
load_dotenv()

class BeaconTrigger:
    def __init__(self, target_ip='127.0.0.1', port=9999):
        self.target_ip = target_ip
        self.port = port
        self.key = os.getenv("GHOST_KEY").encode()
        self.password = os.getenv("GHOST_PASS")
        self.cipher = Fernet(self.key)

    def fire(self, cmd):
        """Encrypts and sends a command to the Beacon server."""
        payload = f"{self.password}:{cmd}".encode()
        encrypted_payload = self.cipher.encrypt(payload)

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(5) # Prevents the client from hanging
            try:
                s.connect((self.target_ip, self.port))
                s.send(encrypted_payload)
                
                # Decrypt the server's response
                raw_response = s.recv(4096)
                return self.cipher.decrypt(raw_response).decode()
            except Exception as e:
                return f"[!] Error: {e}"

if __name__ == "__main__":
    trigger = BeaconTrigger()
    print("--- Beacon Control Interface ---")
    while True:
        command = input("beacon@remote:~$ ")
        if command.lower() in ['exit', 'quit']: break
        if not command.strip(): continue
        
        result = trigger.fire(command)
        print(f"\n{result}\n")