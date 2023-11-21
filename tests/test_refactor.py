from pylspclient import LspClient
import socket
import json
import os

# Connect to the LSP server
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 2087) # Port where your LSP server is running
sock.connect(server_address)


client = LspClient(sock)

# The file and code you want to refactor
file_uri = 'file:///Users/jim/Projects/aider/tests/sample.py'
code = """def example_function():
    print("Hello, World!")
"""

# Prepare initialization parameters
root_uri = 'file:///Users/jim/Projects/aider/tests'
initialization_options = {}  # Any server-specific initialization options
capabilities = {}  # Client capabilities
trace = 'off'
workspace_folders = None

# Initialize the LSP session
client.initialize(
    processId=os.getpid(),
    rootPath=os.path.dirname(root_uri),
    rootUri=root_uri,
    initializationOptions=initialization_options,
    capabilities=capabilities,
    trace=trace,
    workspaceFolders=workspace_folders
)

# Send a request for refactoring (e.g., rename)
rename_params = {
    "textDocument": {"uri": file_uri},
    "position": {"line": 1, "character": 5}, # Position in the code to refactor
    "newName": "new_function_name"
}

response = client.rename(rename_params)
print(json.dumps(response, indent=4))

# Don't forget to close the connection
client.close()
