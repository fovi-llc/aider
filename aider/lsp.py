import json
import socket

class LSPClient:
    def __init__(self, host, port, project_uri):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))
        self.request_id = 1
        self.project_uri = project_uri
        self.initialize()
        self.command_mapping = {
            "extract_method": "pylsp_rope.refactor.extract.method",
            "extract_variable": "pylsp_rope.refactor.extract.variable",
            "organize_imports": "pylsp_rope.source.organize_import",
            "extract_method": "pylsp_rope.refactor.extract.method",
            "extract_variable": "pylsp_rope.refactor.extract.variable",
            # Add more mappings here as needed
        }

    def send_request(self, method, params):
        message = {
            "jsonrpc": "2.0",
            "id": self.request_id,
            "method": method,
            "params": params
        }
        self.request_id += 1
        message_json = json.dumps(message)
        content_length = len(message_json)
        self.sock.send(f"Content-Length: {content_length}\r\n\r\n".encode() + message_json.encode())

    def receive_response(self):
        """Receive a response from the LSP server."""
        # Read the headers
        headers = ""
        while True:
            headers += self.sock.recv(1).decode()
            if headers.endswith("\r\n\r\n"):
                break

        # Extract the content length
        content_length = int([line for line in headers.split("\r\n") if line.startswith("Content-Length:")][0].split(":")[1].strip())

        # Read the content
        content = self.sock.recv(content_length).decode()
        return json.loads(content)

    def initialize(self):
        init_params = {
            "processId": None,
            "rootUri": self.project_uri,
            "capabilities": {},
        }
        self.send_request("initialize", init_params)
        return self.receive_response()

    def document_uri(self, relative_path):
        if relative_path.startswith("file:"):
            return relative_path
        return self.project_uri + "/" + relative_path

    def execute_command(self, command, path, range_start, range_end, additional_args=None):
        if additional_args is None:
            additional_args = {}

        command_params = {
            "command": command,
            "arguments": [
                {
                    "document_uri": self.document_uri(path),
                    "range": {
                        "start": range_start,
                        "end": range_end
                    },
                    **additional_args
                }
            ]
        }
        # pp(command_params)
        self.send_request("workspace/executeCommand", command_params)
        return self.receive_response()

    def extract_method(self, path, range_start, range_end, global_=False, similar=False):
        command = self.command_mapping["extract_method"]
        additional_args = {"global_": global_, "similar": similar}
        return self.execute_command(command, self.document_uri(path), range_start, range_end, additional_args)

    def extract_variable(self, path, range_start, range_end, variable_name):
        command = self.command_mapping["extract_variable"]
        additional_args = {"name": variable_name}
        return self.execute_command(command, self.document_uri(path), range_start, range_end, additional_args)

    def extract_method(self, path, range_start, range_end, method_name):
        command = self.command_mapping["extract_method"]
        additional_args = {"name": method_name}
        return self.execute_command(command, self.document_uri(path), range_start, range_end, additional_args)

    def close(self):
        self.sock.close()
    
    def get_document_symbols(self, path):
        params = {
            "textDocument": {"uri": self.document_uri(path)}
        }
        self.send_request("textDocument/documentSymbol", params)
        return self.receive_response()
    
    def get_definition(self, path, position):
        params = {
            "textDocument": {"uri": self.document_uri(path)},
            "position": position
        }
        # pp(params)
        self.send_request("textDocument/definition", params)
        return self.receive_response()

def lsp_kind_to_name(kind):
    lsp_kind_map = {
        1: "File",
        2: "Module",
        3: "Namespace",
        4: "Package",
        5: "Class",
        6: "Method",
        7: "Property",
        8: "Field",
        9: "Constructor",
        10: "Enum",
        11: "Interface",
        12: "Function",
        13: "Variable",
        14: "Constant",
        15: "String",
        16: "Number",
        17: "Boolean",
        18: "Array",
        19: "Object",
        20: "Key",
        21: "Null",
        22: "EnumMember",
        23: "Struct",
        24: "Event",
        25: "Operator",
        26: "TypeParameter"
    }
    
    return lsp_kind_map.get(kind, "Unknown")

