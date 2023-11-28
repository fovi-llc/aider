from aider.coders.base_coder import Coder

class RefactorFunctionCoder(Coder):
    def generate_prompt(self, repo_map, file_path, start_line, end_line):
        # This method will generate the prompt for the model
        # Retrieve the source file from the repo_map
        source_file = repo_map.get_file_content(file_path)
        # Extract the relevant lines of code
        lines = source_file.split('\n')[start_line - 1:end_line]
        # Add line numbers to the extracted lines
        numbered_lines = [f"{i + start_line}: {line}" for i, line in enumerate(lines)]
        # Generate the prompt with line numbers
        prompt = (
            f"Refactor the function in the following Python code from {file_path} starting from line {start_line} to line {end_line}:\n\n"
            + "\n".join(numbered_lines)
        )
        return prompt

    def process_response(self, response):
        # This method will process the response from the model
        # and return the refactored code or necessary edits
        # For now, we will just return the response as is
        return response
