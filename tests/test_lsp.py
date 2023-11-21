from pathlib import Path

from pprint import pp

from aider.dump import dump
from aider.lsp import LSPClient, lsp_kind_to_name

# LSP root dir is URI of this file's directory

project_uri = Path.cwd().as_uri()
dump(project_uri)
client = LSPClient('localhost', 2087, project_uri)

response = client.get_document_symbols('tests/sample.py')
pp(response)
for symbol in response['result']:
    location = symbol['location']
    if symbol['containerName']:
        print(f"{lsp_kind_to_name(symbol['kind'])} {symbol['containerName']}:{symbol['name']}")
    else:
        print(f"{lsp_kind_to_name(symbol['kind'])} {symbol['name']}")
    print('get start')
    definition = client.get_definition(path=location['uri'], position=symbol['location']['range']['start'])
    dump(definition)
    print('get end')
    definition = client.get_definition(path=location['uri'], position=symbol['location']['range']['end'])
    dump(definition)

# Example of using the extract_method
extract_method_response = client.extract_method(
    'tests/sample.py',
    {"line": 2, "character": 0},
    {"line": 3, "character": 0},
    False,
    False
)

pp(extract_method_response, depth=4)
pp(type(extract_method_response['params']['edit']['changes']))
dump(extract_method_response['params']['edit']['changes'])
for path, change in extract_method_response['params']['edit']['changes'].items():
    print(type(change))
    pp(path)
    dump(change)

client.close()
