# Beacon 
**Secure Remote Execution Tool (SRET)**

Beacon is a proof-of-concept remote administration tool designed for secure, encrypted command execution across a network. It utilizes Python sockets and Fernet symmetric encryption to ensure that commands and outputs remain private.

## Features
* **End-to-End Encryption**: Uses AES-128 via the `cryptography` library.
* **Command Blacklisting**: Prevents high-risk commands (like `rm`) from being executed.
* **Environment Security**: Uses `.env` files to prevent credential leakage.
* **Network Reliability**: Built-in socket timeouts for robust client-server interaction.

## Setup
1. Install dependencies: `pip install -r requirements.txt`
2. Create a `.env` file with your `GHOST_KEY` and `GHOST_PASS`.
3. Run the server: `python ghost.py`
4. Use the client: `python trigger.py`