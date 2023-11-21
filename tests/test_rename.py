import json
import socket
from pprint import pp


# To install the Python LSP server, run the following command in the terminal:
# pip install "python-lsp-server[rope]" pylspclient pylsp-rope python-lsp-jsonrpc

# rope                          1.11.0
# pylsp-rope                    0.1.11
# pylspclient                   0.0.2
# python-lsp-jsonrpc            1.1.2
# python-lsp-server             1.9.0

# To start the Python LSP server, run the following command in the terminal:
# pylsp --tcp --host 127.0.0.1 --port 2087


def send_request(sock, method, params, request_id):
    """Send a request to the LSP server."""
    message = {
        "jsonrpc": "2.0",
        "id": request_id,
        "method": method,
        "params": params
    }
    message_json = json.dumps(message)
    content_length = len(message_json)
    sock.send(f"Content-Length: {content_length}\r\n\r\n".encode() + message_json.encode())

def receive_response(sock):
    """Receive a response from the LSP server."""
    # Read the headers
    headers = ""
    while True:
        headers += sock.recv(1).decode()
        if headers.endswith("\r\n\r\n"):
            break

    # Extract the content length
    # The line of code you mentioned is extracting the content length from the headers received from
    # the LSP server.
    content_length = int([line for line in headers.split("\r\n") if line.startswith("Content-Length:")][0].split(":")[1].strip())

    # Read the content
    content = sock.recv(content_length).decode()
    return json.loads(content)

# Connect to the LSP server
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('localhost', 2087))  # Make sure this matches your LSP server's address and port

# Initialize the LSP session
init_params = {
    "processId": None,
    "rootUri": "file:///Users/jim/Projects/aider/tests",
    "capabilities": {},
}
send_request(sock, "initialize", init_params, 1)
response = receive_response(sock)
print('initialize response:')
pp(response)

# Send a code action request
code_action_params = {
    "textDocument": {"uri": "file:///Users/jim/Projects/aider/tests/sample.py"},
    "range": {
        "start": {"line": 0, "character": 7},
        "end": {"line": 0, "character": 13}
    },
    "context": {
        "diagnostics": []  # Include any relevant diagnostics here
    }
}
send_request(sock, "textDocument/codeAction", code_action_params, 3)
response = receive_response(sock)
print('codeAction response:')
pp(response, depth=1)
pp(response['result'])

# Send a refactoring request (e.g., rename)
rename_params = {
    "textDocument": {"uri": "file:///Users/jim/Projects/aider/tests/sample.py"},
    "position": {"line": 0, "character": 7},
    "newName": "poodle"
}

send_request(sock, "textDocument/rename", rename_params, 2)
response = receive_response(sock)
print('rename response:')
pp(response, depth=2)
# pp(response['result'], depth=1)
if response['result']:
    changes = response['result']['documentChanges']
    if changes:
        for i, change in enumerate(changes, start=1):
            print(f'rename result documentChange {i}:')
            pp(change, width=120)
    else:
        print('rename result documentChanges empty')
else:
    print('rename result empty')

# Command parameters for extracting a method
command_params = {
    "command": "pylsp_rope.refactor.extract.method",
    "arguments": [
        {
            "document_uri": "file:///Users/jim/Projects/aider/tests/sample.py",
            "range": {
                "start": {"line": 0, "character": 0},
                "end": {"line": 0, "character": 22}
            },
            "global_": False,  # Set to True if you want to extract a global method
            "similar": False  # Set to True if you want to include similar statements
        }
    ]
}

# Send the execute command request
send_request(sock, "workspace/executeCommand", command_params, 4)
response = receive_response(sock)
print('executeCommand response:')
pp(response)
# pp(f"executeCommand response: {response['result']}", depth=1)
# for change in response['result']['documentChanges']:
#     pp(change)


# Close the connection
sock.close()
